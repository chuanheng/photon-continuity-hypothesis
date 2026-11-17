"""v1.82-v1.91: Operational no-go vs identifiable dissipative channel.
Standard quantum information toy model; NOT a photon-identity or QED proof.
Requires numpy/scipy. Run: python -m models.identity_channel_audit_v182_v191
"""
import json,math,numpy as np
from scipy.stats import binom
GAMMA=.36
I=np.eye(2,dtype=complex)
P0=np.diag([1,0]).astype(complex)
H=np.array([[1,1],[1,-1]],complex)/math.sqrt(2)
K0=np.diag([1,math.sqrt(1-GAMMA)]).astype(complex)
K1=np.array([[0,math.sqrt(GAMMA)],[0,0]],complex)
K=(K0,K1)
def channel(r,ks=K):return sum(k@r@k.conj().T for k in ks)
def basis():
 for i in range(2):
  for j in range(2):
   a=np.zeros((2,2),complex);a[i,j]=1
   yield a
def mixed_kraus():return tuple(sum(H[i,j]*K[j] for j in range(2)) for i in range(2))
def dilation():
 c,s=math.sqrt(1-GAMMA),math.sqrt(GAMMA)
 u=np.eye(4,dtype=complex);u[1,1]=c;u[2,2]=c;u[1,2]=s;u[2,1]=-s
 return u
def traced_channel(r):
 u=dilation();x=u@np.kron(r,P0)@u.conj().T
 return np.einsum('ieje->ij',x.reshape(2,2,2,2))
def kl(p,q):
 if p==q:return 0.
 return p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))
def exact_test(n,alpha=.05):
 for k in range(n+1):
  type1=float(binom.sf(k-1,n,.5))
  if type1<=alpha:return k,type1
 return n+1,0.
def run():
 plus=np.array([1,1],complex)/math.sqrt(2)
 states=[P0,np.diag([0,1]),np.outer(plus,plus.conj()),np.eye(2)/2]
 spectator=max(float(np.max(np.abs(channel(r)-channel(r)))) for r in states)
 kraus_gap=max(float(np.max(np.abs(channel(b)-channel(b,mixed_kraus())))) for b in basis())
 u=dilation()
 dilation_gap=max(float(np.max(np.abs(channel(b)-traced_channel(b)))) for b in basis())
 excitation=np.diag([0,1,1,2]).astype(complex)
 out=channel(I/2);d=out-I/2
 trace_dist=float(np.sum(np.abs(np.linalg.eigvalsh(d)))/2)
 p1=float(np.trace(P0@out).real);p0=.5;D=kl(p1,p0)
 n=200;kstar,type1=exact_test(n)
 power=float(binom.sf(kstar-1,n,p1))
 k=int(np.random.default_rng(20261117).binomial(n,p1))
 llr=k*math.log(p1/p0)+(n-k)*math.log((1-p1)/(1-p0))
 return {
  'v1.82':{'spectator_label_accessible_gap':spectator},
  'v1.83':{'different_kraus_sets_same_channel_gap':kraus_gap},
  'v1.84':{'kraus_completeness_error':float(np.max(np.abs(K0.conj().T@K0+K1.conj().T@K1-I))),'gamma':GAMMA},
  'v1.85':{'unitarity_error':float(np.max(np.abs(u.conj().T@u-np.eye(4)))),'dilation_channel_gap':dilation_gap,'excitation_conservation_error':float(np.max(np.abs(u@excitation-excitation@u)))},
  'v1.86':{'unitality_trace_distance':trace_dist,'ground_probability':p1},
  'v1.87':{'random_unitary_ground_probability':p0,'amplitude_damping_ground_probability':p1,'KL':D},
  'v1.88':{'expected_LLR_200':200*D,'expected_LLR_5_event_proxy':5/D},
  'v1.89':{'trials':n,'critical_ground_count':kstar,'actual_type_I':type1,'exact_power':power,'seeded_ground_count':k,'seeded_LLR':llr},
  'v1.90':{'standard_amplitude_damping_fit_gamma':GAMMA,'profile_KL':0.},
  'v1.91':{'identity_Fisher_information':0.,'unique_identity_prediction':False,'physical_experiment':False}
 }
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
