"""v2.22-v2.31: Remote steering/no-signalling audit of nonlinear Bloch model.
Mathematical counterexample, not physical photon identity evidence. Requires numpy/scipy.
"""
import json,math,numpy as np
from scipy.stats import binom
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]).astype(complex)
BELL=np.array([1,0,0,1],complex)/math.sqrt(2)
def rho(v):return (I+v[0]*X+v[1]*Y+v[2]*Z)/2
def coords(a):return np.array([float(np.trace(a@x).real) for x in (X,Y,Z)])
def evolve(a,lam=.4):
 x,y,z=coords(a);c=1-2*lam*x*x;return rho((c*x,c*y,z))
def A():return [(.5,(1.,0.,0.)),(.5,(-1.,0.,0.))]
def B():return [(1/3,(1.,0.,0.)),(1/3,(-.5,0.,math.sqrt(3)/2)),(1/3,(-.5,0.,-math.sqrt(3)/2))]
def steering(scheme):
 # For Bell |Phi+>, Alice effects E_i=2 w_i rho_i^T steer Bob to w_i rho_i
 effects=[2*w*rho(v).T for w,v in scheme]
 joint=np.outer(BELL,BELL.conj()).reshape(2,2,2,2)
 unnorm=[np.einsum('ca,abcd->bd',e,joint) for e in effects]
 return effects,[float(np.trace(r).real) for r in unnorm],unnorm
def average(scheme,lam=.4):return sum(w*evolve(rho(v),lam) for w,v in scheme)
def distance(a,b):return float(np.sum(abs(np.linalg.eigvalsh(a-b)))/2)
def plus(a):return float(np.trace((I+X)/2@a).real)
def kl(p,q):return p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))
def run():
 ea,wa,ra=steering(A());eb,wb,rb=steering(B())
 a,b=average(A()),average(B())
 pA,pB=plus(a),plus(b);n=1000
 k=next(j for j in range(n+1) if binom.cdf(j,n,.5)>.05)-1
 rng=np.random.default_rng(20261117)
 scan=[{'lambda':l,'pA':plus(average(A(),l)),'pB':plus(average(B(),l))} for l in (0,.05,.1,.2,.3,.4,.5)]
 return {
 'v2.22':{'Bell_norm':float(np.linalg.norm(BELL))},
 'v2.23':{'A_POVM_error':float(np.max(abs(sum(ea)-I))),'weights':wa,'conditional_errors':[distance(r,w*rho(v)) for r,(w,v) in zip(ra,A())]},
 'v2.24':{'B_POVM_error':float(np.max(abs(sum(eb)-I))),'weights':wb,'min_effect_eigenvalue':min(float(min(np.linalg.eigvalsh(e))) for e in eb),'conditional_errors':[distance(r,w*rho(v)) for r,(w,v) in zip(rb,B())]},
 'v2.25':{'unconditioned_trace_distance':distance(sum(ra),sum(rb)),'Bob_vs_I2':distance(sum(rb),I/2)},
 'v2.26':{'pA':pA,'pB':pB,'difference':pA-pB,'output_trace_distance':distance(a,b)},
 'v2.27':{'branchwise_remote_signalling':True,'KL':kl(pB,pA),'conditional_on':'Alice can steer ensemble; Bob evolves each branch by the nonlinear rule'},
 'v2.28':{'n':n,'critical_at_most':k,'type_I':float(binom.cdf(k,n,.5)),'power':float(binom.cdf(k,n,.4)),'seeded_counts':[int(rng.binomial(n,pA)),int(rng.binomial(n,pB))]},
 'v2.29':{'lambda_scan':scan,'analytic_pB':'0.5 - lambda/4'},
 'v2.30':{'density_only_pplus':plus(evolve(I/2)),'branchwise_B_pplus':pB,'shared_affine_minimax_distance':distance(a,b)/2},
 'v2.31':{'survives_standard_remote_steering_no_signalling_assumptions':False,'identity_specific_prediction':False,'covariant_QED_model':False}}
if __name__=='__main__':print(json.dumps(run(),indent=2,ensure_ascii=False))
