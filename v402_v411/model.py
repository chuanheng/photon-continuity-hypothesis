"""v4.02-v4.11: independently verified operational equivalence of finite HMMs.
This is NOT a general quantum-field-theory theorem or photon experiment.
"""
import numpy as np,itertools,json
P_L=np.array([.6,.4]);P_E=np.array([.7,.3])
T0=np.array([[.9,.1],[.2,.8]]);T1=np.array([[.6,.4],[.5,.5]])
PI=np.kron(P_L,P_E);T=np.zeros((4,4))
for l in (0,1):T[2*l:2*l+2,2*l:2*l+2]=[T0,T1][l]
B=np.tile(np.array([[.9,.1],[.1,.9]]),(2,1))
def matrix_word(w,reset=None):
 a=PI*B[:,w[0]]
 for i,y in enumerate(w[1:]):
  if reset is not None and i==reset[0]:
   q=reset[1];J=np.zeros((4,4))
   for l in (0,1):J[2*l:2*l+2,2*l:2*l+2]=np.tile([1-q,q],(2,1))
   a=a@J
  else:a=a@T
  a=a*B[:,y]
 return float(sum(a))
def device_word(w,reset=None):
 total=0.
 for c in (0,1):
  Q=[T0,T1][c]
  for epath in itertools.product((0,1),repeat=len(w)):
   a=P_L[c]*P_E[epath[0]]
   for i,e in enumerate(epath):
    a*=([.9,.1][w[i]] if e==0 else [.1,.9][w[i]])
    if i:
     a*=([1-reset[1],reset[1]][e] if reset is not None and i-1==reset[0] else Q[epath[i-1],e])
   total+=a
 return float(total)
def dist(n,reset=None):return np.array([matrix_word(w,reset) for w in itertools.product((0,1),repeat=n)])
def run():
 d2=dist(2);d3=dist(3);q0=matrix_word([0,0,1])/(matrix_word([0,0,0])+matrix_word([0,0,1]))
 q1=matrix_word([1,0,1])/(matrix_word([1,0,0])+matrix_word([1,0,1]))
 d1=dist(1);o=np.array([d1[w[0]]*(d2[w[0]*2+w[1]]/d1[w[0]])*(d2[w[1]*2+w[2]]/d1[w[1]]) for w in itertools.product((0,1),repeat=3)])
 err={str(n):max(abs(matrix_word(w)-device_word(w)) for w in itertools.product((0,1),repeat=n)) for n in range(1,7)}
 return {'two_time':d2.tolist(),'three_time':d3.tolist(),'conditional_history_difference':float(abs(q0-q1)),
  'strong_lumpability_failure':float(max(abs(T0-T1).ravel())),
  'observed_first_order_Markov_TV':float(sum(abs(d3-o))/2),
  'reset_normalization':float(sum(dist(3,(0,.5)))),
  'independent_device_label_errors':err,
  'reset_equivalence_error':max(abs(matrix_word(w,(0,.5))-device_word(w,(0,.5))) for w in itertools.product((0,1),repeat=3)),
  'length5_normalization':float(sum(dist(5))),'identity_unique':False}
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
