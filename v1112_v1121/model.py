"""Energy-preserving implementation of recovery on the ideal single-jump subspace."""
import json
import numpy as np

def overlap(amp,k):
    return np.vdot(amp[:-k],amp[k:]) if k<len(amp) else 0.

def shifted(amp,k):
    out=np.zeros(len(amp)+4,complex)
    out[k:k+len(amp)]=amp
    return out

def encoded(amp):
    # Input battery levels start at 1. New battery indices start at 0.
    # Columns correspond to input Fock 3,1 respectively.
    blocks=np.zeros((5,len(amp)+4,2),complex)
    blocks[0,:,0]=shifted(amp,4)/np.sqrt(2)
    blocks[4,:,0]=shifted(amp,0)/np.sqrt(2)
    blocks[2,:,1]=shifted(amp,0)
    return blocks

def run():
    D=16
    amp=np.ones(D)/np.sqrt(D)
    g=float(overlap(amp,4))
    flat=encoded(amp).reshape(-1,2)
    # Test each nonzero amplitude of the elementary map, before summing over energy.
    defects=[abs(n+m-(s+l)) for m in range(1,D+1) for n,s,l in [(3,0,m+3),(3,4,m-1),(1,2,m-1)]]
    H=(np.eye(D,k=4)+np.eye(D,k=-4))/2
    eig,vec=np.linalg.eigh(H)
    L,R=shifted(amp,4),shifted(amp,0)
    envdiff=np.outer(L,L.conj())-np.outer(R,R.conj())
    # Equal amplitudes in the idealized two-arm environment measurement.
    herald=(L+R)/np.linalg.norm(L+R)
    phase=.08
    return dict(conservation=dict(gram_error=float(np.linalg.norm(flat.conj().T@flat-np.eye(2))),energy_defect=max(defects)),
                finite_coherence=dict(number_Fe=.625,flat_g4=g,flat_Fe=.625+.375*g),
                energy_shift=dict(base=float(overlap(amp,4)),raised=float(overlap(np.pad(amp,(23,0)),4))),
                optimized=dict(max_g4=float(eig[-1]),flat_g4=g,rayleigh=float(overlap(vec[:,-1],4))),
                worst_input=dict(Fe=.625+.375*g,worst=(1+g)/2,best=1.),
                phase_drift=dict(known_offset_g=g*np.cos(4*phase),Gaussian_g=g*np.exp(-8*phase**2)),
                which_shift=dict(trace_distance=float(abs(np.linalg.eigvalsh(envdiff)).sum()/2),overlap=g),
                eraser=dict(accept=float(abs(np.vdot(herald,L))**2),arm_mismatch=float(abs(np.vdot(herald,L)-np.vdot(herald,R)))),
                reuse=dict(shared_g8=float(overlap(amp,8)),fresh_g4_squared=g**2,exchange_shared=1.,exchange_fresh=g**2),
                number_readout=dict(population_distance=0.,phase_contrast_gap=1-g))
if __name__=='__main__':print(json.dumps(run(),indent=2))
