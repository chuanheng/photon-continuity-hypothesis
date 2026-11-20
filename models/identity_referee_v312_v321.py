"""v3.12-v3.21 adversarial review: explicit feedback counterexample.
Standard quantum information toy models, not photon identity evidence.
"""
import numpy as np,math,json
from scipy.stats import binom
I=np.eye(2,dtype=complex);Z=np.diag([1,-1]).astype(complex)
X=np.array([[0,1],[1,0]],complex);P0=np.diag([1,0]).astype(complex);P1=np.diag([0,1]).astype(complex)
U=np.zeros((4,4),complex)
for s in range(2):
 for e in range(2):U[(s^e)*2+e,s*2+e]=1
def td(a,b):return float(np.linalg.norm(a-b,ord='nuc')/2)
def trace_e(r):return np.einsum('ae be->ab',r.reshape(2,2,2,2))
def joint(anti=False):
 r=np.zeros((4,4),complex)
 for s in (0,1):
  e=s^int(anti);v=np.kron(np.eye(2)[s],np.eye(2)[e])
  r+=np.outer(v,v.conj())/2
 return r
def out(r):return trace_e(U@r@U.conj().T)
def hom(a,b):return (1-float(np.trace(a@b).real))/2
def kl(p,q):return p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))
def calc():
 a,b=joint(),joint(True);a1,b1=out(a),out(b)
 plus=np.array([1,1],complex)/math.sqrt(2);pplus=np.outer(plus,plus.conj())
 minus=Z@pplus@Z
 E=lambda x:.8*x+.2*Z@x@Z
 q=.81;s=.64;p=(1-q*s)/2;fixed=(1-q)/2;n=200
 crit=next(k for k in range(n+1) if binom.sf(k-1,n,fixed)<=.05)
 A=np.array([[.91,.1],[.09,.9]]);B=np.array([[1.1,.2],[.1,.75]])
 r=np.array([.6,.4]);e=np.array([1.,0.]);R=B@A@np.linalg.inv(B)
 gauge=max(abs(e@np.linalg.matrix_power(A,t)@r-(e@np.linalg.inv(B))@np.linalg.matrix_power(R,t)@(B@r)) for t in range(12))
 return {'v3.12':{'claim_originality_proven':False,'literature_overlap':True},
 'v3.13':{'closed_CPTP_ensemble_gap':td(.5*E(P0)+.5*E(P1),.5*E(pplus)+.5*E(minus))},
 'v3.14':{'same_initial_reduced_gap':td(trace_e(a),trace_e(b)),'feedback_output_gap':td(a1,b1),'feedback_unitarity_gap':float(np.max(abs(U.conj().T@U-np.eye(4))))},
 'v3.15':{'setting_dependent_channel_gap':td(pplus,(pplus+minus)/2)},
 'v3.16':{'same_CPTP_ensemble_gap':td(.5*E(P0)+.5*E(P1),.5*E(pplus)+.5*E(minus))},
 'v3.17':{'mixed_HOM':hom(np.diag([.7,.3]),np.diag([.2,.8])),'candidate_p':p,'standard_refit_p':(1-q*s)/2},
 'v3.18':{'noisy_candidate_p':.02+.98*.85*p,'noisy_standard_p':.02+.98*.85*((1-q*s)/2)},
 'v3.19':{'critical_ge':crit,'size':float(binom.sf(crit-1,n,fixed)),'power':float(binom.sf(crit-1,n,p)),'fixed_KL':kl(p,fixed),'profile_KL':0.},
 'v3.20':{'gauge_probability_gap':gauge,'arbitrary_similarity_physically_CPTP':False},
 'v3.21':{'conditional_not_global_no_go':True,'originality_established':False,'QED_new_dynamics':False,'experiment':False}}
if __name__=='__main__':print(json.dumps(calc(),ensure_ascii=False,indent=2))
