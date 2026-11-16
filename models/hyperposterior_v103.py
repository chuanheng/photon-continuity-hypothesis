"""v1.03 GitHub companion: continuous sensor hyperposterior via Laplace-informed
importance weights, Gaussian latent phase path, and calibrated HOM nuisance.

Synthetic conventional quantum optics, NOT permanent photon-history evidence.
The exact 38/38 locally executed code and its full data are in ZIP.
"""
import numpy as np
from scipy.linalg import solve_triangular
from scipy.special import logsumexp
from models.continuous_calibration_v102 import (
 Setup,fit_sensor,sensor_nll,phase_draws,calibration_draws,forward)

BOUNDS=np.array([[np.log(.015),np.log(.5)], [np.log(.025),np.log(.55)],[-.3,.3]])

def sensor_log_posterior(x,rec):
    x=np.asarray(x,float)
    if x.shape!=(3,) or np.any(x<=BOUNDS[:,0]) or np.any(x>=BOUNDS[:,1]):
        return -np.inf
    return -sensor_nll(x,rec['y'],rec['z'])

def hyper_mle(rec):
    h=fit_sensor(rec['y'],rec['z'])
    return np.array([np.log(h['walk_sd']),np.log(h['read_sd']),h['bias']])

def numerical_hessian(x,rec,step=(.012,.012,.002)):
    h=np.asarray(step,float);z=np.zeros((3,3));f=lambda a:sensor_nll(a,rec['y'],rec['z'])
    f0=f(x)
    for i in range(3):
        a=np.zeros(3);a[i]=h[i]
        z[i,i]=(f(x+a)-2*f0+f(x-a))/h[i]**2
        for j in range(i):
            b=np.zeros(3);b[j]=h[j]
            z[i,j]=z[j,i]=(f(x+a+b)-f(x+a-b)-f(x-a+b)+f(x-a-b))/(4*h[i]*h[j])
    return z

def sample_hyper(rec,n=100,seed=10301,scale=1.4):
    if n<10 or scale<=0:raise ValueError('sample settings')
    center=hyper_mle(rec);H=numerical_hessian(center,rec)
    eigen,V=np.linalg.eigh(H)
    cov=(V*(scale*scale/np.maximum(eigen,.001)))@V.T
    L=np.linalg.cholesky(cov)
    rng=np.random.default_rng(seed)
    accepted=[];attempts=0
    while len(accepted)<n and attempts<80*n:
        K=max(2*(n-len(accepted)),8)
        vals=center+rng.normal(size=(K,3))@L.T
        accepted.extend(vals[np.all((vals>BOUNDS[:,0])&(vals<BOUNDS[:,1]),axis=1)][:n-len(accepted)])
        attempts+=K
    if len(accepted)<n:raise RuntimeError('hyper proposal acceptance')
    samples=np.asarray(accepted)
    z=solve_triangular(L,(samples-center).T,lower=True).T
    logproposal=-.5*np.sum(z*z,axis=1)
    logtarget=np.array([sensor_log_posterior(x,rec) for x in samples])
    w=np.exp(logtarget-logproposal-logsumexp(logtarget-logproposal))
    return {'theta':samples,'weights':w,'ess':float(1/np.sum(w*w)),
            'mle':center,'hessian_eigen':eigen}

def calibrated_optical_grid(rec,settings,attenuation,particles,importance_weights):
    A=np.asarray(attenuation,float);w=np.asarray(importance_weights,float)
    if len(A)!=len(particles) or len(w)!=len(A) or not np.isclose(sum(w),1):
        raise ValueError('matching weights and particles')
    M=np.linspace(.01,.99,161)
    c0=[];slope=[];far=[]
    for p,f,q in particles:
        a=forward(0,1,p,f,q);b=forward(1,1,p,f,q)
        c0.append(a[0]);slope.append(a[0]-b[0]);far.append(a[1])
    c0=np.asarray(c0);slope=np.asarray(slope);far=np.asarray(far)
    prob=c0[None,:]-M[:,None]*A[None,:]*slope[None,:]
    if np.any((prob<=0)|(prob>=1)):raise ValueError('optics')
    near_ll=rec['near']*np.log(prob)+(settings.shots-rec['near'])*np.log1p(-prob)
    far_ll=rec['far']*np.log(far)+(settings.shots-rec['far'])*np.log1p(-far)
    l=logsumexp(near_ll+far_ll[None,:]+np.log(w)[None,:],axis=1)
    mass=np.exp(l-logsumexp(l));cdf=np.cumsum(mass)
    lo,hi=np.interp([.025,.975],cdf,M)
    wf=np.exp(np.log(w)+far_ll-logsumexp(np.log(w)+far_ll))
    return {'mean':float(M@mass),'ci95':[float(lo),float(hi)],
        'width':float(hi-lo),'far_particle_ess':float(1/np.sum(wf**2))}

def infer(rec,settings=Setup(),draws=100,seed=10301):
    rng=np.random.default_rng(seed)
    h=sample_hyper(rec,draws,seed)
    A=[]
    for theta in h['theta']:
        hyper={'walk_sd':float(np.exp(theta[0])),
               'read_sd':float(np.exp(theta[1])),'bias':float(theta[2])}
        A.append(float(phase_draws(rec['y'],hyper,1,rng)[0]))
    parts=calibration_draws(rec,settings,draws,rng)
    joint=calibrated_optical_grid(rec,settings,A,parts,h['weights'])
    plugin={'walk_sd':float(np.exp(h['mle'][0])),'read_sd':float(np.exp(h['mle'][1])),'bias':float(h['mle'][2])}
    AP=phase_draws(rec['y'],plugin,draws,np.random.default_rng(seed+2))
    ref=calibrated_optical_grid(rec,settings,AP,parts,np.ones(draws)/draws)
    return {'joint':joint,'plugin':ref,'hyper_ess':h['ess'],
       'hyper_mean':np.sum(h['weights'][:,None]*np.c_[np.exp(h['theta'][:,:2]),h['theta'][:,2]],axis=0).tolist(),
       'hyper_uncertainty_integrated':True,'calibration_nuisance_sampled':True}

def audit(n=40,draws=100,seed=103000,settings=Setup()):
    from models.continuous_calibration_v102 import simulate
    rows=[]
    for i in range(n):
        rec=simulate(seed+19*i,settings)
        fit=infer(rec,settings,draws,seed+80000+19*i)
        rows.append({'seed':seed+19*i,'joint':fit['joint'],'plugin':fit['plugin'],
            'joint_covered':fit['joint']['ci95'][0]<=settings.M<=fit['joint']['ci95'][1],
            'plugin_covered':fit['plugin']['ci95'][0]<=settings.M<=fit['plugin']['ci95'][1],
            'hyper_ess':fit['hyper_ess']})
    return {'version':'v1.03','n':n,'M_truth':settings.M,
        'joint_covered':sum(r['joint_covered'] for r in rows),
        'plugin_covered':sum(r['plugin_covered'] for r in rows),
        'median_hyper_ess':float(np.median([r['hyper_ess'] for r in rows])),
        'rows':rows,'synthetic_only':True}
