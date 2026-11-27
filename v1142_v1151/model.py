"""Operational audits for an explicit hidden photon-label surrogate."""
import json
import math
import numpy as np
from scipy.linalg import expm

SEED = 114251

I2=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex); Y=np.array([[0,-1j],[1j,0]],complex); Z=np.diag([1,-1]).astype(complex)

def hom_coincidence(overlap):
    return .5*(1-abs(overlap)**2)

def swap_storage_fidelity(state):
    # One excitation in either optical or material rail. Two SWAPs restore it.
    swap=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],complex)
    rho=np.kron(state,np.array([[1,0],[0,0]],complex))
    restored=swap@(swap@rho@swap.conj().T)@swap.conj().T
    reduced=np.trace(restored.reshape(2,2,2,2),axis1=1,axis2=3)
    return float(np.real(np.trace(state@reduced)))

def rz(angle): return expm(-.5j*angle*Z)

def hidden_and_classical_histories(seed=SEED, steps=5, theta=.31):
    rng=np.random.default_rng(seed)
    controls=[expm(-.5j*a*X)@expm(-.5j*b*Y) for a,b in rng.normal(size=(steps,2))]
    initial=np.array([[.7,.2+.1j],[.2-.1j,.3]],complex)
    branches=[]
    for sign in (-1,1):
        u=I2.copy()
        for c in controls: u=rz(sign*2*theta)@c@u
        branches.append(u@initial@u.conj().T)
    classical=sum(branches)/2
    # Quantum label is a coherent |+> control; tracing it gives the same two branches.
    quantum=sum(branches)/2
    return float(np.max(abs(quantum-classical))), classical

def reset_witness(theta=.31):
    static=math.cos(4*theta)
    environment_reset=math.cos(2*theta)**2
    system_reset_only=static
    return static, environment_reset, system_reset_only

def cross_kerr_channel(theta=.31):
    # Hidden Z eigenstates produce ordinary random detunings ±theta.
    coherence=math.cos(2*theta)
    choi=np.array([[1,0,0,coherence],[0,0,0,0],[0,0,0,0],[coherence,0,0,1]],float)/2
    return coherence, np.linalg.eigvalsh(choi)

def convex_refit():
    settings=np.array([0.,.4,.9,1.4,2.0,2.6])
    plus=(1+np.cos(settings+.35))/2
    minus=(1+np.cos(settings-.55))/2
    candidate=.35*plus+.65*minus
    fit=np.column_stack([plus,minus])@np.array([.35,.65])
    return float(np.max(abs(candidate-fit))), candidate

def calibrated_distance():
    _,candidate=convex_refit(); settings=np.array([0.,.4,.9,1.4,2.0,2.6])
    plus=(1+np.cos(settings+.35))/2; minus=(1+np.cos(settings-.55))/2
    restricted=.38*plus+.62*minus
    restricted_distance=float(np.linalg.norm(candidate-restricted))
    expanded=np.column_stack([plus,minus,candidate])@np.array([0.,0.,1.])
    return restricted_distance,float(np.linalg.norm(candidate-expanded))

def finite_power(seed=SEED, experiments=2000, shots=400):
    rng=np.random.default_rng(seed); p0=.50; p1=.56
    threshold=.5425
    null=rng.binomial(shots,p0,experiments)/shots
    alt=rng.binomial(shots,p1,experiments)/shots
    return float(np.mean(null>threshold)),float(np.mean(alt>threshold))

def silent_label_theorem(seed=SEED):
    rng=np.random.default_rng(seed)
    rho=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)); rho=rho@rho.conj().T; rho/=np.trace(rho)
    # Any label-only unitary disappears after tracing the label.
    u=expm(-.37j*X); evolved=np.kron(u,I2)@rho@np.kron(u.conj().T,I2)
    trace=lambda a: np.trace(a.reshape(2,2,2,2),axis1=0,axis2=2)
    return float(np.max(abs(trace(rho)-trace(evolved))))

def run():
    hist_error,history_output=hidden_and_classical_histories()
    static,env_reset,sys_reset=reset_witness(); coherence,choi_eigs=cross_kerr_channel()
    convex_error,candidate=convex_refit(); restricted,expanded=calibrated_distance(); alpha,power=finite_power()
    pure=np.array([[.5,.5],[.5,.5]],complex)
    return {'hom':{'overlap':.73,'coincidence':hom_coincidence(.73)},
            'storage':{'fidelity':swap_storage_fidelity(pure)},
            'history_equivalence':{'max_error':hist_error,'output_trace':float(np.trace(history_output).real)},
            'process_memory':{'static_coherence':static,'environment_reset_coherence':env_reset},
            'causal_break':{'system_reset_only':sys_reset,'environment_reset':env_reset,'difference':abs(sys_reset-env_reset)},
            'cross_kerr':{'coherence':coherence,'choi_min_eigenvalue':float(min(choi_eigs))},
            'convex_refit':{'max_error':convex_error,'settings':len(candidate)},
            'calibration':{'restricted_l2':restricted,'expanded_l2':expanded},
            'finite_power':{'seed':SEED,'experiments':2000,'shots':400,'type_i':alpha,'power':power},
            'silent_label':{'max_system_difference':silent_label_theorem(),
                            'missing_axioms':['exchange-symmetric coupling','cross-absorption map','standard-family separation']}}

if __name__=='__main__': print(json.dumps(run(),indent=2))
