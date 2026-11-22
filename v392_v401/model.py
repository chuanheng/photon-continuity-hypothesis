"""v3.92-v4.01: holdout multiple testing with parameter uncertainty.
Ordinary HMM only. Synthetic, no unique photon identity claim.
"""
import numpy as np,json
from scipy.optimize import minimize
from scipy.stats import norm
TRUE=np.array([.3,.4,.85,.12,.05]);LOW=np.array([.0001]*5);HIGH=np.array([.9999]*4+[.4]);N=10000
def p(t,a,b):
 km,kd,u,c,e=t;m=km+(1-km)*a;d=kd+(1-kd)*b
 return (1-(1-2*e)**2*(.36+(1-m)*.64)*(.49+(1-d)*.51))/2
def probs(t,held=False):
 km,kd,u,c,e=t;q=1-(1-u)*(1-c)
 settings=[(u/2,c/2),(c/2,u/2),(u/4,c/4),(c/4,u/4)] if held else [(0,0),(u,c),(c,u),(q,q)]
 z=np.array([p(t,*x) for x in settings])
 return z if held else np.r_[z,e]
def fit(k):
 def obj(t):
  p=np.clip(probs(t),1e-12,1-1e-12)
  return -sum(k*np.log(p)+(N-k)*np.log1p(-p))
 ss=[]
 for start in [TRUE,[.15,.7,.8,.2,.05]]:
  r=minimize(obj,start,method='L-BFGS-B',bounds=list(zip(LOW,HIGH)),options={'maxiter':250})
  ss.append((float(r.fun),r.x))
 return min(ss,key=lambda x:x[0])[1]
def jac(fn,t):
 h=1e-5;out=np.empty((len(fn(t)),5))
 for i in range(5):
  a=t.copy();b=t.copy();a[i]+=h;b[i]-=h
  out[:,i]=(fn(a)-fn(b))/(2*h)
 return out
def run():
 rng=np.random.default_rng(20261122);train=probs(TRUE);hold=probs(TRUE,True)
 ktrain=rng.binomial(N,train);kh=rng.binomial(N,hold);t=fit(ktrain)
 pp=probs(t,True);se=np.sqrt(hold*(1-hold)/N);z=(kh/N-pp)/se
 pv=2*norm.sf(abs(z));adj=np.minimum(1,pv*4)
 F=jac(probs,TRUE).T@np.diag(N/(train*(1-train)))@jac(probs,TRUE)
 J=jac(lambda x:probs(x,True),TRUE);vv=np.sum(J@np.linalg.inv(F)*J,axis=1)
 z2=(kh/N-pp)/np.sqrt(se**2+vv)
 maxzs=[]
 for _ in range(100):
  a=rng.binomial(N,train);b=rng.binomial(N,hold)
  tt=fit(a);maxzs.append(float(max(abs((b/N-probs(tt,True))/se))))
 return {'seed':20261122,'training_counts':ktrain.tolist(),'holdout_counts':kh.tolist(),
         'naive_z':z.tolist(),'naive_p':pv.tolist(),'bonferroni_p':adj.tolist(),
         'fisher_adjusted_z':z2.tolist(),'bootstrap_n':100,'bootstrap_max_z_quantiles':np.quantile(maxzs,[.9,.95]).tolist(),
         'bootstrap_exceedance':float(np.mean(np.array(maxzs)>=max(abs(z)))),
         'standard_profile_KL':0.,'identity_unique':False}
if __name__=='__main__':print(json.dumps(run(),indent=2,ensure_ascii=False))
