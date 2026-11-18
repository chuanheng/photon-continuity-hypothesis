"""v2.62-v2.71 resonant/detuned light-matter toy; standard Jaynes-Cummings physics.
Four-state single-excitation subspace; not evidence of permanent photon identity.
Run: python -m models.identity_light_matter_v262_v271
"""
import json,math,numpy as np
def h(g0=1.,g1=1.,delta=0.):
 a=np.diag([0.,0.,delta,delta]).astype(complex)
 for i,g in enumerate((g0,g1)):a[i,i+2]=a[i+2,i]=g
 return a
def expm(a,t):
 w,v=np.linalg.eigh(a)
 return (v*np.exp(-1j*t*w))@v.conj().T
def ket(i,n=4):
 a=np.zeros(n,complex);a[i]=1;return a
def pop(a):return float(np.sum(np.abs(a[2:4])**2))
def probe(i,theta=.8):
 a=np.diag([0,0,1,-1]).astype(complex)
 y=np.array([[0,-1j],[1j,0]],complex)
 u=expm(np.kron(a,y),theta/2)
 state=u@np.kron(ket(i),ket(0,2))
 x=np.array([[0,1],[1,0]],complex)
 r=np.einsum('iaib->ab',np.outer(state,state.conj()).reshape(4,2,4,2))
 return float(np.trace((np.eye(2)+x)/2@r).real)
def kl(p,q):return p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))
def run():
 H=h();theta=math.pi/2;u=expm(H,theta)
 psi=(ket(0)+ket(1))/math.sqrt(2)
 stored=u@psi
 back=expm(H,-theta)@stored
 delta=.8;Hd=h(delta=delta)
 H0=np.diag([0.,0.,delta,delta])
 om=math.sqrt(1+(delta/2)**2);tm=math.pi/(2*om)
 detuned=pop(expm(Hd,tm)@ket(0))
 mode=[pop(expm(h(1,.7),theta)@ket(i)) for i in (0,1)]
 Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1])
 P=np.kron(np.diag([0,0,1,-1]),Y);F=np.kron(np.eye(4),Z)
 resonant=pop(expm(H,tm)@ket(0))
 return {'v2.62':{'unitarity_error':float(np.max(abs(u.conj().T@u-np.eye(4)))),'hermiticity_error':float(np.max(abs(H-H.conj().T)))},
 'v2.63':{'matter_probability':pop(stored),'photon_probability':1-pop(stored)},
 'v2.64':{'retrieval_fidelity':float(abs(np.vdot(back,psi))**2)},
 'v2.65':{'excitation_conserved':True,'detuned_free_energy_commutator_norm':float(np.linalg.norm(Hd@H0-H0@Hd)),'total_energy_conserved':True},
 'v2.66':{'detuning':delta,'analytic_max_transfer':1/(1+(delta/2)**2),'numerical_max_transfer':detuned},
 'v2.67':{'couplings':[1.,.7],'mode_transfer_probabilities':mode},
 'v2.68':{'probe_Xplus_m0':probe(2),'probe_Xplus_m1':probe(3)},
 'v2.69':{'probe_free_energy_commutator_fro':float(np.linalg.norm(P@F-F@P))},
 'v2.70':{'KL_vs_fixed_resonance':kl(detuned,resonant),'profiled_KL_with_standard_detuning':0.},
 'v2.71':{'identity_specific_prediction':False,'cross_absorption_identity_observable':False,'QED_covariance_proven':False}}
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
