"""v0.91 — resonant single-excitation photon absorption and re-emission.

Basis |g,1a,0b>, |e,0a,0b>, |g,0a,1b>. Switched Jaynes-Cummings
couplings model reversible cavity transfer, not generic spontaneous emission.
Not evidence that a historical photon label persists.
"""
import numpy as np
from scipy.linalg import expm

A=np.array([1,0,0],complex)
E=np.array([0,1,0],complex)
B=np.array([0,0,1],complex)
I=np.eye(3,dtype=complex)
N_A=np.diag([1,0,0]).astype(complex)
N_B=np.diag([0,0,1]).astype(complex)
N_PHOTON=N_A+N_B
N_ATOM=np.diag([0,1,0]).astype(complex)
N_EXCITATION=N_PHOTON+N_ATOM

def coupling(mode='a',g=1.):
    if mode not in ('a','b') or g<=0:raise ValueError('mode a/b, g>0 required')
    j=0 if mode=='a' else 2
    H=np.zeros((3,3),complex)
    H[1,j]=H[j,1]=g
    return H

def pulse(mode='a',area=np.pi/2,g=1.):
    return expm(-1j*coupling(mode,g)*area/g)

def commutator(x,y):
    return x@y-y@x

def expectation(psi,operator):
    psi=np.asarray(psi,complex)
    if psi.shape!=(3,):raise ValueError('three-amplitude ket required')
    return float(np.vdot(psi,operator@psi).real)

def trajectory(absorption=np.pi/2,emission=np.pi/2):
    stored=pulse('a',absorption)@A
    return {'input':A.copy(),'stored':stored,'output':pulse('b',emission)@stored}

def observables(psi):
    return {'P_a':expectation(psi,N_A),'P_e':expectation(psi,N_ATOM),
        'P_b':expectation(psi,N_B),
        'photon_count':expectation(psi,N_PHOTON),
        'excitation_count':expectation(psi,N_EXCITATION)}

def full_fock_operators():
    """Atom (g,e) x Fock a(0,1) x Fock b(0,1): 8D check."""
    i=np.eye(2,dtype=complex)
    n=np.diag([0,1]).astype(complex)
    low=np.array([[0,1],[0,0]],complex)
    raising=low.conj().T
    op=lambda a,b,c: np.kron(np.kron(a,b),c)
    at=op(n,i,i); na=op(i,n,i);nb=op(i,i,n)
    ha=op(raising,low,i)+op(low,raising,i)
    hb=op(raising,i,low)+op(low,i,raising)
    return dict(atom=at,na=na,nb=nb,Nexc=at+na+nb,ha=ha,hb=hb)

def damped_emission_kraus(theta):
    return (np.diag([1,np.cos(theta)]).astype(complex),
        np.array([[0,-1j*np.sin(theta)],[0,0]],complex))

def atom_emission_channel(rho,theta):
    rho=np.asarray(rho,complex)
    if rho.shape!=(2,2):raise ValueError('atomic rho must be 2x2')
    return sum(k@rho@k.conj().T for k in damped_emission_kraus(theta))

def coherent_transfer_reference(alpha=1/np.sqrt(2),beta=1/np.sqrt(2)):
    if not np.isclose(abs(alpha)**2+abs(beta)**2,1):raise ValueError('normalized')
    ua=np.eye(4,dtype=complex);ub=ua.copy()
    ua[:3,:3]=pulse('a');ub[:3,:3]=pulse('b')
    initial=np.array([alpha,0,0,beta],complex)
    return {'initial':initial,'output':ub@ua@initial,
        'expected':np.array([0,0,-alpha,beta],complex)}

def spectator_label_probability(tag):
    tag=np.asarray(tag,complex)
    if tag.ndim!=1 or len(tag)<2 or not np.isclose(np.vdot(tag,tag),1):
        raise ValueError('normalized auxiliary tag required')
    u=pulse('b')@pulse('a')
    joint=np.kron(u,np.eye(len(tag)))@np.kron(A,tag)
    return np.array([
        np.vdot(joint,np.kron(np.diag([int(i==j) for i in range(3)]),np.eye(len(tag)))@joint).real
        for j in range(3)])

def summary():
    out={'version':'v0.91','stages':{},
        'commutator_Ha_Nexc_8D':0.,'commutator_Hb_Nexc_8D':0.,
        'commutator_Ha_Nphoton_8D':0.,'Kraus_completeness_error':0.}
    for stage,psi in trajectory().items():
        out['stages'][stage]={**observables(psi),
            'amplitudes':[[float(z.real),float(z.imag)] for z in psi]}
    op=full_fock_operators()
    for mode in ('a','b'):
        out[f'commutator_H{mode}_Nexc_8D']=float(np.linalg.norm(commutator(op[f'h{mode}'],op['Nexc'])))
    out['commutator_Ha_Nphoton_8D']=float(np.linalg.norm(commutator(op['ha'],op['na']+op['nb'])))
    k0,k1=damped_emission_kraus(np.pi/4)
    out['Kraus_completeness_error']=float(np.linalg.norm(k0.conj().T@k0+k1.conj().T@k1-np.eye(2)))
    out['coherence_transfer_error']=float(np.linalg.norm(coherent_transfer_reference()['output']-coherent_transfer_reference()['expected']))
    out['tag0']=spectator_label_probability([1,0]).tolist()
    out['tag_plus']=spectator_label_probability([1/np.sqrt(2)]*2).tolist()
    out['scientific_status']='RWA toy model; no historical photon identity observable or novel QED prediction'
    return out

if __name__=='__main__':
    import json
    print(json.dumps(summary(),ensure_ascii=False,indent=2))
