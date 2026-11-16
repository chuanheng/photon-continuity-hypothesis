"""v0.81: AR(1) environment drift and GLS/parametric bootstrap.

Phase records are a Gaussian approximation to fitted optical phase; NOT raw
photon counts, NOT QED and NOT evidence of historical photon identity.
"""
import numpy as np
from scipy.stats import chi2

def ar1_cov(n,rho,sigma_innovation):
    if not isinstance(n,int) or n<1:raise ValueError('positive integer n required')
    if abs(rho)>=1 or sigma_innovation<0:raise ValueError('invalid AR(1)')
    indices=np.arange(n)
    return sigma_innovation**2/(1-rho**2)*rho**np.abs(indices[:,None]-indices[None,:])

def residual_cov(n,rho,sigma_differential,sigma_readout):
    if sigma_readout<0:raise ValueError('invalid readout')
    return ar1_cov(n,rho,sigma_differential)+sigma_readout**2*np.eye(n)

def gls_weights(cov):
    cov=np.asarray(cov,float)
    if cov.ndim!=2 or cov.shape[0]!=cov.shape[1] or cov.shape[0]<1:
        raise ValueError('covariance must be square')
    one=np.ones(cov.shape[0]);precision_one=np.linalg.solve(cov,one)
    denominator=one@precision_one
    if denominator<=0:raise ValueError('non-SPD')
    return precision_one/denominator,1/denominator

def score(residual,cov):
    residual=np.asarray(residual,float)
    w,var=gls_weights(cov)
    if residual.shape!=(len(w),):raise ValueError('residual shape mismatch')
    estimate=float(w@residual)
    return {'delta_hat':estimate,'standard_error':float(np.sqrt(var)),
            'z':float(estimate/np.sqrt(var)),'llr':float(estimate**2/var)}

def gaussian_phase_records(n,delta=0,rho=.92,sigma_differential=.09,
                           sigma_readout=.05,seed=81):
    cov=residual_cov(n,rho,sigma_differential,sigma_readout)
    rng=np.random.default_rng(seed)
    return rng.multivariate_normal(np.full(n,delta),cov),cov

def bootstrap_threshold(cov,B=1200,alpha=.05,seed=812):
    """Null bootstrap assuming KNOWN covariance; no nuisance re-fitting."""
    if B<50 or not 0<alpha<1:raise ValueError('invalid bootstrap settings')
    rng=np.random.default_rng(seed)
    simulated=rng.multivariate_normal(np.zeros(len(cov)),cov,size=B)
    w,var=gls_weights(cov)
    stat=(simulated@w)**2/var
    return float(np.quantile(stat,1-alpha)),stat

def phase_fringe_prob(phi,visibility=.8,eta=.65):
    if not(0<=visibility<=1 and 0<=eta<=1):raise ValueError('ranges')
    return np.array([1-eta,eta*(1+visibility*np.cos(phi))/2,
                     eta*(1-visibility*np.cos(phi))/2])

def confounding_with_group_bias(delta,ordinary_bias):
    return delta+ordinary_bias

def monte_carlo(n=80,n_sim=400,rho=.92,sigma_differential=.09,
                sigma_readout=.05,alpha=.05,seed=814,delta=0):
    if n_sim<1:raise ValueError('simulations')
    cov=residual_cov(n,rho,sigma_differential,sigma_readout)
    rng=np.random.default_rng(seed)
    simulated=rng.multivariate_normal(np.full(n,delta),cov,size=n_sim)
    w,var=gls_weights(cov)
    correct_z=(simulated@w)/np.sqrt(var)
    naive_z=simulated.mean(axis=1)/(sigma_readout/np.sqrt(n))
    cutoff=chi2.ppf(1-alpha,1)
    return {'naive_rejection_rate':float(np.mean(naive_z**2>cutoff)),
            'correlated_rejection_rate':float(np.mean(correct_z**2>cutoff)),
            'analytic_threshold':float(cutoff),
            'corrected_standard_error':float(np.sqrt(var)),
            'naive_standard_error':float(sigma_readout/np.sqrt(n)),
            'corrected_mean_z':float(correct_z.mean())}

def summary():
    n=80;rho=.92;sig_d=.09;sig_r=.05
    records,cov=gaussian_phase_records(n,delta=0,seed=81,rho=rho,
        sigma_differential=sig_d,sigma_readout=sig_r)
    boot,_=bootstrap_threshold(cov,B=1600,seed=812)
    null=monte_carlo(n=n,n_sim=400,seed=814,rho=rho,
        sigma_differential=sig_d,sigma_readout=sig_r)
    alternative=monte_carlo(n=n,n_sim=400,seed=814,rho=rho,
        sigma_differential=sig_d,sigma_readout=sig_r,delta=.15)
    return {'version':'v0.81','n':n,'rho':rho,
        'differential_ar1_innovation_sd':sig_d,'paired_readout_sd':sig_r,
        'null_rejection':null,'alternative_rejection':alternative,
        'bootstrap_null_threshold_95pct':boot,
        'chi_squared_1_95pct':float(chi2.ppf(.95,1)),
        'single_null_sequence':score(records,cov),
        'uncalibrated_group_bias_identifiability':'delta and ordinary group bias enter via their sum',
        'caveat':'Known covariance; fitted interferometric phase approximated as Gaussian, not raw photon counts.'}
