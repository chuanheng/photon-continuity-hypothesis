import numpy as np
def dephase(rho,sectors):
 rho=np.asarray(rho,complex);s=np.asarray(sectors)
 if rho.shape!=(len(s),len(s)):raise ValueError('shape')
 return np.where(s[:,None]==s[None,:],rho,0)
def allowed(a,sectors):
 a=np.asarray(a,complex);s=np.asarray(sectors)
 if a.shape!=(len(s),len(s)):raise ValueError('shape')
 return bool(np.all(np.abs(a[s[:,None]!=s[None,:]])<1e-10))
def trace_distance(a,b):
 return float(np.sum(np.abs(np.linalg.eigvalsh(np.asarray(a)-np.asarray(b))))/2)
def operational_distance(a,b,sectors):
 return trace_distance(dephase(a,sectors),dephase(b,sectors))
def phase_state(phi):
 v=np.array([1,np.exp(1j*phi)],complex)/np.sqrt(2)
 return np.outer(v,v.conj())
