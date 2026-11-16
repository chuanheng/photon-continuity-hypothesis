"""v1.07 GitHub companion: independent two-photon rho reference and
joint *conditional-known-nuisance* intrinsic HOM inference.

This simplified companion is NOT byte-identical to the 600-inference
original local ZIP. It omits sensor/nuisance latent calibration, which is
included in the 44-test original local code. No historical photon identity.
"""
import numpy as np
from scipy.special import logsumexp
from models.gram_v107 import restricted_rho

RHO_GRID=np.linspace(0,1,801)
M_GRID=np.linspace(.005,.995,251)

def pair_prob(rho):
    if np.any((np.asarray(rho)<0)|(np.asarray(rho)>1)):
        raise ValueError('rho')
    return (1-np.asarray(rho))/2

def ref_counts(rho,shots,seed=107):
    if not 0<=rho<=1 or shots<0 or int(shots)!=shots:
        raise ValueError('reference')
    return {'shots':int(shots),
        'coincidences':int(np.random.default_rng(seed).binomial(shots,pair_prob(rho)))}

def rho_reference(ref):
    N=int(ref['shots']);k=int(ref['coincidences'])
    if not 0<=k<=N:raise ValueError('counts')
    p=pair_prob(RHO_GRID)
    ll=np.zeros_like(p)
    if k:ll+=k*np.log(np.maximum(p,1e-300))
    if N-k:ll+=(N-k)*np.log1p(-p)
    w=np.exp(ll-logsumexp(ll))
    return {'grid':RHO_GRID,'mass':w,'mean':float(w@RHO_GRID),
        'ci95':np.interp([.025,.975],np.cumsum(w),RHO_GRID).tolist()}

def click(k,eta,dark):
    return 1-(1-dark)*(1-eta)**k

def optical(M,rho,atten=.8,f=.14,q=.014,ea=.74,eb=.68,da=.002,db=.003):
    # restricted same-mode two photon a input and one photon b input
    A=[click(k,ea,da) for k in range(4)]
    B=[click(k,eb,db) for k in range(4)]
    c11=A[1]*B[1];c20=A[2]*B[0];c02=A[0]*B[2];c00=A[0]*B[0]
    mid=.5*c11+.25*(c20+c02)
    same=np.array([3,1,1,3])/8
    distinguish=np.array([1,3,3,1])/8
    triple0=sum(distinguish[k]*A[k]*B[3-k] for k in range(4))
    triple1=sum(same[k]*A[k]*B[3-k] for k in range(4))
    t=triple0+(triple1-triple0)*rho
    pair=mid-M*atten*(.5*c11-.25*(c20+c02))
    near=(.9-f)*pair+.08*mid+.02*c00+f*t
    far=(.98-f)*mid+.02*c00+f*triple0
    return np.broadcast_arrays(q+(1-q)*near,q+(1-q)*far)

def main_record(seed=1,trueM=.72,true_rho=.10,atten=.8,shots=1500):
    if not 0<=trueM<=1 or not 0<=true_rho<=1:raise ValueError('truth')
    pn,pf=optical(trueM,true_rho,atten)
    g=np.random.default_rng(seed)
    return {'near':int(g.binomial(shots,float(pn))),
        'far':int(g.binomial(shots,float(pf))),
        'shots':shots,'attenuation_assumed_known':atten,
        'true_M':trueM,'true_rho':true_rho}

def fit(rec,reference,oracle_rho=None):
    # independent rho reference calibrates the common pure internal modes
    rw=rho_reference(reference)
    grid=rw['grid']
    if oracle_rho is not None:
        if not 0<=oracle_rho<=1:raise ValueError('oracle')
        grid=np.array([oracle_rho]);weights=np.array([1.])
    else:weights=rw['mass']
    near,far=optical(M_GRID[:,None],grid[None,:],
        atten=rec['attenuation_assumed_known'])
    N=rec['shots'];k=rec['near']
    logl=k*np.log(near)+(N-k)*np.log1p(-near)
    logw=logl+np.log(weights)[None,:]
    w=np.exp(logw-logsumexp(logw));pm=w.sum(axis=1);pr=w.sum(axis=0)
    ci=np.interp([.025,.975],np.cumsum(pm),M_GRID)
    return {'M_mean':float(M_GRID@pm),'M_ci95':ci.tolist(),
        'rho_mean':float(grid@pr),'rho_ref_shots':reference['shots'],
        'known_nuisance_simplification':True}

def paired_demo(n=30,seed=10701):
    cases={'wrong':None,'ref_0':0,'ref_100':100,'ref_1000':1000,
       'ref_10000':10000,'oracle':-1}
    rows={k:[] for k in cases}
    for i in range(n):
        s=seed+1009*i;obs=main_record(s)
        for key,num in cases.items():
            ref=ref_counts(obs['true_rho'],max(0,num or 0),s+2000)
            r=fit(obs,ref,oracle_rho=(1 if num is None else .1 if num==-1 else None))
            r['covered']=bool(r['M_ci95'][0]<=obs['true_M']<=r['M_ci95'][1])
            rows[key].append(r)
    return {k:{'n':n,'mean_M':float(np.mean([x['M_mean'] for x in v])),
       'covered':sum(x['covered'] for x in v),'records':v}
       for k,v in rows.items()}
