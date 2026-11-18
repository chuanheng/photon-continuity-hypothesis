"""v2.42-v2.51: two-boson hidden label identifiability audit.
Synthetic quantum-optics math; no physical evidence for permanent identity.
"""
import json, math
import numpy as np
Q=.81
S=.64
N=10000
SEED=20261118
def overlap_state(fidelity):
    if not 0<=fidelity<=1: raise ValueError('fidelity outside [0,1]')
    return np.array([math.sqrt(fidelity),math.sqrt(1-fidelity)],complex)
def hom_explicit(u,v):
    amplitude=(np.outer(u,v)-np.outer(v,u))/2
    return float(np.sum(abs(amplitude)**2).real)
def hom(q,s):
    return .5*(1-q*s)
def kl(p,r):
    if p==r:return 0.
    return p*math.log(p/r)+(1-p)*math.log((1-p)/(1-r))
def fisher(q,s,n=N):
    p=hom(q,s)
    grad=np.array([-s/2,-q/2])
    return n*np.outer(grad,grad)/(p*(1-p))
def run():
    visible_1=np.array([1,0],complex)
    visible_2=overlap_state(Q)
    label_1=np.array([1,0],complex)
    label_2=overlap_state(S)
    u=np.kron(visible_1,label_1)
    v=np.kron(visible_2,label_2)
    p=hom_explicit(u,v)
    original_overlap=float(abs(np.vdot(u,v))**2)
    standard_u=np.array([1,0],complex)
    standard_v=overlap_state(Q*S)
    standard_p=hom_explicit(standard_u,standard_v)
    f=fisher(Q,S)
    p_ref=(1-Q)/2
    reference=np.zeros((2,2))
    reference[0,0]=N*.25/(p_ref*(1-p_ref))
    full=f+reference
    eye=np.eye(2)
    z=np.diag([1,-1])
    swap=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],float)
    slot=np.kron(z,eye)
    sym=(slot+np.kron(eye,z))/2
    label_proj=float(abs(np.vdot(label_1,label_2))**2)
    rng=np.random.default_rng(SEED)
    observed=int(rng.binomial(N,p))
    settings=[.81,.64]
    return {
      'v2.42':{'squared_visible_overlap':Q,'squared_label_overlap':S,'joint_overlap':original_overlap},
      'v2.43':{'explicit_HOM_coincidence':p,'closed_form_coincidence':hom(Q,S),'amplitude_gap':abs(p-hom(Q,S))},
      'v2.44':{'standard_effective_overlap':Q*S,'ordinary_model_coincidence':standard_p,'operational_gap':abs(p-standard_p)},
      'v2.45':{'single_setting_fisher_eigenvalues':np.linalg.eigvalsh(f).tolist(),'single_setting_fisher_determinant':float(np.linalg.det(f))},
      'v2.46':{'two_settings_visible_overlaps':settings,'candidate_coincidences':[hom(q,S) for q in settings],'standard_effective_overlaps':[q*S for q in settings],'profiled_KL':0.0},
      'v2.47':{'reference_ideal_visible_overlap':Q,'reference_probability':p_ref,'joint_fisher_eigenvalues':np.linalg.eigvalsh(full).tolist(),'joint_fisher_determinant':float(np.linalg.det(full))},
      'v2.48':{'label_projector_outcome_if_accessible':label_proj,'label_projector_ordinary_internal_mode_interpretation':label_proj,'label_identity_exclusive':False},
      'v2.49':{'slot_swap_commutator_norm':float(np.linalg.norm(slot@swap-swap@slot)),'symmetric_operator_commutator_norm':float(np.linalg.norm(sym@swap-swap@sym))},
      'v2.50':{'n_trials':N,'random_seed':SEED,'observed_coincidences':observed,'candidate_probability':p,'KL_vs_fixed_visible_only':kl(p,hom(Q,1)),'KL_vs_refitted_standard':0.0},
      'v2.51':{'novel_photon_identity_prediction':False,'gauge_lorentz_consistency_proven':False,'label_cross_absorption_observable_defined':False}
    }
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
