"""Correlated private flags and controls for the proposed four-probe experiment."""
import json
import numpy as np
from scipy.optimize import brentq
from v972_v981.model import SINGLET,T,table
from .model import run as prefix, mix

TARGET=-.093/8

def observed_flags(e,q,sensitivity,false):
    matrix=np.array([[1-false,1-sensitivity],[false,sensitivity]])
    true=np.array([[1-2*e+q,e-q],[e-q,q]])
    return matrix@true@matrix.T

def run():
    prev=prefix()
    scores=prev['independent']['sectors']
    e=.03
    q=brentq(lambda x:mix(scores,e,x)-TARGET,e**2,e)
    edge=brentq(lambda x:mix(scores,x,x*x)-TARGET,.03,.04)
    # Hidden shared history carries both locally generated flag values in advance.
    history=mix([0,-.25,-.25,-.5],e,e**2)
    obs=observed_flags(e,q,.8,.002)
    matrix=np.array([[.998,.2],[.002,.8]])
    inv=np.linalg.inv(matrix)
    margin=prev['independent_enclosure']['lower']-TARGET
    n=int(np.ceil(144*np.log(20)/(2*margin**2)))
    # Material storage: encode into ancilla, depolarize there, read back.
    swap=np.eye(4)[[0,2,1,3]]
    unitary=np.kron(np.eye(2),swap)
    stored=unitary@np.kron(SINGLET,np.diag([1,0]))@unitary.T
    z=np.diag([1,-1])
    phase=np.kron(np.eye(4),z)
    vis=.73
    # Apply a stochastic phase flip to the material qubit.
    returned=unitary@((1+vis)*stored/2+(1-vis)*phase@stored@phase/2)@unitary.T
    output=np.trace(returned.reshape(4,2,4,2),axis1=1,axis2=3)
    direct=np.kron(np.eye(2),z)
    candidate=(1+vis)*SINGLET/2+(1-vis)*direct@SINGLET@direct/2
    return dict(prefix=prev,joint_crossing=dict(q=q,pearson=(q-e*e)/(e*(1-e)), necessary_pearson=margin/(prev['independent_enclosure']['lower']+e/2)),
                independent_feasible_rate=edge,history_score=history,
                monitor=dict(observed_joint=float(obs[1,1]),recovered_joint=float((inv@obs@inv.T)[1,1]),condition=float(np.linalg.cond(matrix)**2)),
                finite_trials=dict(margin=margin,N=n),
                heldout=dict(max_table_error=float(abs(table(candidate)-table(output)).max()),
                             test_input_error=float(np.linalg.norm(candidate-output))))
if __name__=='__main__': print(json.dumps(run(),indent=2))
