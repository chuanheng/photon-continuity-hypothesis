"""v3.32-v3.41. Standard hidden Markov two-time environment.
Synthetic statistics; NOT permanent photon identity evidence.
"""
import json,math,csv
from pathlib import Path
import numpy as np
R,EPS,N,SEED=.2,.1,10000,20261121
def p1(r=R,eps=EPS):return eps+(1-2*eps)*r
def joint(kappa,r=R,eps=EPS):
 p=p1(r,eps);h=(1-kappa)*r*(1-r)*(1-2*eps)**2
 z=p*p+h
 return np.array([1-2*p+z,p-z,p-z,z])
def kl(a,b):return float(np.sum(a*np.log(a/b)))
def info(kappa,n=N):
 z=joint(kappa);h=R*(1-R)*(1-2*EPS)**2
 deriv=np.array([-h,h,h,-h])
 return n*float(np.sum(deriv*deriv/z))
def estimate(counts,r=R,eps=EPS):
 p=p1(r,eps);p11=counts[3]/sum(counts)
 return float(np.clip(1-(p11-p*p)/(r*(1-r)*(1-2*eps)**2),0,1))
def triple(kappa):
 transition=(1-kappa)*np.eye(2)+kappa*np.array([[1-R,R],[1-R,R]])
 emit=np.array([[1-EPS,EPS],[EPS,1-EPS]])
 ans=[]
 for ys in np.ndindex(2,2,2):
  a=0.
  for es in np.ndindex(2,2,2):
   a += [1-R,R][es[0]]*emit[es[0],ys[0]]*transition[es[0],es[1]]*emit[es[1],ys[1]]*transition[es[1],es[2]]*emit[es[2],ys[2]]
  ans.append(a)
 return np.array(ans)
def run():
 s,h,f=joint(0),joint(.5),joint(1)
 cnt=np.random.default_rng(SEED).multinomial(N,h)
 k=estimate(cnt);t=triple(.5)
 return {
 'v3.32':{'r':R,'epsilon':EPS,'single_p1':p1()},
 'v3.33':{'shared':s.tolist(),'fresh':f.tolist(),'same_single_time':True},
 'v3.34':{'shared_disagree':float(s[1]+s[2]),'half_disagree':float(h[1]+h[2]),'fresh_disagree':float(f[1]+f[2])},
 'v3.35':{'standard_HMM_match_error':0.,'profile_KL':0.},
 'v3.36':{'KL_wrong_fresh_baseline':kl(h,f),'KL_wrong_shared_baseline':kl(h,s),'TV_wrong_fresh':float(sum(abs(h-f))/2)},
 'v3.37':{'seed':SEED,'N':N,'counts':cnt.tolist(),'kappa_hat':k,'Fisher_SE':1/math.sqrt(info(.5))},
 'v3.38':{'wrong_epsilon':.12,'kappa_hat_wrong':estimate(cnt,eps=.12),'shift':estimate(cnt,eps=.12)-k},
 'v3.39':{'fresh_reference':f.tolist(),'detector_common_memory_alternative_possible':True},
 'v3.40':{'three_time_probs':t.tolist(),'normalization':float(sum(t)),'standard_HMM_gap':0.},
 'v3.41':{'unique_photon_identity_prediction':False,'real_photonic_measurements':False,'QED_model_built':False}}
if __name__=='__main__':
 r=run();p=Path(__file__).parent
 (p/'results.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 with (p/'summary.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.writer(f);w.writerow(['version','metric','value','provenance'])
  for version,section in r.items():
   for name,value in section.items():w.writerow([version,name,json.dumps(value,ensure_ascii=False),'synthetic'])
 print(json.dumps(r,indent=2,ensure_ascii=False))
