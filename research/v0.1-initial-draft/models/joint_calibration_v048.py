"""Standard Poisson toy model; not a physical derivation of photon identity."""
from dataclasses import dataclass
import math, random

@dataclass(frozen=True)
class Design:
    s: tuple=(10.,8.,6.,4.)
    b: tuple=(1.,1.,1.,1.)
    h: tuple=(0.,0.,3.,0.)
    t: float=1.
    k_eta: float=100.
    k_beta: float=100.
    def validate(self):
        if not (len(self.s)==len(self.b)==len(self.h)>0): raise ValueError('templates must have equal nonzero length')
        if any(not math.isfinite(x) or x<0 for x in self.s+self.b+self.h): raise ValueError('templates must be finite and nonnegative')
        if any(not math.isfinite(x) or x<0 for x in (self.t,self.k_eta,self.k_beta)): raise ValueError('exposures must be finite and nonnegative')
        if not any(self.s) or not any(self.b): raise ValueError('signal and background templates cannot both be uninformative')

@dataclass(frozen=True)
class Data:
    science: tuple
    cal_eta: float
    cal_beta: float

def means(d:Design, eta=1., beta=1., eps=0.):
    d.validate()
    if min(eta,beta,eps)<0: raise ValueError('parameters must be nonnegative')
    return tuple(d.t*(eta*s+beta*b+eps*h) for s,b,h in zip(d.s,d.b,d.h))

def loglike(d:Design, y:Data, eta,beta,eps):
    if min(eta,beta,eps)<0: return -math.inf
    mu=means(d,eta,beta,eps)
    def lp(n,m):
        if n<0 or int(n)!=n or m<0: return -math.inf
        if m==0: return 0. if n==0 else -math.inf
        return n*math.log(m)-m-math.lgamma(n+1)
    vals=[lp(n,m) for n,m in zip(y.science,mu)]
    vals += [lp(y.cal_eta,d.k_eta*eta),lp(y.cal_beta,d.k_beta*beta)]
    return sum(vals) if all(math.isfinite(v) for v in vals) else -math.inf

def fit(d,y,alt=True):
    """Constrained derivative-free coordinate search; reproducible, no external dependencies."""
    # Coarse-to-fine coordinate pattern search from several starts helps boundary cases.
    best=(-math.inf,(1.,1.,0.))
    for start in ((1.,1.,0.),(.1,.1,0.),(2.,2.,1.)):
        x=list(start); x[2]=0. if not alt else x[2]
        score=loglike(d,y,*x)
        step=[.5,.5,.5 if alt else 0.]
        for _ in range(100):
            changed=False
            for j in range(3 if alt else 2):
                for sign in (-1,1):
                    z=x.copy(); z[j]=max(0.,z[j]+sign*step[j]); sc=loglike(d,y,*z)
                    if sc>score+1e-12: x,score,changed=z,sc,True
            if not changed: step=[v*.5 for v in step]
            if max(step)<2e-6: break
        if score>best[0]: best=(score,tuple(x))
    return best[0], best[1]

def q_stat(d,y):
    l0,_=fit(d,y,False); l1,_=fit(d,y,True)
    return max(0.,2*(l1-l0))

def poisson(rng,mu):
    if mu<0: raise ValueError('negative mean')
    if mu==0: return 0
    # Knuth exact sampler; model sizes here are moderate.
    limit=math.exp(-mu); k=0; p=1.
    while p>limit: k+=1; p*=rng.random()
    return k-1

def generate(d,eta=1.,beta=1.,eps=0.,cal_bias_eta=1.,cal_bias_beta=1.,seed=None):
    rng=random.Random(seed)
    return Data(tuple(poisson(rng,m) for m in means(d,eta,beta,eps)),
                poisson(rng,d.k_eta*eta*cal_bias_eta),poisson(rng,d.k_beta*beta*cal_bias_beta))

def bootstrap(d, n_null=199, n_alt=199, eps=1., alpha=.05, seed=20261112, calibration_bias=(1.,1.), evaluation_bias=(1.,1.)):
    """Split deterministic streams; empirical upper-tail critical rank with +1 correction."""
    if n_null<20 or n_alt<1 or not 0<alpha<1: raise ValueError('invalid simulation settings')
    master=random.Random(seed); seeds=[master.randrange(2**32) for _ in range(n_null+n_alt)]
    qcal=[q_stat(d,generate(d,cal_bias_eta=calibration_bias[0],cal_bias_beta=calibration_bias[1],seed=s)) for s in seeds[:n_null]]
    q0=[q_stat(d,generate(d,cal_bias_eta=evaluation_bias[0],cal_bias_beta=evaluation_bias[1],seed=s)) for s in seeds[:n_null]]
    # Inclusive empirical threshold; ties are rejected only when strictly above threshold.
    q0s=sorted(qcal); rank=max(0,min(n_null-1,math.ceil((1-alpha)*(n_null+1))-1)); threshold=q0s[rank]
    q1=[q_stat(d,generate(d,eps=eps,seed=s)) for s in seeds[n_null:]]
    return {'threshold':threshold,'fpr':sum(q>threshold for q in q0)/n_null,'power':sum(q>threshold for q in q1)/n_alt,'n_null':n_null,'n_alt':n_alt,'seed':seed,'q0':q0,'q1':q1}

def wilson(k,n,z=1.959963984540054):
    if n<=0: raise ValueError('n must be positive')
    p=k/n; den=1+z*z/n; mid=(p+z*z/(2*n))/den; half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return (0. if k==0 else max(0.,mid-half),1. if k==n else min(1.,mid+half))
