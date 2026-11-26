"""Environment information, feedback and probabilistic reversal of qubit noise."""
import json
import numpy as np
from v1072_v1081.model import I,X,Y,Z,PAULI
from v1082_v1091.model import branches

def best(record):
    return float(np.max(record,axis=1).sum())

def damping(g):
    return [np.diag([1,np.sqrt(1-g)]),np.array([[0,np.sqrt(g)],[0,0]])]

def fidelity(ops):
    return float(sum(abs(np.trace(k))**2 for k in ops)/4)

def run():
    flags=branches()
    # Bit records whether the error interchanges computational letters.
    partition=np.array([[.25,0,0,.25],[0,.25,.25,0]])
    g=.36
    K,J=damping(g)
    recovery=np.diag([np.sqrt(1-g),1.])
    # Monitoring in the rotated basis of the uniform I/Z error purification.
    dark=(I-Z)/2;bright=(I+Z)/2
    overlap=.6
    r=.72
    # Same single-trial bit error .15; comparing an independent re-sample with a persistent flip.
    err=.15
    # Equal Fe, radically different worst input survival: depolarizing vs Z errors.
    p=.24
    return dict(order_flag=dict(posterior_F=best(flags),no_record=best(flags.sum(axis=0)[None,:]),full_tag=best(np.diag(flags.sum(axis=0)))),
                parity_only=dict(Fe=best(partition),Z_letter=1.,X_letter=.5),
                imperfect_marker=dict(overlap=overlap,optimal_Fe=(1+np.sqrt(1-overlap**2))/2),
                unambiguous=dict(accepted=1-overlap,conditional_Fe=1.,filled_Fe=1-overlap/2),
                repeat_read=dict(both_wrong_independent=err**2,both_wrong_shared=err,
                                 accepted_independent=(1-err)**2+err**2,
                                 conditional_independent=err**2/((1-err)**2+err**2)),
                basis_choice=dict(projective_Fe=fidelity([bright,dark]),error_basis_Fe=fidelity([I/np.sqrt(2),I/np.sqrt(2)])),
                nonunital=dict(shift=float(np.linalg.norm(K@K.T+J@J.T-I,2)),best_count_unitary_Fe=(sum(np.linalg.svd(K,compute_uv=False))**2+g)/4),
                heralded_inverse=dict(success=float(np.trace((recovery@K).T@(recovery@K))/2),reverse_error=float(np.linalg.norm(recovery@K-np.sqrt(1-g)*I))),
                missing_tags=dict(F=r+(1-r)/4,certify_threshold=1/3),
                heldout=dict(Fe=1-p,Z_noise_z=1.,Z_noise_x=1-p,isotropic_survival=1-2*p/3))
if __name__=='__main__':print(json.dumps(run(),indent=2))
