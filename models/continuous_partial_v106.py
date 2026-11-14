"""v1.06 Github counterpart: restricted three-boson partial-mode overlap,
continuous Gaussian sensor hyperprior, and fixed-truth synthetic audit.
Full exact 43-test locally executed model and 500 records are in ZIP.

The special input |2_phi,1_psi> has two phi photons in one port,
psi in the other, and |<phi|psi>|^2=rho. Not generic Gram 3-photon theory.
"""
from dataclasses import dataclass
import numpy as np
from scipy.optimize import minimize
from scipy.linalg import solve_triangular
from scipy.special import logsumexp
from models.full_sbc_v105 import (T,REPEATS,NZERO,NOPT,NSRC,NSTD,NREF,NDARK,
    calibration_particles)

FULL=np.array([3,1,1,3])/8
DIST=np.array([1,3,3,1])/8
LO=np.array([np.log(.045),np.log(.08),-.06])
HI=np.array([np.log(.22),np.log(.28),.06])

def triplet_probabilities(rho):
    if not np.isfinite(rho) or not 0<=rho<=1:raise ValueError('rho outside [0,1]')
    return rho*FULL+(1-rho)*DIST

def optical(M,A,f,q,ea,eb,da,db,rho=1.):
    ca=[1-(1-da)*(1-ea)**k for k in range(4)]
    cb=[1-(1-db)*(1-eb)**k for k in range(4)]
    c20=ca[2]*cb[0];c11=ca[1]*cb[1];c02=ca[0]*cb[2];c00=ca[0]*cb[0]
    mid=.5*c11+.25*(c20+c02)
    trip_near=sum(float(v)*ca[k]*cb[3-k] for k,v in enumerate(triplet_probabilities(rho)))
    trip_far=sum(float(v)*ca[k]*cb[3-k] for k,v in enumerate(DIST))
    near=(.9-f)*(mid-M*A*(.5*c11-.25*(c20+c02)))+.08*mid+.02*c00+f*trip_near
    far=(.98-f)*mid+.02*c00+f*trip_far
    return np.broadcast_arrays(q+(1-q)*near,q+(1-q)*far)

@dataclass(frozen=True)
class Setting:
    M:float=.72
    f:float=.065
    rho:float=1.
    q:float=.014
    ea:float=.74
    eb:float=.68
    da:float=.002
    db:float=.003
    sw:float=.095
    sr:float=.15
    bias:float=.015
    anomaly_fraction:float=0.

def make_record(seed=106001,s=Setting()):
    if not(0<s.M<1 and 0<=s.rho<=1 and 0<=s.f<.9 and 0<=s.anomaly_fraction<=1):raise ValueError('setting')
    rng=np.random.default_rng(seed)
    u=np.r_[0.,np.cumsum(rng.normal(0,s.sw,T-1))]
    y=u[:,None]+s.bias+rng.normal(0,s.sr,(T,REPEATS))
    z=s.bias+rng.normal(0,s.sr,NZERO)
    if s.anomaly_fraction:
        flags=rng.random(y.shape)<s.anomaly_fraction
        y+=flags*rng.normal(0,.55,y.shape)
        flags=rng.random(z.shape)<s.anomaly_fraction
        z+=flags*rng.normal(0,.55,z.shape)
    r=s.f/.9;alpha=.2;beta=.025
    obs={'y':y,'zero':z,
      'source_report_triplet':int(rng.binomial(NSRC,r*(1-alpha)+(1-r)*beta)),
      'triplet_as_pair':int(rng.binomial(NSTD,alpha)),
      'pair_as_triplet':int(rng.binomial(NSTD,beta)),
      'q_click':int(rng.binomial(NREF,s.q)),
      'eta_a_click':int(rng.binomial(NREF,s.ea)),
      'eta_b_click':int(rng.binomial(NREF,s.eb)),
      'dark_a_click':int(rng.binomial(NDARK,s.da)),
      'dark_b_click':int(rng.binomial(NDARK,s.db))}
    A=float(np.mean(np.exp(-abs(u))))
    near,far=optical(s.M,A,s.f,s.q,s.ea,s.eb,s.da,s.db,s.rho)
    obs['near']=int(rng.binomial(NOPT,float(near)))
    obs['far']=int(rng.binomial(NOPT,float(far)))
    return obs,{'M':s.M,'A':A,'rho':s.rho,'walk':s.sw,'read':s.sr,'bias':s.bias}

def sensor_loglike(x,y,z):
    if np.any(x<=LO) or np.any(x>=HI):return -np.inf
    sw,sr=np.exp(x[:2]);b=x[2];k=y.shape[1]
    avg=y.mean(axis=1);variance=sr*sr
    C=sw**2*np.minimum.outer(np.arange(T),np.arange(T))+np.eye(T)*variance/k
    L=np.linalg.cholesky(C)
    d=solve_triangular(L,avg-b,lower=True)
    ss=np.sum((y-avg[:,None])**2)
    return float(-.5*(T*np.log(2*np.pi)+2*np.log(np.diag(L)).sum()+d@d+
       T*(k-1)*np.log(2*np.pi*variance)+ss/variance+
       len(z)*np.log(2*np.pi*variance)+sum((z-b)**2)/variance))

def phase_posterior_sample(y,x,rng):
    sw,sr=np.exp(x[:2]);b=x[2];n=T-1;v=sr*sr;k=y.shape[1]
    Q=np.diag(np.r_[np.full(n-1,2),1])/sw**2+np.eye(n)*k/v
    idx=np.arange(n-1);Q[idx,idx+1]=-1/sw**2;Q[idx+1,idx]=-1/sw**2
    L=np.linalg.cholesky(Q)
    h=np.sum(y[1:]-b,axis=1)/v
    m=np.linalg.solve(L.T,np.linalg.solve(L,h))
    u=m+solve_triangular(L.T,rng.normal(size=n),lower=False)
    return np.mean(np.exp(-np.abs(np.r_[0,u])))

def hyper_samples(obs,n=120,seed=55):
    if n<20:raise ValueError('n')
    rng=np.random.default_rng(seed)
    x0=np.array([np.log(.1),np.log(.15),0.])
    fit=minimize(lambda t:-sensor_loglike(t,obs['y'],obs['zero']),x0,
       bounds=list(zip(LO+1e-5,HI-1e-5)),method='L-BFGS-B')
    center=np.clip(fit.x,LO+[.04,.04,.009],HI-[.04,.04,.009])
    h=np.array([.015,.015,.0015])
    def objective(t):return -sensor_loglike(t,obs['y'],obs['zero'])
    H=np.empty((3,3))
    for i in range(3):
        a=np.eye(3)[i]*h[i];H[i,i]=(objective(center+a)-2*objective(center)+objective(center-a))/h[i]**2
        for j in range(i):
            b=np.eye(3)[j]*h[j]
            H[i,j]=H[j,i]=(objective(center+a+b)-objective(center+a-b)-objective(center-a+b)+objective(center-a-b))/(4*h[i]*h[j])
    vals,V=np.linalg.eigh(H)
    cov=(V*(1.5**2/np.maximum(vals,.3)))@V.T;L=np.linalg.cholesky(cov)
    samples=[];attempts=0
    while len(samples)<n:
        attempts+=1
        if attempts>200:raise RuntimeError('hyper proposals rejected')
        x=fit.x+rng.normal(size=(2*n,3))@L.T
        z=x[np.all((x>LO)&(x<HI),axis=1)]
        samples.extend(z[:n-len(samples)])
    samples=np.asarray(samples[:n])
    d=solve_triangular(L,(samples-fit.x).T,lower=True).T
    lw=np.array([sensor_loglike(x,obs['y'],obs['zero']) for x in samples])+.5*np.sum(d*d,axis=1)
    weights=np.exp(lw-logsumexp(lw))
    return samples,weights,float(1/sum(weights*weights))

def infer(obs,rho=1.,n=120,seed=75):
    rng=np.random.default_rng(seed)
    theta,hw,ess=hyper_samples(obs,n,seed+10)
    atten=np.array([phase_posterior_sample(obs['y'],t,rng) for t in theta])
    calibration,source_evidence=calibration_particles(obs,n,rng)
    M=np.linspace(.005,.995,151)
    pnear,pfar=optical(M[:,None],atten[None,:],.9*calibration['f_ratio'][None,:],
         calibration['q'][None,:],calibration['eta_a'][None,:],calibration['eta_b'][None,:],
         calibration['dark_a'][None,:],calibration['dark_b'][None,:],rho)
    logl=(obs['near']*np.log(pnear)+(NOPT-obs['near'])*np.log1p(-pnear)+
          obs['far']*np.log(pfar)+(NOPT-obs['far'])*np.log1p(-pfar)+
          np.log(hw)[None,:]+source_evidence[None,:])
    w=np.exp(logl-logsumexp(logl));prob=w.sum(axis=1)
    ci=np.interp([.025,.975],np.cumsum(prob),M)
    return {'mean':float(M@prob),'ci95':ci.tolist(),'width':float(ci[1]-ci[0]),
       'hyper_ess':ess,'rho_assumed':rho}

def small_audit(n=10,seed=10600,particles=120):
    scenarios={
      'matched':(Setting(),1.),
      'partial_wrong':(Setting(f=.14,rho=.1),1.),
      'partial_oracle':(Setting(f=.14,rho=.1),.1),
      'hyper_outside':(Setting(sw=.31,sr=.32,bias=.11),1.),
      'sensor_outliers':(Setting(anomaly_fraction=.08),1.)}
    out={}
    for name,(setting,assumption) in scenarios.items():
        rows=[]
        for i in range(n):
            obs,truth=make_record(seed+1019*i,setting)
            result=infer(obs,assumption,particles,seed+80000+19*i)
            result['covers_fixed_truth']=bool(result['ci95'][0]<=truth['M']<=result['ci95'][1])
            rows.append(result)
        out[name]={'n':n,'coverage_count':sum(x['covers_fixed_truth'] for x in rows),
            'mean_estimate':float(np.mean([x['mean'] for x in rows])),
            'median_ess':float(np.median([x['hyper_ess'] for x in rows])),'rows':rows}
    return out
