"""v3.02-v3.11: conditional operational no-go + HOM and statistical audits.
Synthetic models only; not QED or permanent photon-identity evidence.
Run: python -m models.identity_paper_audit_v302_v311
"""
import json,math,numpy as np
from scipy.stats import binom
I=np.eye(2);X=np.array([[0,1],[1,0]]);Z=np.diag([1,-1]);S=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
def kl(p,q):return p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q)) if abs(p-q)>1e-14 else 0.
def hom(q,s=1):return (1-q*s)/2
def calc():
 q,s=.81,.64;p=hom(q,s);fixed=hom(q);n=200
 k=next(z for z in range(n+1) if binom.sf(z-1,n,fixed)<=.05)
 sym=(np.eye(4)+S)/2
 slot=np.kron(Z,I);collective=(slot+np.kron(I,Z))/2
 rng=np.random.default_rng(20261120);worst=0.
 for _ in range(100):
  def density(d):
   a=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));t=a@a.conj().T;return t/np.trace(t)
  a,b,c=density(2),density(2),density(2)
  z=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));eff=z@z.conj().T;eff/=np.linalg.eigvalsh(eff).max()+.5
  worst=max(worst,abs(np.trace(np.kron(eff,I)@np.kron(a,b))-np.trace(np.kron(eff,I)@np.kron(a,c))))
 grad=np.array([-s/2,-q/2]);f=n*np.outer(grad,grad)/(p*(1-p))
 settings=[.81,.64,.49,.36]
 e=np.array([1.,0.]);state=np.array([.6,.4]);G=np.array([[.9,.2],[.1,.8]]);B=np.array([[1.2,.1],[0,.8]])
 gauge=max(abs(e@np.linalg.matrix_power(G,i)@state-(e@np.linalg.inv(B))@np.linalg.matrix_power(B@G@np.linalg.inv(B),i)@(B@state)) for i in range(8))
 return {
 'v3.02':{'symmetric_rank':int(np.linalg.matrix_rank(sym)),'projector_error':float(np.max(abs(sym@sym-sym)))},
 'v3.03':{'inert_label_max_gap':float(worst),'scope':'identical accessible marginal, no label feedback'},
 'v3.04':{'candidate_HOM':p,'standard_HOM':hom(q*s),'effective_overlap':q*s},
 'v3.05':{'fisher_rank_analytic':1,'min_eigenvalue_numerical':float(np.linalg.eigvalsh(f)[0])},
 'v3.06':{'settings':settings,'candidate':[hom(x,s) for x in settings],'standard':[hom(x*s) for x in settings]},
 'v3.07':{'n':n,'critical_ge':k,'type_I':float(binom.sf(k-1,n,fixed)),'power':float(binom.sf(k-1,n,p)),'fixed_KL':kl(p,fixed),'profile_KL':0.},
 'v3.08':{'restricted_standard_min_overlap':.7,'restricted_KL':kl(p,hom(.7)),'bound_physically_justified':False},
 'v3.09':{'similarity_gauge_max_probability_gap':float(gauge),'is_representation_not_CPTP_guarantee':True},
 'v3.10':{'mixed_HOM_overlap':.7*.2+.3*.8,'mixed_HOM_coincidence':(1-(.7*.2+.3*.8))/2,
 'noisy_candidate':.02+.98*.85*p,'noisy_standard':.02+.98*.85*hom(q*s),
 'branchwise_nonlinear_A':.5,'branchwise_nonlinear_B':.4},
 'v3.11':{'conditional_no_go_only':True,'global_no_go':False,'new_identity_prediction':False,'real_experiment':False},
 'checks':{'slot_swap_commutator':float(np.linalg.norm(slot@S-S@slot)),
           'collective_swap_commutator':float(np.linalg.norm(collective@S-S@collective))}}
if __name__=='__main__':print(json.dumps(calc(),indent=2,ensure_ascii=False))
