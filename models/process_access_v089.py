"""v0.89: two-step qubit process with fixed vs fresh classical environment memory.
Operationally complete 16 CP branches x 4 output effects; NOT QED.
"""
import numpy as np
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
P0=np.diag([1,0]).astype(complex)
P1=np.diag([0,1]).astype(complex)
KETS=[np.array([1,0],complex),np.array([0,1],complex),
      np.array([1,1],complex)/np.sqrt(2),np.array([1,1j],complex)/np.sqrt(2)]
EFFECTS=[np.outer(v,v.conj()) for v in KETS]

def kraus(prep,effect):
    return np.outer(KETS[prep],KETS[effect].conj())

def instrument_outcome(rho,K):
    return K@rho@K.conj().T

def process_output(K,correlated=True,relabel=False,rho=P0):
    rho=np.asarray(rho,complex);K=np.asarray(K,complex)
    if rho.shape!=(2,2) or K.shape!=(2,2):
        raise ValueError('qubit matrices required')
    ans=np.zeros((2,2),complex)
    for a in (0,1):
        for b in (0,1):
            if correlated and a!=b:continue
            w=.5 if correlated else .25
            aa=1-a if relabel else a
            bb=1-b if relabel else b
            U1=I if aa==0 else X
            U2=I if bb==0 else X
            t=U2@K@U1
            ans+=w*t@rho@t.conj().T
    return ans

def probability(K,final_effect,correlated=True,relabel=False,rho=P0):
    return float(np.trace(np.asarray(final_effect)@
        process_output(K,correlated,relabel,rho)).real)

def no_intervention(rho=P0,correlated=True):
    return process_output(I,correlated,rho=rho)

def tomography_signature(correlated=True,relabel=False,rho=P0):
    return np.array([probability(kraus(p,e),EFFECTS[f],correlated,relabel,rho)
        for p in range(4) for e in range(4) for f in range(4)])

def trace_distance(a,b):
    return float(np.sum(np.abs(np.linalg.eigvalsh(a-b)))/2)

def single_step(rho):
    return (rho+X@rho@X)/2

def outcome_reset(effect_index,prepared_index=0,correlated=True):
    result=process_output(kraus(prepared_index,effect_index),correlated)
    p=float(np.trace(result).real)
    return (p,result/p) if p>0 else (p,None)

def gram_rank_hermitian(operators):
    G=np.array([[np.trace(A@B).real for B in operators] for A in operators])
    return int(np.linalg.matrix_rank(G,tol=1e-10)),np.linalg.eigvalsh(G)

def informational_completeness():
    rs,sg=gram_rank_hermitian(EFFECTS)
    cp=[]
    for p in range(4):
        for e in range(4):
            v=kraus(p,e).reshape(4)
            cp.append(np.outer(v,v.conj()))
    ri,ig=gram_rank_hermitian(cp)
    return {'final_effect_span_rank':rs,'instrument_choi_span_rank':ri,
        'joint_linear_span_rank':ri*rs,
        'min_final_gram_eigenvalue':float(sg.min()),
        'min_instrument_gram_eigenvalue':float(ig.min())}

def summary():
    fixed=tomography_signature(True)
    fresh=tomography_signature(False)
    rewrite=tomography_signature(True,True)
    a=no_intervention(correlated=True)
    b=no_intervention(correlated=False)
    p0,r0=outcome_reset(0,0,True)
    _,r0fresh=outcome_reset(0,0,False)
    p1,r1=outcome_reset(1,0,True)
    return {'version':'v0.89','single_step_channel_zero':single_step(P0).real.tolist(),
        'two_step_fixed_p0':float(np.trace(P0@a).real),
        'two_step_fresh_p0':float(np.trace(P0@b).real),
        'two_step_trace_distance':trace_distance(a,b),
        'causal_break_outcome_0':{'occurrence_probability':p0,
           'fixed_conditional_future_p0':float(np.trace(P0@r0).real),
           'fresh_conditional_future_p0':float(np.trace(P0@r0fresh).real)},
        'causal_break_outcome_1':{'occurrence_probability':p1,
           'fixed_conditional_future_p1':float(np.trace(P1@r1).real)},
        'tomography':{**informational_completeness(),
            'number_observables':len(fixed),
            'max_label_rewrite_error':float(np.max(np.abs(fixed-rewrite))),
            'max_fixed_vs_fresh_probability_difference':float(np.max(np.abs(fixed-fresh))),
            'rms_fixed_vs_fresh_probability_difference':float(np.sqrt(np.mean((fixed-fresh)**2)))},
        'caveat':'Process-tensor toy qubit memory; not a photon QED or permanent identity proof.'}
