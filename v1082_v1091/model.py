"""Flagged Pauli channels: communication and entanglement-breaking boundaries."""
import json
import numpy as np
from scipy.optimize import brentq
from v1072_v1081.model import PAULI

def branches(v=0.,shared=0.):
    weights=np.array([1+3*v,1-v,1-v,1-v])/4
    joint=(1-shared)*np.outer(weights,weights)+shared*np.diag(weights)
    flags=np.zeros((2,4))
    for i,a in enumerate(PAULI):
        for j,b in enumerate(PAULI):
            prod=a@b
            index=np.argmax([abs(np.trace(p.conj().T@prod)) for p in PAULI])
            sign=int(np.linalg.norm(prod-b@a)>1.)
            flags[sign,index]+=joint[i,j]
    return flags

def bell_pt(weights):
    bell=np.eye(2).ravel()/np.sqrt(2)
    J=np.zeros((4,4),complex)
    for w,p in zip(weights,PAULI):
        ket=np.kron(np.eye(2),p)@bell
        J+=w*np.outer(ket,ket.conj())
    return np.linalg.eigvalsh(J.reshape(2,2,2,2).transpose(0,3,2,1).reshape(4,4))

def success(flags):
    # Orthogonal computational-basis letters. I and Z preserve; X and Y flip.
    return float(sum(max(row[0]+row[3],row[1]+row[2]) for row in flags))

def run():
    flags=branches()
    normalized=flags/flags.sum(axis=1)[:,None]
    e=.2
    mixed=np.array([[1-e,e],[e,1-e]])@flags
    def margin(v=0.,shared=0.):
        plus=branches(v,shared)[0]
        return 2*max(plus)-sum(plus)
    vcrit=brentq(margin,0,.8)
    wcrit=brentq(lambda w:margin(shared=w),0,.5)
    return dict(choi=dict(branches=normalized.tolist(),pt_min=[float(min(bell_pt(row))) for row in normalized]),
                single_use=dict(with_flag=success(flags),ignored=success(flags.sum(axis=0)[None,:])),
                noisy_flag=dict(error=e,success=success(mixed),hidden=success(np.ones((2,2))@flags/2)),
                noise_boundary=dict(vcrit=vcrit,serial=np.sqrt(1/3),individual_EB=1/3),
                shared_boundary=dict(wcrit=wcrit,example=.15,
                    plus_pt=float(min(bell_pt(branches(shared=.15)[0]))),
                    serial_pt=float(min(bell_pt(branches(shared=.15).sum(axis=0))))))
if __name__=='__main__':print(json.dumps(run(),indent=2))
