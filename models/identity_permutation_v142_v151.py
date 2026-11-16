"""v1.42-v1.51: permutation and HOM operational-identity audit.
Finite-dimensional demonstrations only. NumPy required; not a QED prediction.
"""
import math,json
import numpy as np
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Z=np.diag([1,-1]).astype(complex)
S=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],complex)
Q=(np.eye(4)+S)/2
a=np.array([0,1,0,0],complex);b=S@a
s=(a+b)/np.sqrt(2)
O=np.kron(Z,I);A=(O+np.kron(I,Z))/2
def norm(x):return float(np.linalg.norm(x))
def hom(z):
    if abs(z)>1:raise ValueError("overlap must be <=1")
    return (1-abs(z)**2)/2
def kl(p,q):
    if p==q:return 0.
    if not 0<p<1 or not 0<q<1:return float("inf")
    return p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))
def run():
    H=np.kron(X,I)+np.kron(I,X)+.35*np.kron(Z,Z)
    phase=complex(math.cos(.53),math.sin(.53))
    val={
    "v1.42":{"labeled_dim":4,"boson_dim":int(np.linalg.matrix_rank(Q)),"swap_gap":norm(S@s-s)},
    "v1.43":{"symmetrized_relabel_gap":norm(Q@a-Q@b)},
    "v1.44":{"slot_observable_commutator":norm(O@S-S@O),"symmetric_commutator":norm(A@S-S@A),"projected_difference":norm(Q@O@Q-Q@A@Q)},
    "v1.45":{"hom_overlap_0":hom(0),"hom_overlap_06":hom(.6),"hom_overlap_1":hom(1)},
    "v1.46":{"relative_mode_phase_modulus_gap":abs(hom(.6*complex(math.cos(.7),math.sin(.7)))-hom(.6)),"global_phase_density_gap":norm(np.outer(s*phase,np.conjugate(s*phase))-np.outer(s,np.conjugate(s)))},
    "v1.47":{"orthogonal_internal_HOM":hom(0),"same_internal_HOM":hom(1)},
    "v1.48":{"symmetric_H_commutator":norm(H@S-S@H),"slot_specific_H_commutator":norm(O@S-S@O)},
    "v1.49":{"projected_slot_vs_symmetrized_gap":norm(Q@O@Q-Q@A@Q),"symmetric_coupling_norm":norm(Q@A@Q)},
    "v1.50":{"candidate_probability":hom(.7),"standard_refit_probability":hom(.7),"profiled_KL":kl(hom(.7),hom(.7)),"fixed_reference_KL":kl(hom(.7),hom(.6))},
    "v1.51":{"lorentz_covariance_verified":False,"gauge_consistency_verified":False,"identity_specific_prediction":False}}
    return val
if __name__=="__main__":print(json.dumps(run(),ensure_ascii=False,indent=2))
