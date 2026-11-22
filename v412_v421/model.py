"""v4.12-v4.21: observable Hankel rank, finite-sample noise and ordinary HMM.
No photon experiment or individual-identity dynamics.
"""
import numpy as np,itertools,json
from scipy.linalg import svdvals
PI=np.kron([.6,.4],[.7,.3]);T0=np.array([[.9,.1],[.2,.8]]);T1=np.array([[.6,.4],[.5,.5]])
T=np.zeros((4,4))
for l in (0,1):T[2*l:2*l+2,2*l:2*l+2]=[T0,T1][l]
B=np.tile(np.array([[.9,.1],[.1,.9]]),(2,1))
def pword(w):
 a=PI.copy()
 for i,y in enumerate(w):
  if i:a=a@T
  a=a*B[:,y]
 return float(sum(a))
def words(d):return [()]+[w for n in range(1,d+1) for w in itertools.product((0,1),repeat=n)]
def H(d,p):
 W=words(d);return np.array([[p(u+v) for v in W] for u in W])
def draw(N,rng):
 l=(rng.random(N)<.4).astype(int);e=(rng.random(N)<.3).astype(int);y=np.empty((N,6),int)
 for t in range(6):
  if t:
   pe=np.where(l==0,np.where(e==0,.1,.8),np.where(e==0,.4,.5))
   e=(rng.random(N)<pe).astype(int)
  y[:,t]=np.bitwise_xor(e,(rng.random(N)<.1).astype(int))
 return y
def empirical(y):
 n=len(y);counts=[np.array([n])]
 for i in range(1,7):
  codes=np.zeros(n,dtype=int)
  for j in range(i):codes=2*codes+y[:,j]
  counts.append(np.bincount(codes,minlength=2**i))
 def calc(w):
  idx=0
  for a in w:idx=2*idx+a
  return counts[len(w)][idx]/n
 return calc
def run():
 a={d:svdvals(H(d,pword)) for d in (1,2,3,4)}
 em=svdvals(H(3,empirical(draw(50000,np.random.default_rng(20261122)))))
 # Local evidence independently seeds each null sequence from a master generator.
 rng=np.random.default_rng(20261122)
 null=[]
 for i in range(60):
  seed=int(rng.integers(0,2**31))
  null.append(svdvals(H(3,empirical(draw(50000,np.random.default_rng(seed)))))[4])
 return {'one_time':[pword((0,)),pword((1,))],
 'theoretical_ranks':{str(d):int(sum(a[d]>1e-11)) for d in a},
 'hankel_shapes':{str(d):list(H(d,pword).shape) for d in a},
 'theoretical_singular_first5':a[3][:5].tolist(),
 'best_rank2_residual':float(np.linalg.norm(a[3][2:])),
 'sample_N':50000,'empirical_singular_first8':em[:8].tolist(),
 'naive_rank_at_1e_minus_4':int(sum(em>1e-4)),
 'null_n':60,'null_fifth_quantiles':np.quantile(null,[.5,.9,.95]).tolist(),
 'observed_fifth':float(em[4]),'identity_unique':False}
if __name__=='__main__':print(json.dumps(run(),indent=2,ensure_ascii=False))
