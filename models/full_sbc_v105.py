"""v1.05 GitHub companion: joint prior HOM SBC, finite grids & Fock triplets.
Independently authored: exact 40-test executed source is in local ZIP.
"""
import numpy as np
from scipy.special import logsumexp,betaln
from scipy.linalg import solve_triangular
from scipy.stats import chisquare

T=24; K=2; SOURCE_N=240; STD_N=250; REF_N=500; DARK_N=900; ZERO_N=40; OPT_N=1500
HYPER=np.array([(a,b,c) for a in (.07,.11,.17)
    for b in (.10,.17,.26) for c in (-.035,0.,.035)])
R=np.linspace(.0005,.9995,151);M=np.linspace(.0005,.9995,161)
PR=(2-1)*np.log(R)+(30-1)*np.log1p(-R)-betaln(2,30)

def split_fock_21():return np.array([3,1,1,3])/8

def clicks(m,A,f,q,eta_a,eta_b,da,db):
    def click(k,e,d):return 1-(1-d)*(1-e)**k
    ca=[click(k,eta_a,da) for k in range(4)]
    cb=[click(k,eta_b,db) for k in range(4)]
    c20=ca[2]*cb[0];c11=ca[1]*cb[1];c02=ca[0]*cb[2];c00=ca[0]*cb[0]
    mid=.5*c11+.25*(c20+c02)
    near_trip=(3*ca[0]*cb[3]+ca[1]*cb[2]+ca[2]*cb[1]+3*ca[3]*cb[0])/8
    far_trip=(ca[0]*cb[3]+3*ca[1]*cb[2]+3*ca[2]*cb[1]+ca[3]*cb[0])/8
    pair_near=mid-m*A*(.5*c11-.25*(c20+c02))
    near=(.9-f)*pair_near+.08*mid+.02*c00+f*near_trip
    far=(.98-f)*mid+.02*c00+f*far_trip
    return np.broadcast_arrays(q+(1-q)*near,q+(1-q)*far)

def generate(seed):
    g=np.random.default_rng(seed)
    truth={'M':g.uniform(),'r':g.beta(2,30),'alpha':g.beta(2,8),
       'beta':g.beta(1,45),'q':g.beta(2,160),'eta_a':g.beta(25,8),
       'eta_b':g.beta(23,10),'da':g.beta(1,350),'db':g.beta(1,300)}
    h=int(g.integers(27));sw,sr,b=HYPER[h]
    truth.update({'hyper_idx':h,'walk_sd':sw,'read_sd':sr,'bias':b})
    u=np.r_[0.,g.normal(0,sw,T-1).cumsum()]
    y=u[:,None]+b+g.normal(0,sr,(T,K));z=b+g.normal(0,sr,ZERO_N)
    r=truth['r'];p=r*(1-truth['alpha'])+(1-r)*truth['beta']
    obs={'y':y,'zero':z,'source':int(g.binomial(SOURCE_N,p)),
      'alpha':int(g.binomial(STD_N,truth['alpha'])),
      'beta':int(g.binomial(STD_N,truth['beta'])),
      'q':int(g.binomial(REF_N,truth['q'])),
      'eta_a':int(g.binomial(REF_N,truth['eta_a'])),
      'eta_b':int(g.binomial(REF_N,truth['eta_b'])),
      'da':int(g.binomial(DARK_N,truth['da'])),
      'db':int(g.binomial(DARK_N,truth['db']))}
    p0,p1=clicks(truth['M'],np.mean(np.exp(-abs(u))),.9*r,
       truth['q'],truth['eta_a'],truth['eta_b'],truth['da'],truth['db'])
    obs['near']=int(g.binomial(OPT_N,p0));obs['far']=int(g.binomial(OPT_N,p1))
    return obs,truth

def conditional_phase(obs):
    y=obs['y'];avg=y.mean(axis=1)
    tm=np.minimum.outer(np.arange(T),np.arange(T))
    resid=np.sum((y-avg[:,None])**2);ll=[];details=[]
    for sw,sr,b in HYPER:
        v=sr**2;cov=sw**2*tm+np.eye(T)*v/K
        L=np.linalg.cholesky(cov)
        h=solve_triangular(L,avg-b,lower=True)
        lp=-.5*(T*np.log(2*np.pi)+2*np.log(np.diag(L)).sum()+h@h)
        lp+=-.5*(T*(K-1)*np.log(2*np.pi*v)+resid/v)
        lp+=-.5*(ZERO_N*np.log(2*np.pi*v)+np.sum((obs['zero']-b)**2)/v)
        Q=np.diag(np.r_[np.full(T-2,2.),1.])/sw**2+np.eye(T-1)*K/v
        ii=np.arange(T-2);Q[ii,ii+1]=-1/sw**2;Q[ii+1,ii]=-1/sw**2
        C=np.linalg.cholesky(Q)
        h=np.sum(y[1:]-b,axis=1)/v
        mean=np.linalg.solve(C.T,np.linalg.solve(C,h))
        ll.append(lp);details.append((mean,C))
    return np.exp(ll-logsumexp(ll)),details

def calibrate(obs,n,g):
    a=g.beta(2+obs['alpha'],8+STD_N-obs['alpha'],n)
    b=g.beta(1+obs['beta'],45+STD_N-obs['beta'],n)
    p=b[:,None]+(1-a-b)[:,None]*R[None,:]
    lp=obs['source']*np.log(p)+(SOURCE_N-obs['source'])*np.log1p(-p)+PR[None,:]
    evidence=logsumexp(lp,axis=1)
    cp=np.exp(lp-logsumexp(lp,axis=1,keepdims=True))
    ir=np.sum(np.cumsum(cp,axis=1)<g.random(n)[:,None],axis=1)
    return dict(alpha=a,beta=b,r=R[np.minimum(ir,len(R)-1)],
       q=g.beta(2+obs['q'],160+REF_N-obs['q'],n),
       eta_a=g.beta(25+obs['eta_a'],8+REF_N-obs['eta_a'],n),
       eta_b=g.beta(23+obs['eta_b'],10+REF_N-obs['eta_b'],n),
       da=g.beta(1+obs['da'],350+DARK_N-obs['da'],n),
       db=g.beta(1+obs['db'],300+DARK_N-obs['db'],n)),evidence

def infer(obs,n=850,draws=49,seed=1):
    g=np.random.default_rng(seed);hp,details=conditional_phase(obs)
    h=g.choice(27,n,p=hp);p,ev=calibrate(obs,n,g)
    A=np.empty(n)
    for i in np.unique(h):
        loc=np.flatnonzero(h==i);m,C=details[i]
        u=m[:,None]+solve_triangular(C.T,g.normal(size=(T-1,len(loc))),lower=False)
        A[loc]=np.mean(np.exp(-abs(np.vstack([np.zeros(len(loc)),u]))),axis=0)
    near,far=clicks(M[:,None],A[None,:],(.9*p['r'])[None,:],p['q'][None,:],
       p['eta_a'][None,:],p['eta_b'][None,:],p['da'][None,:],p['db'][None,:])
    logl=obs['near']*np.log(near)+(OPT_N-obs['near'])*np.log1p(-near)
    logl+=obs['far']*np.log(far)+(OPT_N-obs['far'])*np.log1p(-far)
    logl+=ev[None,:]-max(ev)
    w=np.exp(logl-logsumexp(logl));nw=w.sum(axis=0)
    selected=g.choice(n,draws,p=nw)
    conditional=w[:,selected]/nw[selected]
    midx=np.sum(np.cumsum(conditional,axis=0)<g.random(draws)[None,:],axis=0)
    out={'M':M[np.minimum(midx,len(M)-1)],'walk_sd':HYPER[h[selected],0],
         'read_sd':HYPER[h[selected],1],'bias':HYPER[h[selected],2]}
    for key,value in p.items():out[key]=value[selected]
    Mprob=w.sum(axis=1);interval=np.interp([.025,.975],np.cumsum(Mprob),M)
    return {'draws':out,'M95':interval.tolist(),'Mmean':float(M@Mprob),
        'ess':float(1/np.sum(nw**2))}

def ranks(truth,draws,g):
    output={}
    for k in truth:
        if k=='hyper_idx':continue
        if k not in draws:continue
        values=np.asarray(draws[k]);x=truth[k]
        if k in ('walk_sd','read_sd','bias'):
            x=x+g.random()*1e-4;values=values+g.random(len(values))*1e-4
        output[k]=int(np.sum(values<x))
    return output

def audit(n=450,particles=850,draws=49,seed=10501):
    rng=np.random.default_rng(seed)
    rr={k:[] for k in ('M','r','alpha','beta','q','eta_a','eta_b','da','db','walk_sd','read_sd','bias')}
    data=[]
    for i in range(n):
        obs,truth=generate(int(rng.integers(1,2**31-1)))
        fit=infer(obs,particles,draws,int(rng.integers(1,2**31-1)))
        x=ranks(truth,fit['draws'],rng)
        for name in rr:rr[name].append(x[name])
        data.append({'M_truth':truth['M'],'Mmean':fit['Mmean'],
          'covered':bool(fit['M95'][0]<=truth['M']<=fit['M95'][1]),'ESS':fit['ess']})
    return {'n':n,'particles':particles,'draws':draws,'records':data,
        'Mcovered':sum(d['covered'] for d in data),
        'median_ESS':float(np.median([d['ESS'] for d in data])),
        'rank_tests':{k:float(chisquare(np.histogram(v,np.linspace(-.5,draws+.5,11))[0]).pvalue)
                     for k,v in rr.items()},'ranks':rr}
