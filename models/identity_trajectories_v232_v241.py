"""v2.32-v2.41: quantum-jump trajectory and no-signalling audit.
Standard quantum-information toy model, NOT permanent photon identity.
Requires numpy. Execute python -m models.identity_trajectories_v232_v241
"""
import json,math,numpy as np
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Z=np.diag([1,-1]).astype(complex)
GAMMA=.36
K0=np.diag([1,math.sqrt(1-GAMMA)]).astype(complex)
K1=np.array([[0,math.sqrt(GAMMA)],[0,0]],complex)
K=(K0,K1)
PLUS=np.array([1,1],complex)/math.sqrt(2)
BELL=np.array([1,0,0,1],complex)/math.sqrt(2)
def rho(v):return np.outer(v,v.conj())
def channel(a,ks=K):return sum(k@a@k.conj().T for k in ks)
def branches(a,ks=K):
 out=[]
 for k in ks:
  b=k@a@k.conj().T
  p=float(np.trace(b).real)
  out.append((p,b/p if p>1e-12 else np.zeros_like(a)))
 return out
def td(a,b):return float(sum(abs(np.linalg.eigvalsh(a-b)))/2)
def plus(a):return float(np.trace((I+X)/2@a).real)
def partial_alice(a):return np.einsum('abad->bd',a.reshape(2,2,2,2))
def partial_bob(a):return np.einsum('abcb->ac',a.reshape(2,2,2,2))
def bell_bob_channel(a):return sum(np.kron(I,k)@a@np.kron(I,k).conj().T for k in K)
def run():
 a=rho(PLUS)
 b=branches(a)
 other_ks=((K0+K1)/math.sqrt(2),(K0-K1)/math.sqrt(2))
 alt=branches(a,other_ks)
 mixture=lambda x:sum(p*r for p,r in x)
 bell=rho(BELL)
 final=bell_bob_channel(bell)
 alice_gap=td(partial_bob(bell),partial_bob(final))
 bob_gap=td(partial_alice(final),channel(I/2))
 alice_x=np.kron(X,I)
 bob_after_alice_x=partial_alice(alice_x@final@alice_x.conj().T)
 ensemble_z=[(.5,rho(np.array([1,0],complex))),(.5,rho(np.array([0,1],complex)))]
 ensemble_x=[(.5,rho(PLUS)),(.5,rho(np.array([1,-1],complex)/math.sqrt(2)))]
 ea=sum(p*channel(st) for p,st in ensemble_z)
 eb=sum(p*channel(st) for p,st in ensemble_x)
 count=np.random.default_rng(20261118).multinomial(20000,[p for p,_ in b])
 two=channel(channel(a))
 two_branch=sum(p*channel(st) for p,st in b)
 return {
 'v2.32':{'Kraus_completeness_error':float(np.max(abs(sum(k.conj().T@k for k in K)-I)))},
 'v2.33':{'jump_probability':b[1][0],'no_jump_probability':b[0][0]},
 'v2.34':{'ensemble_reconstruction_gap':td(mixture(b),channel(a)),'plus_probability':plus(channel(a))},
 'v2.35':{'other_unraveling_outcome_probabilities':[p for p,_ in alt],
   'unconditional_gap':td(mixture(b),mixture(alt)),
   'conditional_first_branch_distance':td(b[0][1],alt[0][1])},
 'v2.36':{'Alice_marginal_gap':alice_gap,'Bob_marginal_to_standard_channel':bob_gap},
 'v2.37':{'Bob_marginal_after_Alice_X_gap':td(bob_after_alice_x,partial_alice(final))},
 'v2.38':{'equivalent_input_ensemble_channel_gap':td(ea,eb)},
 'v2.39':{'seed':20261118,'n':20000,'jump_count':int(count[1]),'expected_jump_count':20000*b[1][0]},
 'v2.40':{'two_step_channel_trajectory_gap':td(two,two_branch),'two_step_plus_probability':plus(two)},
 'v2.41':{'identity_specific_prediction':False,'is_standard_quantum_trajectory':True,'QED_theory_proven':False}}
if __name__=='__main__':print(json.dumps(run(),indent=2,ensure_ascii=False))
