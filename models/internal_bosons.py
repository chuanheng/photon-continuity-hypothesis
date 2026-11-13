"""v0.67: bosonic internal labels and HOM visibility."""
import numpy as np

def swap_operator(d):
    s=np.zeros((d*d,d*d),complex)
    for i in range(d):
        for j in range(d): s[j*d+i,i*d+j]=1
    return s

def symmetric_projector(d):
    return (np.eye(d*d)+swap_operator(d))/2

def internal_overlap(a,b):
    a=np.asarray(a,complex); b=np.asarray(b,complex)
    if a.ndim!=1 or b.ndim!=1 or a.shape!=b.shape: raise ValueError('shape mismatch')
    if not np.isclose(np.vdot(a,a),1) or not np.isclose(np.vdot(b,b),1): raise ValueError('states must be normalized')
    return float(np.clip(abs(np.vdot(a,b))**2,0,1))

def hom_coincidence(a,b):
    return (1-internal_overlap(a,b))/2

def symmetric_pair(a,b):
    a=np.asarray(a,complex); b=np.asarray(b,complex)
    if a.shape!=b.shape or a.ndim!=1: raise ValueError('shape mismatch')
    if not np.isclose(np.vdot(a,a),1) or not np.isclose(np.vdot(b,b),1): raise ValueError('not normalized')
    v=np.kron(a,b)+np.kron(b,a)
    return v/np.linalg.norm(v)

def number_operator(d,state_index):
    if not 0<=state_index<d: raise ValueError('invalid index')
    p=np.zeros((d,d),complex); p[state_index,state_index]=1
    return np.kron(p,np.eye(d))+np.kron(np.eye(d),p)

def passive_label_equivalence(overlap_squared):
    if not 0<=overlap_squared<=1: raise ValueError('overlap outside [0,1]')
    p=(1-overlap_squared)/2
    return {'ordinary_internal':p,'permanent_identity':p}
