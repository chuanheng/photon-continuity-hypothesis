"""v0.76: neutral complex scalar EFT checks and independent finite-mode toy.
Not full QED; not proof of photon identity.
"""
import numpy as np
ETA=np.diag([1.,-1.,-1.,-1.])
def ladder(d):
    if d<2: raise ValueError('dimension')
    a=np.zeros((d,d),complex)
    for n in range(1,d):a[n-1,n]=np.sqrt(n)
    return a
def number(d): return np.diag(np.arange(d)).astype(complex)
def commutator(a,b):return a@b-b@a
def model(photon_dim=4,carrier_dim=3,omega=1.,mass=1.3,g=0.2):
    a=ladder(photon_dim)
    ia=np.eye(photon_dim);ib=np.eye(carrier_dim)
    q=np.kron(ia,number(carrier_dim))
    nph=np.kron(number(photon_dim),ib)
    h=omega*nph+mass*q+g*np.kron(a+a.conj().T,number(carrier_dim))
    return h,q,nph
def propagate(h,initial,t):
    eig,vec=np.linalg.eigh(h)
    return (vec*np.exp(-1j*eig*t))@vec.conj().T@initial
def field_strength(k,eps):
    k=np.asarray(k,float);eps=np.asarray(eps,float)
    if k.shape!=(4,) or eps.shape!=(4,):raise ValueError('4-vectors')
    return np.outer(k,eps)-np.outer(eps,k)
def contract_f_squared(f):
    f=np.asarray(f,float)
    if f.shape!=(4,4):raise ValueError('tensor')
    return float(np.einsum('mn,mp,nq,pq->',f,ETA,ETA,f))
def boost_z(r):
    c,s=np.cosh(r),np.sinh(r)
    return np.array([[c,0,0,s],[0,1,0,0],[0,0,1,0],[s,0,0,c]])
def noether_density(amplitude,frequency):return 2*frequency*abs(amplitude)**2
def dimension(term):return {'S':1,'SdagS':2,'F':2,'F2':4,'SdagS_F2':6,'S_F2':5}[term]
def charge_balance(term):return {'S':1,'Sdag':-1,'SdagS':0,'S_F2':1,'SdagS_F2':0,'S2':2,'Sdag2':-2}[term]
def summary():
    h,q,nph=model()
    k=np.array([2.,.2,.3,1.5]);eps=np.array([.1,.3,-.4,.2])
    f=field_strength(k,eps);l=boost_z(.7)
    return {'carrier_charge_commutator':float(np.linalg.norm(commutator(h,q))),
      'photon_number_commutator':float(np.linalg.norm(commutator(h,nph))),
      'f2':contract_f_squared(f),'f2_boosted':contract_f_squared(l@f@l.T),
      'carrier_current_density_at_A1_w2':noether_density(1,2),
      'operator_dimension':dimension('SdagS_F2')}
