"""v2.82-v2.91. Five-observation independent calibration toy.
All results synthetic, not QED or permanent photon identity evidence.
Requires numpy. Run: python -m models.identity_calibration_v282_v291
"""
import json,math,numpy as np
V,C,S,ETA,D,THETA=.95,.85,.8,.9,.01,.6
COUNTS=np.array([10000,5000,5000,5000,5000])
TRUE=np.array([V,C,S,ETA,D])
SEED=20261119
def optical(v,c,s,theta=THETA):return (1+v*c*s*math.cos(theta))/2
def probabilities(t):
 v,c,s,e,d=t
 return np.array([d+(1-d)*e*optical(v,c,s),(1+c)/2,(1+v)/2,d,d+(1-d)*e])
def jacobian(t):
 v,c,s,e,d=t
 a=math.cos(THETA)/2;p=optical(v,c,s)
 j=np.zeros((5,5))
 j[0]=[(1-d)*e*a*c*s,(1-d)*e*a*v*s,(1-d)*e*a*v*c,(1-d)*p,1-e*p]
 j[1,1]=.5;j[2,0]=.5;j[3,4]=1
 j[4,3]=1-d;j[4,4]=1-e
 return j
def fisher(t=TRUE):
 p=probabilities(t);j=jacobian(t)
 return j.T@np.diag(COUNTS/(p*(1-p)))@j
def estimate(k):
 m,c,v,d,b=k/COUNTS
 e=(b-d)/(1-d);p=(m-d)/((1-d)*e)
 cc=2*c-1;vv=2*v-1
 return np.array([vv,cc,(2*p-1)/(vv*cc*math.cos(THETA)),e,d])
def kl(p,q):
 if abs(p-q)<1e-15:return 0.
 return p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))
def simulate(rng,t=TRUE):return rng.binomial(COUNTS,probabilities(t))
def run(reps=2000):
 p=probabilities(TRUE);j=jacobian(TRUE);f=fisher()
 main_f=COUNTS[0]*np.outer(j[0],j[0])/(p[0]*(1-p[0]))
 rng=np.random.default_rng(SEED)
 k=simulate(rng);point=estimate(k)
 draws=np.array([estimate(simulate(rng)) for _ in range(reps)])
 se=math.sqrt(np.linalg.inv(f)[2,2])
 drift=TRUE.copy();drift[1]=C-.02
 biased=[]
 for _ in range(reps):
  sample=simulate(rng);sample[0]=rng.binomial(COUNTS[0],probabilities(drift)[0])
  biased.append(estimate(sample)[2])
 scan=[{'theta':t,'candidate':optical(V,C,S,t),
        'standard_environment':optical(V*S,C,1.,t)}
       for t in (0.,.3,.6,.9)]
 no_extra=TRUE.copy();no_extra[2]=1.
 return {
 'v2.82':{'main_only_fisher_rank':int(np.linalg.matrix_rank(main_f,tol=1e-8)),'main_click_p':float(p[0]),'visibility_product':V*C*S},
 'v2.83':{'c_reference_p':float(p[1]),'v_reference_p':float(p[2]),'rank_main_plus_two_refs':int(np.linalg.matrix_rank(j[:3],tol=1e-8))},
 'v2.84':{'dark_reference_p':float(p[3]),'bright_reference_p':float(p[4]),'full_fisher_rank':int(np.linalg.matrix_rank(f,tol=1e-8)),'eigenvalues':np.linalg.eigvalsh(f).tolist()},
 'v2.85':{'seed':SEED,'counts':k.tolist(),'estimate':point.tolist(),'truth':TRUE.tolist()},
 'v2.86':{'replicates':reps,'fisher_se_s':se,'mc_se_s':float(draws[:,2].std(ddof=1)),'coverage_95':float(np.mean(abs(draws[:,2]-S)<1.96*se))},
 'v2.87':{'storage_drift':-.02,'estimated_s_mean':float(np.mean(biased)),'estimated_s_bias':float(np.mean(biased)-S)},
 'v2.88':{'theta_scan':scan,'max_gap':max(abs(a['candidate']-a['standard_environment']) for a in scan)},
 'v2.89':{'KL_wrong_fixed_s_one':kl(float(p[0]),float(probabilities(no_extra)[0])),'KL_standard_environment_refit':0.},
 'v2.90':{'five_statistical_parameters_identifiable':True,'permanent_photon_identity_proven':False},
 'v2.91':{'unique_identity_prediction':False,'full_QED_compared':False,'real_experiment':False}}
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
