"""v1.01 GitHub companion. Unknown sensor random-walk hyperparameters and
two experimentally calibrated aggregate optical responses are marginalized.
A finite hyperprior GRID, exact conditional Gaussian smoothing and Monte
Carlo optical likelihood are used. Original tested source is in local ZIP.
"""
from dataclasses import dataclass
import numpy as np
from scipy.linalg import solve_triangular
from scipy.special import logsumexp
from models.latent_phase_v100 import default_setup

@dataclass(frozen=True)
class HyperGrid:
    walk:tuple=(.065,.095,.125)
    read:tuple=(.11,.15,.19)
    bias:tuple=(-.04,0.,.04)
    def combinations(self):
        if any(v<=0 for v in self.walk+self.read):raise ValueError('positive standard deviations')
        return [(float(q),float(r),float(b))
                for q in self.walk for r in self.read for b in self.bias]

def generate(seed=10101,repeats=2,steps=40,truth=.72,sw=.095,sr=.15,bias=0.,shots=25000,controls=15000,zero_refs=80):
    if repeats<1 or steps<3 or min(sw,sr,shots,controls,zero_refs)<=0 or not 0<truth<1:raise ValueError('inputs')
    rng=np.random.default_rng(seed)
    u=np.r_[0,np.cumsum(rng.normal(0,sw,steps-1))]
    y=u[:,None]+bias+rng.normal(0,sr,(steps,repeats))
    z=bias+rng.normal(0,sr,zero_refs)
    setup=default_setup();c0=setup.intercept;c1=setup.intercept-setup.slope
    control0=int(rng.binomial(controls,c0));control1=int(rng.binomial(controls,c1))
    A=float(np.mean(np.exp(-np.abs(u))))
    c=int(rng.binomial(shots,c0-(c0-c1)*truth*A))
    return {'y':y,'zero':z,'control0':control0,'control1':control1,
        'count':c,'shots':shots,'controls':controls,'truth':truth,
        'true_attenuation':A,'true_path':u,'repeats':repeats}

def hyperposterior(rec,grid=None):
    grid=HyperGrid() if grid is None else grid
    y=np.asarray(rec['y'],float);z=np.asarray(rec['zero'],float)
    if y.ndim!=2 or y.shape[0]<3 or y.shape[1]<1 or len(z)<2:raise ValueError('sensor observations')
    T,k=y.shape;d=T-1;avg=y.mean(axis=1)
    SSE=float(np.sum((y-avg[:,None])**2))
    temporal=np.minimum.outer(np.arange(T),np.arange(T))
    models=[];ll=[]
    for sw,sr,b in grid.combinations():
        r=sw*sw;v=sr*sr
        S=r*temporal+(v/k)*np.eye(T)
        L=np.linalg.cholesky(S)
        zeta=solve_triangular(L,avg-b,lower=True)
        logp=-.5*(T*np.log(2*np.pi)+2*np.log(np.diag(L)).sum()+zeta@zeta)
        logp+=-.5*(T*(k-1)*np.log(2*np.pi*v)+SSE/v)
        logp+=-.5*(len(z)*np.log(2*np.pi*v)+np.sum((z-b)**2)/v)
        Q=np.diag(np.r_[np.full(d-1,2.),1.])/r+k/v*np.eye(d)
        indices=np.arange(d-1);Q[indices,indices+1]=-1/r;Q[indices+1,indices]=-1/r
        C=np.linalg.cholesky(Q)
        h=k*(avg[1:]-b)/v
        mean=np.linalg.solve(C.T,np.linalg.solve(C,h))
        models.append((sw,sr,b,mean,C));ll.append(logp)
    weights=np.exp(ll-logsumexp(ll))
    return models,weights

def path_draws(models,weights,count=240,seed=42):
    if count<10:raise ValueError('count >=10')
    rng=np.random.default_rng(seed);ix=rng.choice(len(models),size=count,p=weights)
    attenuation=np.empty(count);drawn_hyper=np.empty((count,3))
    for j in np.unique(ix):
        sw,sr,b,mean,L=models[j]
        indices=np.flatnonzero(ix==j)
        noise=np.linalg.solve(L.T,rng.normal(size=(len(mean),len(indices))))
        p=np.column_stack([np.zeros(len(indices)),(mean[:,None]+noise).T])
        attenuation[indices]=np.mean(np.exp(-np.abs(p)),axis=1)
        drawn_hyper[indices]=[sw,sr,b]
    return attenuation,drawn_hyper

def optical_posterior(rec,attenuation,c0,c1,grid=None):
    M=np.linspace(.001,.999,251) if grid is None else np.asarray(grid)
    n=rec['count'];N=rec['shots']
    probability=c0[None,:]-(c0[None,:]-c1[None,:])*M[:,None]*attenuation[None,:]
    if np.any((probability<=0)|(probability>=1)):raise ValueError('optical probabilities')
    logl=n*np.log(probability)+(N-n)*np.log1p(-probability)
    logw=logsumexp(logl,axis=1)-np.log(len(attenuation))
    w=np.exp(logw-logsumexp(logw));cdf=np.cumsum(w)
    lo,hi=np.interp([.025,.975],cdf,M)
    return {'mean':float(w@M),'ci95':[float(lo),float(hi)],
            'width':float(hi-lo)}

def infer(rec,draws=240,seed=42,grid=None):
    models,weights=hyperposterior(rec,grid)
    attenuation,hypers=path_draws(models,weights,draws,seed)
    rng=np.random.default_rng(seed+9900)
    a0=rec['control0']+1;b0=rec['controls']-rec['control0']+1
    a1=rec['control1']+1;b1=rec['controls']-rec['control1']+1
    c0=rng.beta(a0,b0,draws);c1=rng.beta(a1,b1,draws)
    joint=optical_posterior(rec,attenuation,c0,c1)
    plugin_attenuation=sum(wi*np.mean(np.exp(-np.abs(np.r_[0.,m[3]])))
        for m,wi in zip(models,weights))
    plugin=optical_posterior(rec,np.full(draws,plugin_attenuation),
       np.full(draws,a0/(a0+b0)),np.full(draws,a1/(a1+b1)))
    h=np.asarray([model[:3] for model in models])
    return {'joint':joint,'plugin':plugin,
        'hyper_mean':(weights@h).tolist(),
        'attenuation_mean':float(attenuation.mean()),
        'attenuation_sd':float(attenuation.std(ddof=1))}

def audit(outer=40,repeats=(1,2,10),draws=240,seed=101000):
    if outer<2:raise ValueError('outer >=2')
    res={}
    for count in repeats:
        rows=[]
        for i in range(outer):
            rec=generate(seed+107*i,repeats=count)
            fit=infer(rec,draws,seed+10000+i+100*count)
            row={'seed':seed+107*i,'true_attenuation':rec['true_attenuation'],
                'hyper_mean':fit['hyper_mean']}
            for m in ('joint','plugin'):
                row[m]=fit[m]
                row[m+'_covered']=fit[m]['ci95'][0]<=rec['truth']<=fit[m]['ci95'][1]
            rows.append(row)
        summary={}
        for m in ('joint','plugin'):
            vals=np.asarray([r[m]['mean'] for r in rows])
            summary[m]={'covered':sum(r[m+'_covered'] for r in rows),
                'mean':float(vals.mean()),'rmse':float(np.sqrt(np.mean((vals-.72)**2))),
                'mean_width':float(np.mean([r[m]['width'] for r in rows]))}
        summary['rows']=rows;res[str(count)]=summary
    return {'version':'v1.01','synthetic':True,'prior':'discrete 27-point hypergrid',
        'reference_control':15000,'zero_phase_refs':80,'results':res,
        'scientific_limit':'not separately identifying every PNR/detector/electronics error'}
