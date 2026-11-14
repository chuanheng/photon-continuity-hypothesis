"""v0.83: independently estimated AR(1) hyperparameters and refit bootstrap.
Finite statistical research model, not QED. The separate calibration record is
noisy observations of a stationary AR(1) phase. The photon-data fit is the
penalized v0.82 Poisson/MAP fit conditioned on estimated hyperparameters.
"""
from __future__ import annotations
import numpy as np
from scipy.optimize import minimize
from models.count_hierarchy_v082 import (
    simulate_data, source_means, profile_statistic, phase_covariance,
)

def simulate_calibration(length=120, rho=.8, sigma=.12, readout_sd=.03, seed=123):
    if length < 4 or abs(rho) >= 1 or sigma <= 0 or readout_sd <= 0:
        raise ValueError('invalid calibration settings')
    rng = np.random.default_rng(seed)
    latent = np.empty(length)
    latent[0] = rng.normal(0, sigma / np.sqrt(1-rho*rho))
    for i in range(1, length):
        latent[i] = rho*latent[i-1] + rng.normal(0, sigma)
    return latent + rng.normal(0, readout_sd, length), latent

def kalman_nll(record, rho, sigma, readout_sd=.03):
    """Exact Gaussian stationary AR1+known-sensor-noise log likelihood."""
    y = np.asarray(record, float)
    if y.ndim != 1 or len(y) < 4 or not (abs(rho)<1 and sigma>0 and readout_sd>0):
        raise ValueError('invalid Kalman input')
    mean = 0.
    variance = sigma*sigma/(1-rho*rho)
    nll=0.
    for obs in y:
        v=variance+readout_sd**2
        innovation=obs-mean
        nll += .5*(np.log(2*np.pi*v)+innovation*innovation/v)
        gain=variance/v
        mean=mean+gain*innovation
        variance=(1-gain)*variance
        mean=rho*mean
        variance=rho*rho*variance+sigma*sigma
    return float(nll)

def estimate_hyperparameters(record, readout_sd=.03):
    y=np.asarray(record,float)
    if y.ndim!=1 or len(y)<4 or readout_sd<=0:raise ValueError('calibration record')
    sd=max(.02, float(np.std(y)))
    starts=[(.2,min(.3,sd)),(.75,min(.2,sd)),(.94,min(.14,sd))]
    solutions=[]
    for rho0,sigma0 in starts:
        r=minimize(lambda p: kalman_nll(y,p[0],p[1],readout_sd),
                   [rho0,sigma0],method='L-BFGS-B',
                   bounds=[(-.95,.97),(.008,.5)],
                   options={'maxiter':150,'ftol':1e-12})
        solutions.append(r)
    best=min(solutions,key=lambda r:r.fun)
    return {'rho':float(best.x[0]),'sigma':float(best.x[1]),
            'nll':float(best.fun),'success':bool(best.success)}

def conditioned_photon_data(data, rho, sigma):
    return {**data,'rho':float(rho),'sigma':float(sigma)}

def bootstrap_with_refit(photon_data, calibration,
                         replications=24,seed=500,readout_sd=.03):
    """Each replicate refits rho/sigma on new independent sensor observations,
    then refits H0 and H1 on new Poisson detector counts.
    """
    if replications<10:raise ValueError('at least 10 replicates')
    measured=estimate_hyperparameters(calibration,readout_sd)
    if not measured['success']:raise RuntimeError('calibration fit failed')
    data=conditioned_photon_data(photon_data,measured['rho'],measured['sigma'])
    observed=profile_statistic(data)
    if not (observed['null']['success'] and observed['alternative']['success']):
        raise RuntimeError('observed photon fit failed')
    eta,v,dark,beta=observed['null']['parameters'][:4]
    rng=np.random.default_rng(seed)
    stats=[];hyper=[];both_ok=0
    for _ in range(replications):
        cal_seed=int(rng.integers(1,2**31-1))
        cal,_=simulate_calibration(len(calibration),rho=measured['rho'],
                                   sigma=measured['sigma'],
                                   readout_sd=readout_sd,seed=cal_seed)
        est=estimate_hyperparameters(cal,readout_sd)
        if not est['success']:raise RuntimeError('bootstrap hyperparameter refit failed')
        hyper.append([est['rho'],est['sigma']])
        t=len(data['x'])
        latent=rng.multivariate_normal(np.zeros(t),
                  phase_covariance(t,measured['rho'],measured['sigma']))
        means=source_means(data['x'],latent,eta,v,dark,beta,0.,data['exposure'])
        replica=conditioned_photon_data({**data,'counts':rng.poisson(means),
                                         'dark_counts':rng.poisson(dark,size=(t,2))},
                                         est['rho'],est['sigma'])
        fit=profile_statistic(replica)
        both_ok+=int(fit['null']['success'] and fit['alternative']['success'])
        stats.append(fit['statistic'])
    arr=np.asarray(stats,float)
    return {'observed':observed['statistic'],
            'null_fit':{'eta':eta,'visibility':v,'dark':dark,'beta':beta},
            'calibration_fit':measured,
            'null_bootstrap_stats':arr.tolist(),
            'refitted_hyperparameters':hyper,
            'critical_value_95':float(np.quantile(arr,.95)),
            'p_plus_one':float((1+np.sum(arr>=observed['statistic']))/(replications+1)),
            'replications':replications,'both_photon_fits_converged':both_ok,
            'all_calibration_fits_converged':True}

def group_bias_equivalent(delta, ordinary_test_bias):
    return float(delta+ordinary_test_bias)

def random_walk(n, step_sd, seed=12):
    if n<1 or step_sd<0:raise ValueError('invalid walk')
    return np.random.default_rng(seed).normal(0,step_sd,n).cumsum()

def covariance_model_mismatch_example(n=12,seed=91):
    from models.count_hierarchy_v082 import DEFAULT
    data=simulate_data(t=n,delta=0.,seed=seed)
    u=random_walk(n,.20,seed=seed+1)
    ordinary_group_bias=.23
    p=DEFAULT
    test_mu=source_means(data['x'],u,p['eta'],p['visibility'],p['dark'],
                         p['beta'],ordinary_group_bias,p['exposure'])
    rng=np.random.default_rng(seed+2)
    data['counts']=rng.poisson(test_mu)
    return data, ordinary_group_bias
