"""v1.02 independent GitHub companion: continuous sensor MLE + decomposed
HOM calibration. Exact 37-test executed source is in local v1.02 ZIP.
No claim of complete joint Bayesian hyperparameter inference.
"""
from dataclasses import dataclass
import numpy as np
from scipy.linalg import solve_triangular
from scipy.optimize import minimize
from scipy.special import logsumexp
from models.mixed_hom_v094 import Config
from models.fock_calibration_v096 import optical_probs as optical_probabilities

@dataclass(frozen=True)
class Setup:
    T:int=40
    M:float=.72
    walk_sd:float=.095
    read_sd:float=.15
    bias:float=.015
    repeats:int=3
    zero_refs:int=100
    shots:int=25000
    ref_shots:int=30000
    pnr_standards:int=10000
    source_shots:int=40000

def response_confusion(miss_triplet=.20,miss_pair=.025):
    if not (0<=miss_triplet<.5 and 0<=miss_pair<.5):raise ValueError('confusion')
    c=np.eye(5)
    c[0,0]=1-miss_pair;c[0,4]=miss_pair
    c[4,0]=miss_triplet;c[4,4]=1-miss_triplet
    return c

def forward(M,A,p,f,q):
    return optical_probabilities(p,f,q,M*A)

def simulate(seed=10201,s=Setup()):
    rng=np.random.default_rng(seed)
    u=np.r_[0.,np.cumsum(rng.normal(0,s.walk_sd,s.T-1))]
    y=u[:,None]+s.bias+rng.normal(0,s.read_sd,(s.T,s.repeats))
    z=s.bias+rng.normal(0,s.read_sd,s.zero_refs)
    A=np.mean(np.exp(-abs(u)))
    p=Config();f=.065;q=.014;c=response_confusion()
    near,far=forward(s.M,A,p,f,q)
    w=np.array([p.w11-f,p.w20,p.w02,p.w00,f])
    source_true=rng.multinomial(s.source_shots,w)
    seen=np.zeros(5,int)
    for i,n in enumerate(source_true):seen+=rng.multinomial(int(n),c[i])
    known0=rng.multinomial(s.pnr_standards,c[0])
    known4=rng.multinomial(s.pnr_standards,c[4])
    dark=rng.binomial(s.ref_shots,[p.dark_a,p.dark_b])
    one=rng.binomial(s.ref_shots,[1-(1-e)*(1-d)
        for e,d in ((p.eta_a,p.dark_a),(p.eta_b,p.dark_b))])
    bg=p.dark_a*p.dark_b+q*(1-p.dark_a*p.dark_b)
    triggered=int(rng.binomial(s.ref_shots,bg))
    counts=rng.binomial(s.shots,[near,far])
    return dict(y=y,z=z,near=int(counts[0]),far=int(counts[1]),
         source=seen,ref0=known0,ref4=known4,dark=dark,one=one,
         triggered=triggered,truth_A=float(A),truth_M=s.M)

def sensor_nll(x,y,z):
    sw,sr=np.exp(x[:2]);b=x[2];T,k=y.shape;v=sr*sr
    K=sw*sw*np.minimum.outer(np.arange(T),np.arange(T))+np.eye(T)*(v/k)
    L=np.linalg.cholesky(K)
    means=y.mean(axis=1)
    h=solve_triangular(L,means-b,lower=True)
    SSE=np.sum((y-means[:,None])**2)
    return float(.5*(T*np.log(2*np.pi)+2*np.log(np.diag(L)).sum()+h@h
      +T*(k-1)*np.log(2*np.pi*v)+SSE/v
      +len(z)*np.log(2*np.pi*v)+np.sum((z-b)**2)/v))

def fit_sensor(y,z):
    start=[np.log(.1),np.log(max(np.std(z),.06)),float(np.mean(z))]
    bounds=[(np.log(.015),np.log(.5)),(np.log(.025),np.log(.55)),(-.3,.3)]
    f=minimize(sensor_nll,start,args=(y,z),method='L-BFGS-B',
               bounds=bounds,options={'maxiter':140})
    if not np.isfinite(f.fun):raise RuntimeError('optimization failed')
    return {'walk_sd':float(np.exp(f.x[0])),'read_sd':float(np.exp(f.x[1])),
            'bias':float(f.x[2])}

def phase_draws(y,hyper,draws,rng):
    T,k=y.shape;d=T-1;rw=hyper['walk_sd']**2;rv=hyper['read_sd']**2
    Q=np.diag(np.r_[np.full(d-1,2),1])/rw+np.eye(d)*k/rv
    ix=np.arange(d-1);Q[ix,ix+1]=-1/rw;Q[ix+1,ix]=-1/rw
    L=np.linalg.cholesky(Q)
    h=k*(y[1:].mean(axis=1)-hyper['bias'])/rv
    m=np.linalg.solve(L.T,np.linalg.solve(L,h))
    delta=solve_triangular(L.T,rng.normal(size=(d,draws)),lower=False)
    u=np.c_[np.zeros(draws),(m[:,None]+delta).T]
    return np.mean(np.exp(-abs(u)),axis=1)

def calibration_draws(rec,s,n,rng):
    particles=[];tries=0
    while len(particles)<n and tries<30*n:
        tries+=1
        C=np.eye(5)
        C[0]=rng.dirichlet(rec['ref0']+1)
        C[4]=rng.dirichlet(rec['ref4']+1)
        try:w=np.linalg.solve(C.T,rng.dirichlet(rec['source']+1))
        except np.linalg.LinAlgError:continue
        if np.min(w)<0:continue
        dark=np.array([rng.beta(v+1,s.ref_shots-v+1) for v in rec['dark']])
        clicks=np.array([rng.beta(v+1,s.ref_shots-v+1) for v in rec['one']])
        eta=(clicks-dark)/(1-dark)
        bg=rng.beta(rec['triggered']+1,s.ref_shots-rec['triggered']+1)
        q=(bg-dark[0]*dark[1])/(1-dark[0]*dark[1])
        if not(np.all((eta>0)&(eta<1)) and 0<q<1):continue
        p=Config(eta_a=float(eta[0]),eta_b=float(eta[1]),dark_a=float(dark[0]),dark_b=float(dark[1]),
             w11=float(w[0]+w[4]),w20=float(w[1]),w02=float(w[2]),overlap=.5)
        try:p.validate()
        except ValueError:continue
        particles.append((p,float(w[4]),float(q)))
    if len(particles)!=n:raise RuntimeError('insufficient calibrated particles')
    return particles

def marginal(rec,s,hyper,draws=160,seed=111):
    rng=np.random.default_rng(seed)
    A=phase_draws(rec['y'],hyper,draws,rng)
    particles=calibration_draws(rec,s,draws,rng)
    grid=np.linspace(.01,.99,161)
    baseline=np.zeros(draws);slope=np.zeros(draws);far=np.zeros(draws)
    for i,(p,f,q) in enumerate(particles):
        c0=forward(0,1,p,f,q);c1=forward(1,1,p,f,q)
        baseline[i]=c0[0];slope[i]=c0[0]-c1[0];far[i]=c0[1]
    probs=baseline[None,:]-grid[:,None]*A[None,:]*slope[None,:]
    ll=rec['near']*np.log(probs)+(s.shots-rec['near'])*np.log1p(-probs)
    far_ll=rec['far']*np.log(far)+(s.shots-rec['far'])*np.log1p(-far)
    marginal_ll=logsumexp(ll+far_ll[None,:],axis=1)
    weights=np.exp(marginal_ll-logsumexp(marginal_ll))
    cdf=np.cumsum(weights)
    ci=np.interp([.025,.975],cdf,grid)
    return {'mean':float(grid@weights),'ci95':ci.tolist(),
            'width':float(ci[1]-ci[0])}

def infer(rec,s=Setup(),draws=160,seed=111):
    hyp=fit_sensor(rec['y'],rec['z'])
    return {'hyper_mle':hyp,'posterior':marginal(rec,s,hyp,draws,seed),
            'hyper_uncertainty_integrated':False}

def jacobian(s=Setup(),h=1e-5):
    from dataclasses import replace
    p=Config();theta=np.array([.72,.065,.014,p.eta_a,p.eta_b])
    def f(a):
        pp=replace(p,eta_a=float(a[3]),eta_b=float(a[4]))
        return forward(a[0],.8,pp,a[1],a[2])
    return np.column_stack([(f(theta+np.eye(5)[i]*h)-f(theta-np.eye(5)[i]*h))/(2*h)
        for i in range(5)])

def audit(outer=40,draws=120,seed=102000,s=Setup()):
    rows=[]
    for i in range(outer):
        z=simulate(seed+19*i,s);fit=infer(z,s,draws,seed+80000+19*i)
        lo,hi=fit['posterior']['ci95']
        rows.append({'M_est':fit['posterior']['mean'],'ci95':[lo,hi],
           'covered':bool(lo<=s.M<=hi),'hyper':fit['hyper_mle']})
    est=np.array([x['M_est'] for x in rows])
    return {'outer':outer,'covered':sum(x['covered'] for x in rows),
      'mean':float(est.mean()),'rmse':float(np.sqrt(np.mean((est-s.M)**2))),
      'mean_width':float(np.mean([r['ci95'][1]-r['ci95'][0] for r in rows])),
      'mean_hyper':{k:float(np.mean([r['hyper'][k] for r in rows]))
                    for k in ('walk_sd','read_sd','bias')},'rows':rows}
