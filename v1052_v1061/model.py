"""Occupation certification after a material phase flip with an unresolved spectator."""
import json
import numpy as np

def run():
    a,r,b=np.array([.32,.32]),.18,np.array([.65,.60])
    true=.65
    measured=true*b+(1-true)*(a+r*np.array([-.8,.6]))
    # Individual block spectral envelopes for two phase-cycled effects.
    lo=(measured-a-r)/(b-a-r)
    hi=(measured-a+r)/(b-a+r)
    v=measured-a;w=b-a
    roots=np.roots([w@w-r*r,2*(r*r-v@w),v@v-r*r])
    # A spectator with exactly the material's detection efficiency.
    effect=np.diag([.04,.36,.36])
    rho1=np.diag([.7,.3,0]);rho2=np.diag([.7,0,.3])
    U=np.diag([1,-1,1])
    cycled=(effect+U@effect@U)/2
    # Equal two-pulse mixture at 0 and pi+delta.
    c=.08;gap=.32;delta=.12
    amplitude=abs((1-np.exp(1j*delta))/2)
    # Weight error in nominally cancelling phases: imbalance 2w-1.
    duty=.53
    return dict(alias=dict(clicks=[float(np.trace(cycled@rho)) for rho in (rho1,rho2)],occupancies=[.3,0]),
                spectral=dict(measured=measured.tolist(),individual_lower=np.maximum(0,lo).tolist(),
                              individual_upper=np.minimum(1,hi).tolist()),
                joint=dict(interval=np.clip(np.sort(roots),0,1).tolist(),intersection=[max(0.,max(lo)),min(1.,min(hi))]),
                angle_error=dict(residual=amplitude,worst_population_bias=c*amplitude/gap),
                unequal_duty=dict(raw_max_bias=c*abs(2*duty-1)/gap,weighted_phase_coefficient=float(abs(np.average([1.,-1.],weights=[duty,1-duty]))),balanced_coeff=float(abs(np.mean([1.,-1.])))))
if __name__=='__main__':print(json.dumps(run(),indent=2))
