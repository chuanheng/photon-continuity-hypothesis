"""External loss-port monitors of an intermediate one-excitation subspace."""
import json
import numpy as np
from scipy.linalg import expm
from scipy.integrate import quad

def interval(p,a,b,c):
    # Positive-state constraint on the unknown off-diagonal element of rho.
    d=b-a;z=p-a
    return sorted(np.roots([d*d+4*c*c,-2*z*d-4*c*c,z*z]).real.tolist())

def survival(t,k):
    generator=np.array([[0,-1j],[-1j,-k/2]])
    return float(np.linalg.norm(expm(t*generator)[:,0])**2)

def run():
    x=.25;k=.4;eta=.8;d=.01
    observed=d+(1-d)*eta*k*x
    noisy=[(observed-.012)/(1-.012)/(.85*.42),(observed-.008)/(1-.008)/(.75*.38)]
    E=np.array([[.04,.08],[.08,.36]])
    state=np.sqrt([1-x,x])
    p=float(state@E@state)
    flipped=state*np.array([1,-1])
    q=float(flipped@E@flipped)
    # Coherent loss into a single initially empty ancillary mode: subsequent inverse pulse.
    U=np.array([[np.sqrt(1-k),-np.sqrt(k)],[np.sqrt(k),np.sqrt(1-k)]])
    absorbed=float((U.T@U)[0,0]**2)
    decohered=float(np.dot(U[:,0]**2,U[:,0]**2))
    conditional=x*(1-k)/(1-k*x)
    first=x*k*eta
    second=x*(1-k)*k*eta
    # An ideal absorber after each equally spaced rotation discards jumps.
    def zeno(n):return float(np.cos(np.pi/(2*n))**(2*n))
    t=1.4; analytic=t/2-np.sin(2*t)/4
    step=1e-5
    derivative=(survival(t,-step)-survival(t,step))/(2*step)
    # Same external jump instrument, permuted hidden states: record string probabilities.
    P=np.array([[.8,.25],[.2,.75]])
    J=np.diag([.10,.45]);N=np.eye(2)-J;p0=np.array([.3,.7])
    swap=np.eye(2)[::-1]
    from itertools import product
    def records(initial,ops):
        out=[]
        for choices in product(range(2),repeat=4):
            v=initial.copy()
            for index in choices:v=ops[index]@v
            out.append(float(v.sum()))
        return np.array(out)
    ops=[P@N,P@J];r=records(p0,ops)
    return dict(external_click=dict(observed=observed,recovered=(observed-d)/((1-d)*eta*k)),
                calibration_interval=noisy,coherent_leak=dict(p=p,range=interval(p,.04,.36,.08)),
                phase_cycle=dict(plus=p,minus=q,inferred=((p+q)/2-.04)/.32),
                environment_return=dict(unobserved=absorbed,recorded=decohered),
                null_backaction=dict(ideal_no_jump=conditional,missed_monitor_material=x*(1-k)/(1-eta*k*x)),
                two_taps=dict(first=first,second=second,extraction=1-second/first,occupancy_times_eta=first/k),
                zeno=[zeno(n) for n in (1,2,5,20,100)],
                residence=dict(analytic=analytic,derivative=derivative,error=abs(analytic-derivative)),
                hidden_records=dict(max_error=float(max(abs(r-records(swap@p0,[swap@op@swap.T for op in ops])))),sum=float(r.sum())))
if __name__=='__main__':print(json.dumps(run(),indent=2))
