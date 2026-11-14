"""v0.85 — Fair ordinary-memory composite null and operational equivalence.
Statistical toy model, not QED or a claim about permanent photon identity.
"""
import numpy as np
from scipy.special import gammaln

DEFAULT = {'exposure': 200.0, 'eta': 0.72, 'visibility': 0.8,
           'dark': 0.8, 'baseline': 0.18}

def latent_drift(n, kind='ar1', seed=85, rho=.78, sigma=.065):
    if n < 2 or sigma <= 0 or abs(rho) >= 1:
        raise ValueError('invalid latent process parameters')
    rng = np.random.default_rng(seed)
    if kind == 'ar1':
        v = np.empty(n)
        v[0] = rng.normal(0, sigma / np.sqrt(1-rho*rho))
        for k in range(1, n):
            v[k] = rho * v[k-1] + rng.normal(0, sigma)
    elif kind == 'random_walk':
        v = rng.normal(0, sigma, n).cumsum()
    elif kind == 'piecewise':
        v = rng.normal(0, sigma, n)
        v[n//2:] += .18
    else:
        raise ValueError('unknown drift model')
    return v

def poisson_means(u, ordinary_bias=0., identity_delta=0.,
                  signature=None, cfg=None):
    """Array shape (time, group, quadrature, port).
    group=0 calibration, group=1 test. Normal bias and delta share phase
    for constant signature. Nonconstant signature is hypothetical, not a
    physically established identity intervention.
    """
    cfg = dict(DEFAULT if cfg is None else cfg)
    u = np.asarray(u, dtype=float)
    n = len(u)
    if u.ndim != 1 or n < 2:
        raise ValueError('drift should be 1D with n >=2')
    if signature is None:
        signature = np.ones(n)
    signature = np.asarray(signature, dtype=float)
    if signature.shape != (n,):
        raise ValueError('signature size mismatch')
    eta, vis, dark, exposure = (cfg[k] for k in ('eta','visibility','dark','exposure'))
    if not (0 < eta < 1 and 0 <= vis <= 1 and dark >= 0 and exposure > 0):
        raise ValueError('nonphysical detector values')
    phase = cfg['baseline'] + np.column_stack([np.zeros(n),u+ordinary_bias+identity_delta*signature])
    theta = phase[:,:,None] + np.array([0.,np.pi/2])[None,None,:]
    a = exposure * eta / 2
    c = a * vis * np.cos(theta)
    return np.stack([a+c+dark,a-c+dark],axis=-1)

def sample_counts(mu, seed=85):
    return np.random.default_rng(seed).poisson(mu)

def poisson_log_likelihood(counts, means):
    counts = np.asarray(counts)
    means = np.asarray(means)
    if counts.shape != means.shape or np.any(means <= 0):
        raise ValueError('invalid count likelihood')
    return float(np.sum(counts*np.log(means)-means-gammaln(counts+1)))

def exact_null_relabel(u,b,delta,signature=None):
    """For constant signature, null b'=b+delta matches the identity model."""
    if signature is not None and not np.allclose(signature,signature[0]):
        raise ValueError('nonconstant signature cannot be relabeled as constant bias')
    shift = delta if signature is None else delta*float(signature[0])
    return {'latent_drift':np.array(u,float,copy=True),
            'ordinary_bias':b+shift,'identity_delta':0.}

def poisson_kl(means_p,means_q):
    """KL of independent Poisson distributions (expected log-LR)."""
    p,q=np.asarray(means_p,float),np.asarray(means_q,float)
    if p.shape!=q.shape or np.any(p<=0) or np.any(q<=0):
        raise ValueError('strict positive means required')
    return float(np.sum(p*np.log(p/q)+q-p))

def fisher_bias_delta(u,b,delta,cfg=None):
    """Fisher 2x2 block for (ordinary group bias b, identity delta)."""
    cfg = dict(DEFAULT if cfg is None else cfg)
    u=np.asarray(u,float)
    phi = cfg['baseline']+u+b+delta
    phases=phi[:,None]+np.array([0,np.pi/2])[None,:]
    scale=cfg['exposure']*cfg['eta']*cfg['visibility']/2
    plus=cfg['exposure']*cfg['eta']/2+cfg['dark']+scale*np.cos(phases)
    minus=cfg['exposure']*cfg['eta']/2+cfg['dark']-scale*np.cos(phases)
    grad=-scale*np.sin(phases)
    info=float(np.sum(grad**2*(1/plus+1/minus)))
    return info*np.ones((2,2))

def calibrated_fisher(u,b,delta,bias_calibration_sd,cfg=None):
    if bias_calibration_sd<=0:raise ValueError('positive calibration SD required')
    f=fisher_bias_delta(u,b,delta,cfg)
    f[0,0]+=1/bias_calibration_sd**2
    return f

def independent_bias_calibration(b,sd=.05,seed=86):
    if sd<=0:raise ValueError('sd')
    return float(np.random.default_rng(seed).normal(b,sd))

def nuisance_design(n,signature=None,allow_time_varying_bias=False):
    if n<2:raise ValueError('n')
    s=np.ones(n) if signature is None else np.asarray(signature,float)
    if s.shape!=(n,):raise ValueError('signature')
    cols=[np.ones(n),s]
    if allow_time_varying_bias:cols += [np.eye(n)[:,i] for i in range(n)]
    return np.column_stack(cols)

def summary():
    n=24;u=latent_drift(n,'ar1');b=.11;delta=.20
    out={'version':'v0.85','n_times':n,'bias':b,
         'hypothetical_identity_delta':delta,'per_process':{},
         'matched_sample_log_likelihood_diff':{},'poisson_kl':{},
         'constant_signature_rank':int(np.linalg.matrix_rank(nuisance_design(n))),
         'varying_signature_rank':int(np.linalg.matrix_rank(nuisance_design(n,np.linspace(-1,1,n)))),
         'varying_signature_with_free_time_bias_rank':int(np.linalg.matrix_rank(nuisance_design(n,np.linspace(-1,1,n),True))),
         'calibrated_bias_delta_fisher_eigs':np.linalg.eigvalsh(calibrated_fisher(u,b,delta,.05)).tolist(),
         'uncalibrated_bias_delta_fisher_eigs':np.linalg.eigvalsh(fisher_bias_delta(u,b,delta)).tolist(),
         'model_status':'ordinary composite null exactly absorbs constant identity phase; no QED identity prediction'}
    for i,kind in enumerate(('ar1','random_walk','piecewise')):
        uk=latent_drift(n,kind,seed=85+i)
        p=poisson_means(uk,b,delta)
        theta=exact_null_relabel(uk,b,delta)
        q=poisson_means(theta['latent_drift'],theta['ordinary_bias'],0)
        sample=sample_counts(p,seed=100+i)
        out['per_process'][kind]={'max_abs_mean_diff':float(np.max(np.abs(p-q))),
                                  'n_observations':int(sample.size)}
        out['matched_sample_log_likelihood_diff'][kind]=poisson_log_likelihood(sample,p)-poisson_log_likelihood(sample,q)
        out['poisson_kl'][kind]=poisson_kl(p,q)
    return out
