"""Variable-intensity photon-number controls for one trusted probe arm."""
import json
import numpy as np
from scipy.optimize import linprog,brentq
from scipy.stats import poisson

def gain(mu,eff=.18,d=.002):
    return 1-(1-d)*np.exp(-eff*np.asarray(mu))

def analytic(mu,nu,q0,qn,qm):
    ratio=(nu/mu)**2
    return mu/(mu*nu-nu**2)*(np.exp(nu)*qn-ratio*np.exp(mu)*qm-(1-ratio)*q0)

def interval(mus,counts,cut=8,radius=0.):
    mu=np.array(mus)
    A=poisson.pmf(np.arange(cut+1)[None,:],mu[:,None])
    tail=poisson.sf(cut,mu)
    target=np.eye(cut+1)[1]
    bounds=[]
    for sign in (1,-1):
        fit=linprog(sign*target,A_ub=np.vstack((A,-A)),
                    b_ub=np.r_[counts+radius,-counts+tail+radius],bounds=(0,1),
                    options={'primal_feasibility_tolerance':1e-10,'dual_feasibility_tolerance':1e-10})
        if not fit.success:raise ValueError(fit.message)
        bounds.append(float(sign*fit.fun))
    return bounds

def run():
    mu,nu=.6,.15
    source=np.array([0.,nu,mu])
    q=gain(source)
    y1=float(gain(0)+.998*.18)
    single=interval([mu],np.array([q[2]]))
    # Match an unbounded-support distribution by changing just Y1,Y2.
    shift=.04
    y2=1-.998*(1-.18)**2
    fake=[y1+shift,y2-2*shift/mu]
    classical=analytic(mu,nu,*q)
    tails={str(n):interval(source,q,n) for n in [3,5,8]}
    more=np.r_[source,.035]
    labelq=q.copy()
    labelq[1]=gain(nu,.24)
    # Classical mixture with 80% low and 20% high transmission.
    low,high=.12,.30
    interleaved=.8*gain(source,low)+.2*gain(source,high)
    blocked=np.array([gain(0),gain(nu,high),gain(mu,low)])
    # Project onto (|0>+|1>)/sqrt(2), zero on higher numbers.
    coherent=np.exp(-nu)*(1+np.sqrt(nu))**2/2
    twirled=np.exp(-nu)*(1+nu)/2
    # Bounds for a sixteenth-table cell are not themselves a signed score.
    # Illustrative synthetic response: mode activation eta and depolarizing background d.
    from v972_v981.model import B,table,SINGLET
    bell=table(SINGLET)
    gains=np.array([(.002+(1-np.exp(-.6*m))*bell) for m in more])
    limits=np.array([interval(more,gains[:,i,j],cut=8) for i,j in np.ndindex(4,4)]).reshape(4,4,2)
    upper=float(np.sum(np.where(B>0,B*limits[:,:,1],B*limits[:,:,0])))
    return dict(gain_map=dict(q=q.tolist(),y1=y1),one_setting=dict(interval=single,alternative=fake),
                weak_vacuum=dict(lower=classical,upper=(np.exp(nu)*q[1]-q[0])/nu),
                tail_relaxation=tails,extra_intensity=interval(more,gain(more)),
                noise_budget=interval(more,gain(more),radius=.0002),
                setting_leak=dict(apparent_lower=analytic(mu,nu,*labelq),signal_y1=y1),
                block_drift=dict(randomized_lower=analytic(mu,nu,*interleaved),
                                 pooled_y1=.002+.998*(.8*low+.2*high),blocked_lower=analytic(mu,nu,*blocked)),
                phase_coherence=dict(locked=coherent,randomized=twirled),
                cell_witness=dict(upper=upper,truth=float(np.sum(B*(.002+.6*bell)))))
if __name__=='__main__': print(json.dumps(run(),indent=2))
