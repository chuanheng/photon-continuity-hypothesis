"""v2.52-v2.61: symmetric bosonic label and probe interaction audit.
Finite-dimensional quantum-information demonstration. Not new photon physics.
Requires numpy. Run python -m models.identity_operator_v252_v261
"""
import json, math
import numpy as np
I=np.eye(2,dtype=complex)
Z=np.diag([1,-1]).astype(complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
S=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],complex)
A=(np.kron(Z,I)+np.kron(I,Z))/2
B=np.kron(Z,I)
P=(np.eye(4)+S)/2
THETA=.8
ZERO=np.array([1,0],complex)
ONE=np.array([0,1],complex)
V00=np.kron(ZERO,ZERO)
V11=np.kron(ONE,ONE)
VPSI=(np.kron(ZERO,ONE)+np.kron(ONE,ZERO))/math.sqrt(2)
def dm(v):return np.outer(v,v.conj())
def maxerr(a,b):return float(np.max(np.abs(a-b)))
def comm(a,b):return a@b-b@a
def U(theta=THETA):
    h=np.kron(A,Y)
    w,v=np.linalg.eigh(h)
    return (v*np.exp(-.5j*theta*w))@v.conj().T
def probe_density(label_state,theta=THETA):
    after=U(theta)@np.kron(label_state,dm(ZERO))@U(theta).conj().T
    return np.einsum('ap aq->pq',after.reshape(4,2,4,2))
def probx(r):return float(np.trace((I+X)/2@r).real)
def probz(r):return float(np.trace((I+Z)/2@r).real)
def bin_kl(p,q):
    if p==q:return 0.
    return p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))
def run():
    rho00,rho11,rhopsi=dm(V00),dm(V11),dm(VPSI)
    mixed=.5*(rho00+rho11)
    p00,p11,p0=map(probe_density,(rho00,rho11,rhopsi))
    pm=probe_density(mixed)
    pcoh=probe_density(dm((V00+V11)/math.sqrt(2)))
    no_coupling_gap=maxerr(
      np.einsum('ap aq->pq',np.kron(rho00,dm(ZERO)).reshape(4,2,4,2)),
      np.einsum('ap aq->pq',np.kron(rho11,dm(ZERO)).reshape(4,2,4,2)))
    rng=np.random.default_rng(20261118)
    n=1000
    count00=int(rng.binomial(n,probx(p00)))
    count11=int(rng.binomial(n,probx(p11)))
    m=.6
    pb=(1+m*math.sin(THETA))/2
    grad=np.array([math.sin(THETA)/2,m*math.cos(THETA)/2])
    F=n*np.outer(grad,grad)/(pb*(1-pb))
    H=np.kron(A,Y)
    free=np.kron(np.eye(4),Z)
    return {
     'v2.52':{'bosonic_subspace_rank':int(np.linalg.matrix_rank(P)),'inaccessible_label_probe_gap':no_coupling_gap},
     'v2.53':{'slot_commutator_fro':float(np.linalg.norm(comm(B,S))),'collective_commutator_fro':float(np.linalg.norm(comm(A,S))),'coupling_commutator_fro':float(np.linalg.norm(comm(H,np.kron(S,I))))},
     'v2.54':{'P_X_plus_00':probx(p00),'P_X_plus_11':probx(p11),'P_X_plus_PSI':probx(p0),'theory_00':(1+math.sin(THETA))/2},
     'v2.55':{'mixture_ensemble_gap':maxerr(pm,.5*(p00+p11)),'probe_trace_00':float(np.trace(p00).real)},
     'v2.56':{'coherent_vs_incoherent_probe_trace_distance':float(np.sum(abs(np.linalg.eigvalsh(pcoh-pm)))/2)},
     'v2.57':{'A_mean_PSI':float(np.trace(A@rhopsi).real),'A_mean_mixture':float(np.trace(A@mixed).real),'P_Z_plus_PSI':probz(p0),'P_Z_plus_mixture':probz(pm),'discriminating_gap':probz(p0)-probz(pm)},
     'v2.58':{'p_single_setting':pb,'fisher_eigenvalues':np.linalg.eigvalsh(F).tolist(),'fisher_rank':int(np.linalg.matrix_rank(F,tol=1e-8))},
     'v2.59':{'trials_per_setting':n,'X_plus_counts_00':count00,'X_plus_counts_11':count11,'single_event_KL_00_vs_11':bin_kl(probx(p00),probx(p11))},
     'v2.60':{'coupling_vs_free_probe_commutator_fro':float(np.linalg.norm(comm(H,free))),'probe_free_energy_conserved':False,'joint_externally_driven':True},
     'v2.61':{'novel_permanent_identity_observable':False,'standard_collective_internal_mode_interpretation':True,'QED_or_Lorentz_consistency_demonstrated':False}
    }
if __name__=='__main__':print(json.dumps(run(),indent=2,ensure_ascii=False))
