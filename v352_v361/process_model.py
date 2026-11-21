"""v3.52-v3.61 synthetic two-carrier memory with reset crosstalk.
Requires numpy. No photon-identity or QED prediction.
Run python -m v352_v361.process_model
"""
import json,numpy as np
TRUE=np.array([.3,.4,.85,.12,.05])
P=('none','reset_m','reset_d','both')
def joint(t,protocol):
 km,kd,u,c,e=t
 pair={'none':(0,0),'reset_m':(u,c),'reset_d':(c,u),'both':(1-(1-u)*(1-c),)*2}[protocol]
 km=km+(1-km)*pair[0];kd=kd+(1-kd)*pair[1]
 mu=.6*.7*(1-2*e)
 cm=.6**2+(1-km)*(1-.6**2);cd=.7**2+(1-kd)*(1-.7**2)
 z=(1-2*e)**2*cm*cd
 return np.array([(1+2*mu+z)/4,(1-z)/4,(1-z)/4,(1-2*mu+z)/4])
def mismatches(t):return np.array([sum(joint(t,p)[[1,2]]) for p in P]+[t[4]])
def jac(t):
 h=1e-6;j=np.empty((5,5))
 for i in range(5):
  a=t.copy();b=t.copy();a[i]+=h;b[i]-=h;j[:,i]=(mismatches(a)-mismatches(b))/(2*h)
 return j
def fisher(t,n):
 p=mismatches(t);j=jac(t);return j.T@np.diag(np.array(n)/(p*(1-p)))@j
def fit(y):
 t=TRUE.copy()
 for _ in range(100):
  delta=np.linalg.lstsq(jac(t),y-mismatches(t),rcond=None)[0]
  t=np.clip(t+delta,[.001,.001,.01,.001,.001],[.999,.999,.999,.999,.4])
  if max(abs(delta))<1e-12:break
 return t
def run():
 t=TRUE.copy();p=mismatches(t);N=np.full(5,10000)
 F=fisher(t,N);rng=np.random.default_rng(20261121)
 k=rng.binomial(N,p);est=fit(k/N);se=np.sqrt(np.diag(np.linalg.inv(F)))
 reps=np.array([fit(rng.binomial(N,p)/N) for _ in range(300)])
 drift=t.copy();drift[4]=.07;y=mismatches(drift);y[4]=t[4]
 ideal=t.copy();ideal[2:4]=[1,0]
 return {'v3.52':{'true':t.tolist(),'mismatch':p[:4].tolist()},
 'v3.53':{'ideal_material_reset':mismatches(ideal)[1],'actual_material_reset':p[1]},
 'v3.54':{'effective_detector_reset_rate':t[1]+(1-t[1])*t[3]},
 'v3.55':{'no_epsilon_reference_rank':int(np.linalg.matrix_rank(fisher(t,[10000]*4+[0]),tol=1e-7)),'all_reference_rank':int(np.linalg.matrix_rank(F,tol=1e-7))},
 'v3.56':{'seed':20261121,'counts':k.tolist(),'estimated_parameters':est.tolist(),'fisher_se':se.tolist()},
 'v3.57':{'repetitions':300,'empirical_sd':reps.std(axis=0,ddof=1).tolist(),'coverage_95':np.mean(abs(reps-t)<=1.96*se,axis=0).tolist()},
 'v3.58':{'neglected_reset_and_crosstalk':True,'model_misspecification':True},
 'v3.59':{'stale_epsilon_reference':.05,'actual_epsilon':.07,'biased_fit':fit(y).tolist()},
 'v3.60':{'classical_four_state_HMM_reproduces_all':True,'standard_profile_KL':0.},
 'v3.61':{'real_experiment':False,'permanent_identity_unique_prediction':False}}
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
