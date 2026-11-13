import numpy as np
def kraus(g):
    if not 0<=g<=1: raise ValueError('gamma')
    return [np.diag([1,np.sqrt(1-g)]).astype(complex),np.array([[0,np.sqrt(g)],[0,0]],complex)]
def isometry(g): return np.vstack(kraus(g))
def channel_from_isometry(v,rho,env_dim):
    d=rho.shape[0]
    joint=(v@rho@v.conj().T).reshape(env_dim,d,env_dim,d)
    return np.einsum('aiaj->ij',joint)
def environment_rotate(v,u): return np.kron(u,np.eye(v.shape[1]))@v
def choi_rank(g):
    k=kraus(g)
    j=sum(np.outer(x.reshape(-1,order='F'),x.reshape(-1,order='F').conj()) for x in k)
    return int(np.sum(np.linalg.eigvalsh(j)>1e-10))
def extra_identity(v,identity_state):
    a=np.asarray(identity_state,complex)
    if a.ndim!=1 or not np.isclose(np.vdot(a,a),1): raise ValueError('normalized state required')
    return np.kron(np.kron(np.eye(2),a.reshape(-1,1)),np.eye(2))@v
def phase_unitary(phi):
    return np.array([[np.cos(phi),-np.sin(phi)],[np.sin(phi),np.cos(phi)]],complex)
