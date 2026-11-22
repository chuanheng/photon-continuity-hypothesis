"""v3.72-v3.81: exact binomial likelihood; synthetic ordinary 4-state HMM.
No permanent photon identity claim. Needs numpy scipy.
"""
import numpy as np, json
from scipy.optimize import minimize
from scipy.stats import chi2
from scipy.special import xlogy
TRUE=np.array([.30,.40,.85,.12,.05]);N=np.full(5,10000)
LOW=np.array([.0001]*5);HIGH=np.array([.9999]*4+[.4])
def probs(t):
 km,kd,u,c,e=t;b=1-(1-u)*(1-c)
 out=[]
 for x,y in [(0,0),(u,c),(c,u),(b,b)]:
  m=km+(1-km)*x;d=kd+(1-kd)*y
  out.append((1-(1-2*e)**2*(.36+(1-m)*.64)*(.49+(1-d)*.51))/2)
 return np.array(out+[e])
def nll(t,k):
 p=np.clip(probs(t),1e-10,1-1e-10)
 return -float(np.sum(xlogy(k,p)+xlogy(N-k,1-p)))
def fit(k,fixed=None):
 idx=[i for i in range(5) if fixed is None or i!=fixed[0]]
 def pack(v):
  t=np.zeros(5);t[idx]=v
  if fixed is not None:t[fixed[0]]=fixed[1]
  return t
 results=[]
 for s in [TRUE,np.array([.1,.7,.75,.3,.06]),np.array([.65,.2,.95,.04,.05])]:
  z=minimize(lambda x:nll(pack(x),k),s[idx],method='L-BFGS-B',bounds=list(zip(LOW[idx],HIGH[idx])),options={'maxiter':300})
  results.append((z.fun,pack(z.x)))
 return min(results,key=lambda z:z[0])
def run():
 rng=np.random.default_rng(20261122);k=rng.binomial(N,probs(TRUE))
 ll,hat=fit(k)
 grid=np.linspace(.0001,.65,18)
 lr=[max(0,2*(fit(k,(0,float(v)))[0]-ll)) for v in grid]
 samples=[]
 for _ in range(30):
  a=rng.binomial(N,probs(TRUE));af,at=fit(a);n0,_=fit(a,(0,.3))
  samples.append(max(0,2*(n0-af)))
 return {'seed':20261122,'n':N.tolist(),'counts':k.tolist(),'mle':hat.tolist(),'nll':float(ll),
         'profile_grid':grid.tolist(),'profile_LR':lr,
         'LR_simulations':30,'LR_fraction_above_3_841':float(np.mean(np.array(samples)>chi2.ppf(.95,1))),
         'standard_model_profile_KL':0.,'identity_unique_prediction':False}
if __name__=='__main__':print(json.dumps(run(),indent=2,ensure_ascii=False))
