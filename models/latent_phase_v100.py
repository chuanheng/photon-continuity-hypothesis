"""v1.00: Gaussian latent phase smoothing, Monte Carlo marginalized HOM likelihood.
This GitHub version is separately authored; exact tested local code is in ZIP.
KNOWN: Fock/source contamination, PNR response, detector and electronics
parameters, walk/readout scales and phase bias. No photon identity claim.
"""
from dataclasses import dataclass
import numpy as np
from scipy.linalg import cho_solve,solve_triangular
from scipy.special import logsumexp
from models.fock_calibration_v096 import optical_probs
from models.mixed_hom_v094 import Config

@dataclass(frozen=True)
class Setup:
    intrinsic:float=.72
    steps:int=40
    walk_sd:float=.095
    read_sd:float=.15
    read_bias:float=0.
    near_shots:int=25000
    intercept:float=0.
    slope:float=0.
    def __post_init__(self):
        if not(0<self.intrinsic<1 and self.steps>=3 and self.walk_sd>0 and self.read_sd>0 and
               self.near_shots>0 and 0<self.intercept<1 and self.slope>0 and
               0<self.intercept-self.slope<1):
            raise ValueError('invalid setting')

def optical_calibration():
    p=Config()
    c0=float(optical_probs(p,.065,.014,0)[0])
    c1=float(optical_probs(p,.065,.014,1)[0])
    return c0,c0-c1

def default_setup():
    a,b=optical_calibration()
    return Setup(intercept=a,slope=b)

def generate(seed=1001,repeats=1,setup=None):
    setup=default_setup() if setup is None else setup
    if repeats<1:raise ValueError('repeats')
    r=np.random.default_rng(seed)
    u=np.r_[0.,np.cumsum(r.normal(0,setup.walk_sd,setup.steps-1))]
    y=u[:,None]+setup.read_bias+r.normal(0,setup.read_sd,(setup.steps,repeats))
    A=float(np.mean(np.exp(-abs(u))))
    p=setup.intercept-setup.slope*setup.intrinsic*A
    return {'true_u':u,'y':y,'A_true':A,'bar_true':A*setup.intrinsic,
      'near_count':int(r.binomial(setup.near_shots,p)),
      'near_probability':p,'repeats':repeats,'seed':seed}

def smooth(y,setup=None):
    setup=default_setup() if setup is None else setup
    y=np.asarray(y,float)
    if y.ndim!=2 or y.shape[0]!=setup.steps or y.shape[1]<1 or not np.isfinite(y).all():
        raise ValueError('sensor readings require steps x repeated samples')
    d=setup.steps-1;k=y.shape[1];q=setup.walk_sd**2;v=setup.read_sd**2
    Q=np.diag(np.r_[np.full(d-1,2.),1.])/q+np.eye(d)*k/v
    ix=np.arange(d-1);Q[ix,ix+1]=-1/q;Q[ix+1,ix]=-1/q
    L=np.linalg.cholesky(Q)
    info=np.sum(y[1:]-setup.read_bias,axis=1)/v
    mean=cho_solve((L,True),info)
    covariance=cho_solve((L,True),np.eye(d))
    return {'mean':np.r_[0.,mean],'variance':np.r_[0.,np.diag(covariance)],
       'cov_unknown':covariance,'chol_precision':L,
       'known_initial_phase':0.,'num_reads':k}

def sample_paths(smoother,draws=700,seed=55):
    if draws<10:raise ValueError('draws')
    m=np.asarray(smoother['mean'])
    rng=np.random.default_rng(seed)
    z=rng.normal(size=(len(m)-1,draws))
    dev=solve_triangular(smoother['chol_precision'].T,z,lower=False)
    result=np.zeros((draws,len(m)))
    result[:,1:]=m[1:]+dev.T
    return result

def attenuation(paths):
    p=np.asarray(paths,float)
    if p.ndim!=2 or p.shape[1]<2:raise ValueError('bad paths')
    return np.mean(np.exp(-abs(p)),axis=1)

def posterior_grid(n,shots,A,setup,grid=None):
    grid=np.linspace(.001,.999,401) if grid is None else np.asarray(grid)
    A=np.asarray(A,float)
    if len(A)<10 or np.any((A<=0)|(A>1)) or not 0<=n<=shots:raise ValueError('inputs')
    p=setup.intercept-setup.slope*grid[:,None]*A[None,:]
    if np.any((p<=0)|(p>=1)):raise ValueError('probabilities')
    ll=n*np.log(p)+(shots-n)*np.log1p(-p)
    lm=logsumexp(ll,axis=1)-np.log(len(A))
    w=np.exp(lm-logsumexp(lm))
    cdf=np.cumsum(w)
    qs=np.interp([.025,.5,.975],cdf,grid)
    return {'mean':float(np.sum(w*grid)), 'median':float(qs[1]),
            'ci95':[float(qs[0]),float(qs[2])],'grid':grid,'weight':w}

def infer(rec,setup=None,draws=700,seed=0):
    setup=default_setup() if setup is None else setup
    s=smooth(rec['y'],setup)
    A=attenuation(sample_paths(s,draws,seed))
    plug=float(np.mean(np.exp(-abs(s['mean']))))
    old=posterior_grid(rec['near_count'],setup.near_shots,np.full(draws,plug),setup)
    lat=posterior_grid(rec['near_count'],setup.near_shots,A,setup)
    return {'plugin':old,'latent':lat,
      'posterior_A_mean':float(A.mean()),'posterior_A_sd':float(A.std(ddof=1)),
      'smoother':s,'attenuation_draws':A}

def audit(outer=100,repeats=(1,2,20),draws=700,seed=100000):
    if outer<2 or draws<10:raise ValueError('sizes')
    setup=default_setup();data={}
    for k in repeats:
        rows=[]
        for i in range(outer):
            rec=generate(seed+1009*i,k,setup)
            fit=infer(rec,setup,draws,seed+100000+k*1000+i)
            rows.append({'true_A':rec['A_true'],
             'plugin_mean':fit['plugin']['mean'],'latent_mean':fit['latent']['mean'],
             'plugin_ci95':fit['plugin']['ci95'],'latent_ci95':fit['latent']['ci95'],
             'plugin_covered':fit['plugin']['ci95'][0]<=setup.intrinsic<=fit['plugin']['ci95'][1],
             'latent_covered':fit['latent']['ci95'][0]<=setup.intrinsic<=fit['latent']['ci95'][1]})
        x=np.asarray([v['plugin_mean'] for v in rows]);y=np.asarray([v['latent_mean'] for v in rows])
        data[str(k)]={'runs':len(rows),'plugin_covered':sum(z['plugin_covered'] for z in rows),
         'latent_covered':sum(z['latent_covered'] for z in rows),
         'plugin_mean':float(x.mean()),'latent_mean':float(y.mean()),
         'plugin_rmse':float(np.sqrt(np.mean((x-setup.intrinsic)**2))),
         'latent_rmse':float(np.sqrt(np.mean((y-setup.intrinsic)**2))),
         'mean_plugin_width':float(np.mean([z['plugin_ci95'][1]-z['plugin_ci95'][0] for z in rows])),
         'mean_latent_width':float(np.mean([z['latent_ci95'][1]-z['latent_ci95'][0] for z in rows])),
         'rows':rows}
    return {'version':'v1.00','truth_M0':setup.intrinsic,'repeats':list(repeats),
      'calibration_nuisance':'known','prior':'Uniform(0,1)',
      'results':data,'outer':outer,'draws':draws,'seed':seed,
      'novel_photon_identity_prediction':False}
