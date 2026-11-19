"""v2.92-v3.01: permutation, hidden-label, gauge and statistical audit.
Standard finite quantum mechanics and a gauge-variation sanity check only.
Not a complete QED theory or evidence for permanent photon identity.
"""
import json,math,numpy as np
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1,-1]).astype(complex)
S=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],complex)
P=(np.eye(4)+S)/2
A=(np.kron(Z,I)+np.kron(I,Z))/2
slot=np.kron(Z,I)
zero=np.array([1,0],complex)
plus=np.array([1,1],complex)/math.sqrt(2)
def dm(v):return np.outer(v,v.conj())
def U(H,t):
 w,v=np.linalg.eigh(H)
 return (v*np.exp(-1j*t*w))@v.conj().T
def c(a,b):return float(np.linalg.norm(a@b-b@a))
def read_probe(label):
 u=U(np.kron(A,Y),.4)
 total=u@np.kron(label,dm(zero))@u.conj().T
 probe=np.einsum('ipiq->pq',total.reshape(4,2,4,2))
 return float(np.trace((I+X)/2@probe).real)
def homo(q,s):return (1-q*s)/2
def kl(p,q):return p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))
def run():
 state=dm(plus)
 label0=dm(zero);label1=dm(np.array([0,1],complex))
 observable=np.kron((I+X)/2,I)
 gap=abs(float(np.trace(observable@np.kron(state,label0)).real-np.trace(observable@np.kron(state,label1)).real))
 bad=np.kron(zero,np.array([0,1],complex))
 good=P@bad;good/=np.linalg.norm(good)
 p00=read_probe(dm(np.kron(zero,zero)))
 p11=read_probe(dm(np.kron(np.array([0,1]),np.array([0,1]))))
 pg=read_probe(dm(good))
 q,s=.81,.64
 p=homo(q,s);standard=homo(q*s,1)
 seed=20261119;counts=int(np.random.default_rng(seed).binomial(10000,p))
 h=np.zeros((4,4),complex)
 h[0,2]=h[2,0]=h[1,3]=h[3,1]=1
 w=U(h,math.pi/2)
 photon=np.array([1,1,0,0],complex)/math.sqrt(2)
 matter=w@photon
 recovered=w.conj().T@matter
 G=np.array([[.2,.5,-.3,.1],[-.4,.8,.7,-.2],[.1,.6,-.1,.9],[-.2,.3,-.8,.4]])
 Hess=np.array([[.4,.1,-.2,.3],[.1,-.3,.2,-.1],[-.2,.2,.5,.4],[.3,-.1,.4,.2]])
 F=G-G.T;Fg=(G+Hess)-(G+Hess).T
 metric=np.diag([1.,-1.,-1.,-1.])
 inv=float(np.trace(metric@F@metric@F.T))
 invg=float(np.trace(metric@Fg@metric@Fg.T))
 a=np.array([.4,-.2,.3,.1]);g=np.array([.1,.4,-.2,.5])
 return {
 'v2.92':{'symmetric_subspace_rank':int(np.linalg.matrix_rank(P)),'projector_error':float(np.max(abs(P@P-P)))},
 'v2.93':{'slot_swap_commutator':c(slot,S),'collective_swap_commutator':c(A,S),'symmetrized_state_swap_error':float(np.linalg.norm(S@good-good))},
 'v2.94':{'silent_label_probability_gap':gap},
 'v2.95':{'collective_probe_P00':p00,'collective_probe_P11':p11,'collective_probe_Psymmetric':pg,'new_identity_mechanism':False},
 'v2.96':{'HOM_label_probability':p,'HOM_standard_mode_probability':standard,'exact_gap':abs(p-standard)},
 'v2.97':{'matter_storage_probability':float(np.sum(abs(matter[2:])**2)),'retrieval_fidelity':float(abs(np.vdot(photon,recovered))**2),'number_conservation_in_subspace':True},
 'v2.98':{'field_strength_gauge_variation':float(np.max(abs(F-Fg))),'F_squared_gauge_variation':abs(inv-invg),'A_squared_variation':abs(a@metric@a-(a+g)@metric@(a+g))},
 'v2.99':{'neutral_scalar_chi_F2_gauge_variation':abs(.7*inv-.7*invg),'new_scalar_field_would_be_extra_physics':True,'permanent_particle_id_encoded':False},
 'v3.00':{'N':10000,'seed':seed,'synthetic_coin_count':counts,'KL_wrong_fixed_baseline':kl(p,homo(q,1)),'KL_complete_internal_mode_baseline':0.},
 'v3.01':{'strict_no_go_under_inaccessible_label_assumptions':True,'global_no_go_for_all_new_theories':False,'identity_unique_prediction':False,'full_QED_consistency_proven':False,'actual_physical_experiment':False}}
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
