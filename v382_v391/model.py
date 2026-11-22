"""v3.82-v3.91: heldout interventions, multi-start optimization.
Synthetic ordinary 4-state HMM, no photon identity evidence.
"""
import numpy as np,json
from scipy.optimize import minimize
TRUE=np.array([.3,.4,.85,.12,.05]);LOW=np.array([.0001]*5);HIGH=np.array([.9999]*4+[.4]);N=10000
def value(t,a,b):
 km,kd,u,c,e=t;m=km+(1-km)*a;d=kd+(1-kd)*b
 return (1-(1-2*e)**2*(.36+(1-m)*.64)*(.49+(1-d)*.51))/2
def obs(t,held=False):
 km,kd,u,c,e=t;q=1-(1-u)*(1-c)
 a=[(u/2,c/2),(c/2,u/2),(u/4,c/4),(c/4,u/4)] if held else [(0,0),(u,c),(c,u),(q,q)]
 z=np.array([value(t,*v) for v in a]);return z if held else np.r_[z,e]
def opt(k,fixed=None):
 ix=[i for i in range(5) if fixed is None or i!=fixed[0]]
 def pack(x):
  t=np.zeros(5);t[ix]=x
  if fixed is not None:t[fixed[0]]=fixed[1]
  return t
 def fun(x):
  p=np.clip(obs(pack(x)),1e-12,1-1e-12)
  return -float(np.sum(k*np.log(p)+(N-k)*np.log1p(-p)))
 sols=[]
 for a in [TRUE,[.02,.95,.9,.05,.04],[.9,.05,.35,.85,.08],[.5,.5,.5,.5,.04]]:
  b=np.clip(np.array(a)[ix],LOW[ix],HIGH[ix])
  r=minimize(fun,b,method='L-BFGS-B',bounds=list(zip(LOW[ix],HIGH[ix])),options={'maxiter':400})
  sols.append((float(r.fun),pack(r.x)))
 return min(sols,key=lambda a:a[0]),[z[0] for z in sols]
def run():
 rng=np.random.default_rng(20261122);k=rng.binomial(N,obs(TRUE))
 (loss,t),starts=opt(k);g=np.linspace(.0001,.75,20)
 lr=[max(0,2*(opt(k,(0,float(a)))[0][0]-loss)) for a in g]
 true=obs(TRUE,True);pred=obs(t,True);kh=rng.binomial(N,true)
 z=(kh/N-pred)/np.sqrt(true*(1-true)/N)
 return {'seed':20261122,'counts':k.tolist(),'fitted_params':t.tolist(),'fit_losses':starts,'profile_LR':lr,
         'heldout_true':true.tolist(),'heldout_predictions':pred.tolist(),'heldout_counts':kh.tolist(),
         'heldout_z':z.tolist(),'max_abs_z':float(max(abs(z))),
         'ordinary_standard_min_KL':0.,'identity_unique':False}
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
