"""v3.62–v3.71 finite-sample inference: ordinary four-state HMM.
Synthetic statistics, NOT new photon-identity dynamics.
Requires numpy, scipy. Run: python -m v362_v371.process_model
"""
import json
import numpy as np
from scipy.optimize import least_squares
from scipy.stats import chi2

TRUE=np.array([.30,.40,.85,.12,.05])
LOW=np.array([.001,.001,.01,.001,.001])
HIGH=np.array([.999,.999,.999,.999,.4])
def probs(t):
 km,kd,u,c,e=t
 operations=[(0,0),(u,c),(c,u),(1-(1-u)*(1-c),)*2]
 out=[]
 for x,y in operations:
  km1=km+(1-km)*x;kd1=kd+(1-kd)*y
  cm=.6**2+(1-km1)*(1-.6**2)
  cd=.7**2+(1-kd1)*(1-.7**2)
  out.append((1-(1-2*e)**2*cm*cd)/2)
 return np.array(out+[e])
def jac(t):
 J=np.zeros((5,5));h=1e-5
 for i in range(5):
  a=t.copy();b=t.copy();a[i]+=h;b[i]-=h
  J[:,i]=(probs(a)-probs(b))/(2*h)
 return J
def fisher(t,n):
 p=probs(t);J=jac(t);return (J.T*(n/(p*(1-p))))@J
def fit(k,n,start=TRUE,fixed=None):
 active=list(range(5)) if fixed is None else [j for j in range(5) if j!=fixed[0]]
 def complete(x):
  if fixed is None:return x
  t=np.zeros(5);t[active]=x;t[fixed[0]]=fixed[1];return t
 def residual(x):
  p=probs(complete(x))
  return np.sqrt(n)*(p-k/n)/np.sqrt(np.maximum(p*(1-p),1e-8))
 sol=least_squares(residual,start[active],bounds=(LOW[active],HIGH[active]),max_nfev=250)
 return complete(sol.x)
def dev(t,k,n):
 p=np.clip(probs(t),1e-12,1-1e-12)
 return -2*np.sum(k*np.log(p)+(n-k)*np.log1p(-p))
def run(reps=180):
 n=np.full(5,10000)
 p=probs(TRUE);rng=np.random.default_rng(20261121)
 k=rng.binomial(n,p);hat=fit(k,n)
 F=fisher(TRUE,n);se=np.sqrt(np.diag(np.linalg.inv(F)))
 estimates=np.array([fit(rng.binomial(n,p),n) for _ in range(reps)])
 bootstrap=np.array([fit(rng.binomial(n,probs(hat)),n,start=hat) for _ in range(reps)])
 quantiles=np.quantile(bootstrap,[.025,.975],axis=0).T.tolist()
 grid=np.linspace(.08,.72,33);min_dev=dev(hat,k,n)
 profile=[max(0.,dev(fit(k,n,start=hat,fixed=(0,float(x))),k,n)-min_dev) for x in grid]
 selected=grid[np.array(profile)<=chi2.ppf(.95,1)]
 drift=TRUE.copy();drift[4]=.07
 y=probs(drift);y[4]=.05
 drift_hat=fit(y*n,n)
 return {'v3.62':{'probabilities':p.tolist(),'main_rank':int(np.linalg.matrix_rank(jac(TRUE)[:4]))},
 'v3.63':{'full_rank':int(np.linalg.matrix_rank(jac(TRUE))),'Fisher_condition_number':float(np.linalg.cond(F)),'Fisher_SE':se.tolist()},
 'v3.64':{'seed':20261121,'counts':k.tolist(),'estimate':hat.tolist()},
 'v3.65':{'reps':reps,'normal_coverage':np.mean(abs(estimates-TRUE)<=1.96*se,axis=0).tolist(),'empirical_sd':estimates.std(axis=0,ddof=1).tolist()},
 'v3.66':{'bootstrap_percentile_intervals':quantiles},
 'v3.67':{'approximate_WLS_profile_grid_CI':[float(selected.min()),float(selected.max())],'grid_left_censoring':True},
 'v3.68':{'wrong_shared_epsilon_reference_fit':drift_hat.tolist()},
 'v3.69':{'two_memory_parameter_sensitivity_rank':int(np.linalg.matrix_rank(jac(TRUE)[:4,:2]))},
 'v3.70':{'standard_HMM_exactly_reproduces_candidate':True,'profile_KL':0.},
 'v3.71':{'identity_specific_prediction':False,'experiment':False}}
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
