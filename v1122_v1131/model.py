"""System-only history coherences of a reused, boundary-free energy reference."""
import json
from itertools import product
import numpy as np

def moments(amp,theta):
    amplitude=np.exp(1j*np.outer(theta,np.arange(len(amp))))@amp
    return abs(amplitude)**2/len(theta)

def run():
    D=16
    amp=np.ones(D)/np.sqrt(D)
    shifts=np.array([sum(h) for h in product((-1,3),repeat=3)])
    diff=shifts[:,None]-shifts[None,:]
    gram=np.maximum(0.,1-abs(diff)/D)
    theta=np.arange(64)*2*np.pi/64
    weights=moments(amp,theta)
    ordinary=np.sum(weights[:,None,None]*np.exp(1j*theta[:,None,None]*diff),axis=0)
    g=.75
    # Window starts at level 1; |1> target requires extracting one quantum from pump.
    # The physical terminal branch is chosen to remain unchanged if no quantum is available.
    floor_prob=1/D
    # Midway pulse exp(i*k*N^2) and two translated arms sharing the same initial pump.
    k=.035
    m=np.arange(2,2+D)
    coh=np.mean(np.exp(1j*k*((m+3)**2-(m-1)**2)))
    # Diagonal energy measurement at middle: two equally probable shift histories.
    L=np.r_[np.zeros(4),amp]**2
    R=np.r_[amp,np.zeros(4)]**2
    # A controlled translation and its inverse around a phase rotation.
    phi=.28
    weyl=np.mean(np.exp(1j*phi*((m+4)-m)))
    # Schmidt eigenvalues of an equal two-history state with pump overlap g.
    spectrum=np.linalg.eigvalsh(np.array([[1.,g],[g,1.]])/2)
    s1,s2=np.sqrt(spectrum)
    visibility=abs(coh)
    # Gaussian classical relative phase with exactly the same complex first moment.
    variance=-2*np.log(visibility)
    reconstructed=np.exp(1j*np.angle(coh)-variance/2)
    return dict(loop=dict(phase=float(np.angle(weyl)),visibility=float(abs(weyl))),
                classical_kick_fit=dict(phase_variance=float(variance),complex_error=float(abs(coh-reconstructed))),
                pump_entanglement=dict(schmidt=spectrum.tolist(),negativity=float(s1*s2)),
                bell_test=dict(ideal=float(2*np.sqrt(1+4*s1*s1*s2*s2)),critical_white_visibility=float(1/np.sqrt(1+4*s1*s1*s2*s2))),
                energy_superselection=dict(twirled_negativity=0.,blocks=int(len(L)),joint_trace=float((L+R).sum()/2)),
                phase_representation=dict(max_error=float(abs(ordinary-gram).max()),weights_sum=float(weights.sum()),histories=len(shifts)),
                moment_bound=dict(g4=g,lower=2*g*g-1,upper=1.,flat_g8=.5),
                boundary=dict(second_failure=floor_prob,success_both=1-floor_prob),
                interposed_kerr=dict(real=float(coh.real),imag=float(coh.imag),visibility=float(abs(coh))),
                number_access=dict(energy_TV=float(abs(L-R).sum()/2),optimal_pure_TV=float(np.sqrt(1-g*g))))
if __name__=='__main__':print(json.dumps(run(),indent=2))
