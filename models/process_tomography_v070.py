import numpy as np
def kraus(g):
    if not 0<=g<=1: raise ValueError('gamma')
    return [np.diag([1,np.sqrt(1-g)]).astype(complex),np.array([[0,np.sqrt(g)],[0,0]],complex)]
def channel(rho,g):
    rho=np.asarray(rho,complex)
    if rho.shape!=(2,2): raise ValueError('shape')
    return sum(k@rho@k.conj().T for k in kraus(g))
def choi(g):
    result=np.zeros((4,4),complex)
    for i in range(2):
        for j in range(2):
            e=np.zeros((2,2),complex);e[i,j]=1
            result+=np.kron(e,channel(e,g))
    return result
def probe_states():
    return {'zero':np.diag([1,0]).astype(complex),'one':np.diag([0,1]).astype(complex),'plus':np.array([[.5,.5],[.5,.5]],complex),'plus_i':np.array([[.5,-.5j],[.5j,.5]],complex)}
def reconstruct(outputs):
    e00=outputs['zero'];e11=outputs['one']
    a=2*outputs['plus']-e00-e11
    b=2*outputs['plus_i']-e00-e11
    e01=(a+1j*b)/2;e10=(a-1j*b)/2
    return np.block([[e00,e01],[e10,e11]])
def trace_aux(joint):
    return np.trace(np.asarray(joint).reshape(2,2,2,2),axis1=1,axis2=3)
