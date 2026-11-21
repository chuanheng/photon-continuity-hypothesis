"""v3.42-v3.51: two ordinary memory carriers and selective resets.
Synthetic probability model; no permanent photon-identity evidence.
Requires NumPy; python -m v342_v351.process_model.
"""
import json,math,numpy as np
RM,RD,KM,KD,EPS=.2,.15,.3,.4,.05
PROTOCOLS=('baseline','reset_m','reset_d','reset_both')
def kappa(protocol,km=KM,kd=KD,success=1.):
 m=km+(1-km)*success if protocol in ('reset_m','reset_both') else km
 d=kd+(1-kd)*success if protocol in ('reset_d','reset_both') else kd
 return m,d
def corr(r,k):return (1-2*r)**2+(1-k)*(1-(1-2*r)**2)
def joint(protocol='baseline',km=KM,kd=KD,eps=EPS,success=1.):
 m,d=kappa(protocol,km,kd,success)
 mu=(1-2*RM)*(1-2*RD)*(1-2*eps)
 ez=(1-2*eps)**2*corr(RM,m)*corr(RD,d)
 return np.array([(1+2*mu+ez)/4,(1-ez)/4,(1-ez)/4,(1-2*mu+ez)/4])
def disagree(protocol='baseline',**kw):
 z=joint(protocol,**kw);return float(z[1]+z[2])
def fisher(protos,step=1e-5,n=10000):
 p=np.array([disagree(x) for x in protos])
 J=np.zeros((len(protos),2))
 for a,pr in enumerate(protos):
  for b,(name,val) in enumerate((('km',KM),('kd',KD))):
   J[a,b]=(disagree(pr,**{name:val+step})-disagree(pr,**{name:val-step}))/(2*step)
 return (J.T*(n/(p*(1-p))))@J
def triple():
 pi=np.array([(1-RM)*(1-RD),(1-RM)*RD,RM*(1-RD),RM*RD])
 tm=(1-KM)*np.eye(2)+KM*np.tile([1-RM,RM],(2,1))
 td=(1-KD)*np.eye(2)+KD*np.tile([1-RD,RD],(2,1))
 T=np.kron(tm,td)
 B=np.zeros((4,2))
 for i,(m,d) in enumerate(((0,0),(0,1),(1,0),(1,1))):
  B[i,m^d]=1-EPS;B[i,1-(m^d)]=EPS
 return np.array([pi@np.diag(B[:,ys[0]])@T@np.diag(B[:,ys[1]])@T@B[:,ys[2]] for ys in np.ndindex(2,2,2)])
def kl(p,q):return float(sum(p*np.log(p/q)))
def run():
 ps={x:joint(x) for x in PROTOCOLS}
 ds={x:disagree(x) for x in PROTOCOLS}
 rng=np.random.default_rng(20261121)
 sample={x:rng.multinomial(10000,ps[x]).tolist() for x in PROTOCOLS}
 rates={x:(v[1]+v[2])/10000 for x,v in sample.items()}
 def estimate_m(y):
  ezz=1-2*y
  Em=ezz/((1-2*EPS)**2*(1-2*RD)**2)
  return 1-(Em-(1-2*RM)**2)/(1-(1-2*RM)**2)
 def estimate_d(y):
  ezz=1-2*y
  Ed=ezz/((1-2*EPS)**2*(1-2*RM)**2)
  return 1-(Ed-(1-2*RD)**2)/(1-(1-2*RD)**2)
 F=fisher(('baseline','reset_m','reset_d'))
 t=triple()
 return {
 'v3.42':{'p_one':.5*(1-(1-2*EPS)*(1-2*RM)*(1-2*RD)),'baseline':ps['baseline'].tolist()},
 'v3.43':{'mismatch':ds,'reset_m_effect':ds['reset_m']-ds['baseline'],'reset_d_effect':ds['reset_d']-ds['baseline']},
 'v3.44':{'both_reset_independent_gap':float(max(abs(ps['reset_both']-joint(km=1,kd=1))))},
 'v3.45':{'one_setting_rank':int(np.linalg.matrix_rank(fisher(('baseline',)))),'three_settings_rank':int(np.linalg.matrix_rank(F)),'eigenvalues':np.linalg.eigvalsh(F).tolist()},
 'v3.46':{'seed':20261121,'n_each':10000,'counts':sample,'km_hat':estimate_m(rates['reset_d']),'kd_hat':estimate_d(rates['reset_m'])},
 'v3.47':{'success':.8,'imperfect_reset_m':disagree('reset_m',success=.8),'ideal_reset_m':ds['reset_m']},
 'v3.48':{'unlabelled_environment_can_be_4_state_HMM':True,'photon_individuality_identified':False},
 'v3.49':{'profiled_KL':0.,'KL_wrong_no_memory':kl(ps['baseline'],ps['reset_both'])},
 'v3.50':{'triple':t.tolist(),'norm':float(sum(t)),'two_time_marginal_gap':float(max(abs(t.reshape(2,2,2).sum(axis=2).reshape(4)-ps['baseline'])))},
 'v3.51':{'unique_photon_identity_prediction':False,'real_optical_experiment':False}}
if __name__=='__main__':print(json.dumps(run(),indent=2,ensure_ascii=False))
