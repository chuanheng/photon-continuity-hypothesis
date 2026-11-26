"""Bounds on the one-one sector of two phase-randomized probe sources."""
import json
from itertools import product
import numpy as np
from scipy.stats import poisson
from scipy.optimize import linprog
from scipy.special import i0
from v972_v981.model import B,table,SINGLET

def gains(pairs, scale=.5):
    a,b=np.array(pairs).T
    return .002+scale*np.expm1(-.6*a)*np.expm1(-.4*b)

def interval(pairs,observed,cut=6,err=0.):
    a,b=np.array(pairs).T
    n=np.arange(cut+1)
    left=poisson.pmf(n,a[:,None])
    right=poisson.pmf(n,b[:,None])
    A=np.einsum('si,sj->sij',left,right).reshape(len(pairs),-1)
    tail=1-poisson.cdf(cut,a)*poisson.cdf(cut,b)
    cost=np.zeros((cut+1,cut+1));cost[1,1]=1
    limits=[]
    for sign in (1,-1):
        sol=linprog(sign*cost.ravel(),A_ub=np.vstack([A,-A]),b_ub=np.r_[observed+err,tail-observed+err],
                    bounds=(0,1),options={'primal_feasibility_tolerance':1e-10,'dual_feasibility_tolerance':1e-10})
        if not sol.success: raise RuntimeError(sol.message)
        limits.append(float(sol.x[cut+2]))
    return limits

def mixed(h):
    pairs=[(h,h),(0,h),(h,0),(0,0)]
    vals=gains(pairs)*np.exp(np.sum(pairs,axis=1))
    return float(np.dot([1,-1,-1,1],vals)/h**2)

def run():
    grid=list(product([0,.08,.35],repeat=2))
    rich=list(product([0,.035,.15,.5],repeat=2))
    delta=.1
    def alias(a,b):return delta*np.exp(-a-b)*(a*b-(a*a+b*b)/2)
    bound=interval(grid,gains(grid))
    h=.08
    baseline=mixed(h)
    extrap=2*mixed(h/2)-baseline
    # Total mass of the residual k=n+m-2>=2 terms, for 0<=Y<=1.
    geom=lambda x:(np.expm1(x)/x)**2
    residual=geom(h)-2*geom(h/2)+1
    # Distinguish common pump modulation from independent marginal mixtures.
    pair=np.array([[.35,.35]])
    def activate(mu,eta):return -np.expm1(-mu*eta)
    la=activate(.35*np.array([.4,1.6]),.6)
    lb=activate(.35*np.array([.4,1.6]),.4)
    mu=.35
    # For a balanced beam splitter with equal coherent inputs and random relative phase:
    # mean occupancy in the dark output = mu*(1-cos(phi)).
    ideal=table(SINGLET)
    bounds=np.array([interval(rich,gains(rich,scale=x)) for x in ideal.ravel()]).reshape(4,4,2)
    upper=float(np.sum(np.where(B>0,B*bounds[:,:,1],B*bounds[:,:,0])))
    return dict(joint=dict(truth=.002+.5*.6*.4,range=bound),
                diagonal_alias=dict(diagonal=alias(.35,.35),off_axis=alias(.35,.08),delta_y11=delta),
                vacuum_rails=dict(value=baseline,remainder=geom(h)-1),
                extrapolation=dict(lower=extrap,upper=extrap+residual),
                rectangular_scan=dict(diagonal=interval([(x,x) for x in [0,.08,.35]],gains([(x,x) for x in [0,.08,.35]])),rich=interval(rich,gains(rich))),
                joint_error=interval(rich,gains(rich),err=1e-5),
                shared_pump=dict(shared=float((la*lb).mean()),independent=float(la.mean()*lb.mean())),
                phase_lock=dict(common=0.,independent=float(1-np.exp(-mu)*i0(mu))),
                attenuation_gauge=dict(effective=.8*.6,alternative=.96*.5,
                                       one_photon_yields=[.002+.5*.6*.4,.002+.5*.5*.4]),
                signed_joint=dict(upper=upper,truth=float(np.sum(B*(.002+.6*.4*ideal)))))
if __name__=='__main__':print(json.dumps(run(),indent=2))
