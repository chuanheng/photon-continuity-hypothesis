"""v0.82 Poisson detector counts + shared latent AR(1) phase, penalized profile LRT.

Research toy model, not QED. Known AR(1) hyperparameters in v0.82;
bootstrap refits physical nuisance and latent phase for EVERY replication.
"""
from __future__ import annotations
import numpy as np
from scipy.optimize import minimize
from scipy.special import gammaln

DEFAULT = dict(exposure=80., eta=.72, visibility=.75, dark=.8, beta=.21,
               delta=.18, rho=.8, sigma=.12)

def phase_covariance(t, rho=.8, sigma=.12):
    if not isinstance(t,int) or t<2 or not (-1<rho<1 and sigma>0):
        raise ValueError('invalid AR1 inputs')
    grid=np.arange(t)
    return sigma**2/(1-rho**2)*rho**abs(grid[:,None]-grid[None,:])

def source_means(x, u, eta, visibility, dark, beta, delta, exposure=80.):
    x=np.asarray(x,float);u=np.asarray(u,float)
    if x.shape!=u.shape or x.ndim!=1:raise ValueError('phase shapes')
    if not (0<eta<1 and 0<visibility<1 and dark>0 and exposure>0):
        raise ValueError('invalid physical parameters')
    theta=x[:,None]+u[:,None]+beta+np.array([0,delta])[None,:]
    a=exposure*eta/2
    plus=a*(1+visibility*np.cos(theta))+dark
    minus=a*(1-visibility*np.cos(theta))+dark
    return np.stack([plus,minus],axis=-1)

def simulate_data(t=10, delta=None, seed=82, **overrides):
    p={**DEFAULT,**overrides}
    if delta is not None:p['delta']=delta
    x=np.linspace(.18,2*np.pi+.18,t,endpoint=False)
    rng=np.random.default_rng(seed)
    u=rng.multivariate_normal(np.zeros(t),phase_covariance(t,p['rho'],p['sigma']))
    mu=source_means(x,u,p['eta'],p['visibility'],p['dark'],p['beta'],p['delta'],p['exposure'])
    counts=rng.poisson(mu)
    dark_counts=rng.poisson(p['dark'],size=(t,2))
    return {'x':x,'counts':counts,'dark_counts':dark_counts,'latent_true':u,
            'exposure':float(p['exposure']),'rho':float(p['rho']),'sigma':float(p['sigma'])}

def poisson_nll(counts, means):
    if np.any(means<=0):return float('inf')
    return float(np.sum(means-counts*np.log(means)+gammaln(counts+1)))

def fit(data, allow_delta=False, maxiter=250):
    """Penalized Poisson profile with AR1 prior for latent phase.

    Hyperparameters rho, sigma are treated as independently known. They are NOT
    re-estimated in this version. This is a penalized likelihood/MAP statistic,
    and bootstrap critical values must be empirically estimated.
    """
    x=data['x'];c=data['counts'];dc=data['dark_counts'];t=len(x)
    cov=phase_covariance(t,data['rho'],data['sigma'])
    inv=np.linalg.inv(cov)
    e=data['exposure']
    k=5 if allow_delta else 4
    estimate_dark=max(.1,float(dc.mean()))
    mean_detector=c.mean(axis=(0,1))
    eta0=np.clip((sum(mean_detector)-2*estimate_dark)/e,.1,.95)
    initial=np.r_[eta0,.55,estimate_dark,.05,*([0.] if allow_delta else []),np.zeros(t)]
    bounds=[(.03,.99),(.03,.99),(.05,6.),(-np.pi,np.pi)]
    if allow_delta:bounds.append((-.7,.7))
    bounds.extend([(-1.2,1.2)]*t)
    def obj(p):
        eta,v,dark,beta=p[:4]
        delta=p[4] if allow_delta else 0.
        u=p[k:]
        mu=source_means(x,u,eta,v,dark,beta,delta,e)
        return poisson_nll(c,mu)+poisson_nll(dc,np.full(dc.shape,dark)) + .5*u@inv@u
    def jac(p):
        eta,v,dark,beta=p[:4];delta=p[4] if allow_delta else 0.;u=p[k:]
        theta=x[:,None]+u[:,None]+beta+np.array([0.,delta])[None,:]
        cs=np.cos(theta);sn=np.sin(theta)
        mu=source_means(x,u,eta,v,dark,beta,delta,e)
        w=1-c/mu
        plusminus=np.array([1.,-1.])
        partial_phase=e*eta*v/2*(-sn[:,:,None]*plusminus[None,None,:])
        grad_eta=np.sum(w * (e/2)*(1+v*cs[:,:,None]*plusminus[None,None,:]))
        grad_v=np.sum(w * (e*eta/2)*(cs[:,:,None]*plusminus[None,None,:]))
        grad_dark=np.sum(w)+np.sum(1-dc/dark)
        by_phase=np.sum(w*partial_phase,axis=2)
        grad_beta=np.sum(by_phase)
        grad_u=by_phase.sum(axis=1)+inv@u
        result=[grad_eta,grad_v,grad_dark,grad_beta]
        if allow_delta:result.append(np.sum(by_phase[:,1]))
        return np.r_[result,grad_u]
    res=minimize(obj,initial,method='L-BFGS-B',jac=jac,bounds=bounds,
                 options={'maxiter':maxiter,'ftol':1e-11,'gtol':1e-5})
    return {'objective':float(res.fun),'parameters':res.x,
            'success':bool(res.success),'message':str(res.message),'nit':int(res.nit)}

def profile_statistic(data):
    null=fit(data,False)
    alt=fit(data,True)
    return {'statistic':max(0.,2*(null['objective']-alt['objective'])),
            'null':null,'alternative':alt}

def parametric_bootstrap(data, replications=50, seed=182):
    """Generate from fitted H0, refit both H0 and H1 in EVERY replication."""
    if replications<10:raise ValueError('at least ten bootstrap replicates')
    observed=profile_statistic(data)
    params=observed['null']['parameters'];t=len(data['x'])
    eta,v,dark,beta=params[:4]
    rng=np.random.default_rng(seed)
    stats=[];converged=0
    for _ in range(replications):
        u=rng.multivariate_normal(np.zeros(t),phase_covariance(t,data['rho'],data['sigma']))
        mu=source_means(data['x'],u,eta,v,dark,beta,0.,data['exposure'])
        copy={**data,'counts':rng.poisson(mu),'dark_counts':rng.poisson(dark,size=(t,2))}
        trial=profile_statistic(copy)
        stats.append(trial['statistic'])
        converged+=int(trial['null']['success'] and trial['alternative']['success'])
    arr=np.array(stats)
    return {'observed':float(observed['statistic']),
            'bootstrap_95pct':float(np.quantile(arr,.95)),
            'empirical_p_plus_one':float((1+np.sum(arr>=observed['statistic']))/(1+replications)),
            'null_stats':arr.tolist(),'replications':replications,
            'replicates_both_optimized':converged,
            'observed_null_fit_converged':observed['null']['success'],
            'observed_alt_fit_converged':observed['alternative']['success']}

def group_offset_degeneracy(beta, ordinary_group_bias, identity_delta):
    return beta+ordinary_group_bias+identity_delta

def summary(replications=40):
    clean=simulate_data(seed=100,delta=0.)
    signal=simulate_data(seed=101,delta=.18)
    fit0=profile_statistic(clean);fit1=profile_statistic(signal)
    boot=parametric_bootstrap(clean,replications=replications,seed=102)
    return {'version':'v0.82','model':'paired Poisson test/calibration detector counts, AR1 latent phase',
       't':len(clean['x']),'n_per_setting_mean_exposure':clean['exposure'],
       'null_dataset_profile_stat':fit0['statistic'],
       'signal_dataset_profile_stat':fit1['statistic'],
       'null_bootstrap':boot,
       'known_hyperparameters':{'rho':clean['rho'],'innovation_sigma':clean['sigma']},
       'ordinary_test_group_bias_can_mimic_identity':True,
       'warning':'MAP/penalized profile; fixed AR1 hyperparameters; bootstrap re-fits nuisance and drift; not a QED prediction'}
