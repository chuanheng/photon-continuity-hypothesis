"""v0.84: raw Poisson quadrature counts, independent AR1 sensor calibration,
parametric bootstrap with sensor hyperparameter refitting and outer type-I audit.
Statistical toy example; not QED or photon identity evidence.
"""
import numpy as np
from scipy.linalg import solve_toeplitz

DEFAULT=dict(exposure=700.0,eta=0.72,visibility=0.8,dark=0.8,
             baseline=.18,rho=.78,sigma=.065,sensor_readout=.025)

def ar1_path(n,rho,sigma,rng):
    if not (-1<rho<1 and sigma>0 and n>1):raise ValueError('invalid AR1')
    a=np.empty(n);a[0]=rng.normal(0,sigma/np.sqrt(1-rho*rho))
    a[1:]=rng.normal(0,sigma,n-1)
    for i in range(1,n):a[i]+=rho*a[i-1]
    return a

def estimate_ar1_sensor(y,sensor_sd=.025):
    """Sensor noise variance corrected AR1 method-of-moments, not Kalman MLE."""
    y=np.asarray(y,float)
    if len(y)<5 or sensor_sd<=0:raise ValueError('invalid sensor data')
    z=y-y.mean();v=max(float(np.mean(z*z)-sensor_sd**2),1.e-5)
    lag=float(np.mean(z[:-1]*z[1:]))
    rho=float(np.clip(lag/v,-.94,.94))
    sigma=float(np.sqrt(max(v*(1-rho*rho),1.e-6)))
    return rho,sigma

def poisson_counts(u,rng,*,bias=0.,cfg=DEFAULT):
    """Raw [time,group(cal=0,test=1),quadrature,port] photon counts.
    u is differential test-minus-calibration drift, NOT common-mode drift.
    """
    n=len(u)
    theta=cfg['baseline']+np.column_stack([np.zeros(n),np.asarray(u)+bias])
    phase=theta[:,:,None]+np.array([0.,np.pi/2])[None,None,:]
    amp=cfg['exposure']*cfg['eta']/2
    plus=amp*(1+cfg['visibility']*np.cos(phase))+cfg['dark']
    minus=amp*(1-cfg['visibility']*np.cos(phase))+cfg['dark']
    return rng.poisson(np.stack([plus,minus],axis=-1))

def phase_differences(counts):
    c=np.asarray(counts,float)
    if c.ndim!=4 or c.shape[1:]!=(2,2,2):
        raise ValueError('expected time x group x quadrature x port')
    contrasts=c[...,0]-c[...,1]
    phases=np.arctan2(-contrasts[:,:,1],contrasts[:,:,0])
    return np.angle(np.exp(1j*(phases[:,1]-phases[:,0])))

def phase_readout_variance(cfg=DEFAULT):
    """Delta-method shot noise approx; assumes calibrated detector parameters."""
    amp=cfg['exposure']*cfg['eta']*cfg['visibility']
    return 2*(cfg['exposure']*cfg['eta']+2*cfg['dark'])/(amp*amp)

def gls_statistic(diffs,rho,sigma,cfg=DEFAULT):
    n=len(diffs)
    if n<2 or abs(rho)>=1 or sigma<=0:raise ValueError('invalid covariance')
    col=sigma*sigma/(1-rho*rho)*rho**np.arange(n)
    col[0]+=phase_readout_variance(cfg)
    w=solve_toeplitz((col,col),np.ones(n),check_finite=False)
    information=float(np.sum(w))
    estimate=float(w@diffs)/information
    return {'estimate':estimate,'se':float(np.sqrt(1/information)),
            'z':float(estimate*np.sqrt(information)),
            'stat':float(estimate*estimate*information)}

def generate_experiment(rng,scenario='stationary',n=24,cal_length=100,cfg=DEFAULT):
    rho,sigma=cfg['rho'],cfg['sigma']
    sensor=ar1_path(cal_length,rho,sigma,rng)+rng.normal(0,cfg['sensor_readout'],cal_length)
    if scenario=='stationary':
        drift=ar1_path(n,rho,sigma,rng);bias=0.
    elif scenario=='random_walk':
        drift=np.cumsum(rng.normal(0,.075,n));bias=0.
    elif scenario=='ordinary_group_bias':
        drift=ar1_path(n,rho,sigma,rng);bias=.22
    else:raise ValueError('scenario')
    return {'sensor':sensor,'counts':poisson_counts(drift,rng,bias=bias,cfg=cfg),
            'true_drift':drift,'ordinary_bias':bias}

def bootstrap_pvalue(experiment,rng,b=79,cfg=DEFAULT):
    """Refit AR1 rho/sigma on new independent sensor every inner replicate.
    GLS is on Gaussian-approximated phases extracted from Poisson raw counts,
    NOT the v0.83 Poisson latent MAP likelihood.
    """
    if b<9:raise ValueError('too few bootstrap replicates')
    rho,sigma=estimate_ar1_sensor(experiment['sensor'],cfg['sensor_readout'])
    diff=phase_differences(experiment['counts'])
    observed=gls_statistic(diff,rho,sigma,cfg)['stat']
    simulated=np.empty(b);hyper=np.empty((b,2))
    for j in range(b):
        sensor=ar1_path(len(experiment['sensor']),rho,sigma,rng)+rng.normal(0,cfg['sensor_readout'],len(experiment['sensor']))
        rho_j,sigma_j=estimate_ar1_sensor(sensor,cfg['sensor_readout'])
        hyper[j]=[rho_j,sigma_j]
        u=ar1_path(len(diff),rho,sigma,rng)
        counts=poisson_counts(u,rng,bias=0.,cfg=cfg)
        simulated[j]=gls_statistic(phase_differences(counts),rho_j,sigma_j,cfg)['stat']
    return {'stat':float(observed),
            'p':float((1+np.count_nonzero(simulated>=observed))/(b+1)),
            'estimated_rho':rho,'estimated_sigma':sigma,
            'bootstrap_count':b,'bootstrap_95pct_stat':float(np.quantile(simulated,.95)),
            'hyperparameter_refits':len(hyper)}

def audit_outer(scenarios=('stationary','random_walk','ordinary_group_bias'),
                outer=120,inner=79,seed=8401,cfg=DEFAULT):
    if outer<1 or inner<9:raise ValueError('size')
    rng=np.random.default_rng(seed);result={}
    for scenario in scenarios:
        p=[];stat=[];rho=[];sig=[]
        for _ in range(outer):
            exp=generate_experiment(rng,scenario,cfg=cfg)
            v=bootstrap_pvalue(exp,rng,b=inner,cfg=cfg)
            p.append(v['p']);stat.append(v['stat'])
            rho.append(v['estimated_rho']);sig.append(v['estimated_sigma'])
        nrej=sum(x<=.05 for x in p);rate=nrej/outer
        result[scenario]={
            'false_positive_rate_if_null_held':rate,
            'rejections_at_nominal_5pct':nrej,'outer_simulations':outer,
            'inner_bootstrap_each':inner,
            'binomial_monte_carlo_se':float(np.sqrt(rate*(1-rate)/outer)),
            'mean_stat':float(np.mean(stat)),
            'mean_estimated_rho':float(np.mean(rho)),
            'mean_estimated_sigma':float(np.mean(sig)), 'pvalues':p}
    return {'version':'v0.84','parameters':dict(cfg),
            'scenario_results':result,
            'notes':['Random walk and ordinary group bias violate the fitted stationary zero-bias null; rejection is a misspecification alarm, not an identified photon identity effect.',
             'Photon counts independent Poisson; Gaussian phase GLS approximate; detector efficiency/visibility/dark and sensor readout SD treated known.',
             'AR1 parameters estimated on independent sensor and refitted every inner bootstrap. No QED identity prediction.']}
