"""v0.88: same one-step channel, distinct two-step hidden-memory statistics.
Known process-tensor insight, not photon QED or novel physics.
"""
import numpy as np
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Z=np.diag([1,-1]).astype(complex)
P0=np.diag([1,0]).astype(complex)
P1=np.diag([0,1]).astype(complex)

def density(state):
    a=np.asarray(state,complex)
    if a.shape!=(2,) or not np.isclose(np.vdot(a,a),1):raise ValueError('unit ket required')
    return np.outer(a,a.conj())

def channel(rho):
    rho=np.asarray(rho,complex)
    if rho.shape!=(2,2):raise ValueError('qubit matrix required')
    return .5*(rho+X@rho@X)

def two_step(rho,intermediate=None,correlated=True):
    """One hidden bit repeated vs independent bits across time."""
    rho=np.asarray(rho,complex)
    if rho.shape!=(2,2):raise ValueError('qubit matrix required')
    u=I if intermediate is None else np.asarray(intermediate,complex)
    if u.shape!=(2,2) or not np.allclose(u.conj().T@u,I):raise ValueError('unitary required')
    out=np.zeros((2,2),complex)
    for r in (0,1):
        for s in (0,1):
            if correlated and r!=s:continue
            weight=.5 if correlated else .25
            xr=I if r==0 else X
            xs=I if s==0 else X
            t=xs@u@xr
            out+=weight*t@rho@t.conj().T
    return out

def trace_distance(a,b):
    return float(np.sum(np.abs(np.linalg.eigvalsh(np.asarray(a)-np.asarray(b))))/2)

def distinguishability(intermediate=None):
    fixed=two_step(P0,intermediate,True)
    fresh=two_step(P0,intermediate,False)
    d=trace_distance(fixed,fresh)
    return {'fixed_output_prob_zero':float(np.trace(P0@fixed).real),
        'fresh_output_prob_zero':float(np.trace(P0@fresh).real),
        'trace_distance':d,
        'optimal_equal_prior_success':.5*(1+d)}

def state_readout_vs_process_readout():
    return {'one_step_channel_of_zero':channel(P0).real.tolist(),
        'two_step_identity_intervention':distinguishability(I),
        'two_step_X_intervention':distinguishability(X),
        'two_step_Z_intervention':distinguishability(Z),
        'note':'A multitime memory witness does not distinguish ordinary memory from an asserted permanent photon identity.'}
