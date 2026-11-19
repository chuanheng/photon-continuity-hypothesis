"""v2.72-v2.81. Photon->matter->probe->photon synthetic model.
Standard finite-dimensional quantum information; not proof of permanent identity.
Run: python -m models.identity_full_sequence_v272_v281
"""
import json,math,numpy as np
I2=np.eye(2,dtype=complex);I4=np.eye(4,dtype=complex)
X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex)
ZERO=np.array([1,0],complex);PLUS=np.array([1,1],complex)/math.sqrt(2)
PSI=np.array([1,1,0,0],complex)/math.sqrt(2)
A=np.diag([0,0,1,-1]).astype(complex)
ZMODE=np.diag([1,-1,1,-1]).astype(complex)
def rho(v):return np.outer(v,v.conj())
def evolve(h,t):
 w,v=np.linalg.eigh(h);return (v*np.exp(-1j*t*w))@v.conj().T
def write(g0=1.,g1=1.,delta=0.):
 h=np.diag([0,0,delta,delta]).astype(complex)
 for i,g in enumerate((g0,g1)):h[i,i+2]=h[i+2,i]=g
 return evolve(h,math.pi/2)
def dephase(r,c):return ((1+c)*r+(1-c)*ZMODE@r@ZMODE)/2
def trace_probe(r):return np.einsum('ipjp->ij',r.reshape(4,2,4,2))
def trace_system(r):return np.einsum('ipiq->pq',r.reshape(4,2,4,2))
def joint(c=.85,s=.8,theta=.6,w=None):
 if w is None:w=write()
 state=w@rho(PSI)@w.conj().T
 interaction=evolve(np.kron(A,Y),theta/2)
 combined=interaction@np.kron(dephase(state,c*s),rho(ZERO))@interaction.conj().T
 read=np.kron(w.conj().T,I2)
 return read@combined@read.conj().T
def p(r,obs):return float(np.trace(r@obs).real)
def observed(j):
 ph=trace_probe(j);probe=trace_system(j)
 x=np.zeros((4,4),complex);x[:2,:2]=rho(PLUS)
 px=(I2+X)/2
 return {'photon_X_plus':p(ph,x),'probe_X_plus':p(probe,px),
         'photon_mode0':float(ph[0,0].real),'photon_mode1':float(ph[1,1].real),
         'joint_photonX_probeX':p(j,np.kron(x,px)),
         'photon_total':float((ph[0,0]+ph[1,1]).real)}
def click(v):return .01+.99*.9*v
def kl(p,q):
 if abs(p-q)<1e-14:return 0.
 return p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))
def run():
 w=write();st=w@rho(PSI)@w.conj().T
 back=w.conj().T@st@w
 c,s,theta=.85,.8,.6
 actual=observed(joint(c,s,theta))
 baseline=observed(joint(c,1,theta))
 standard=observed(joint(c*s,1,theta))
 pg=click(actual['photon_X_plus']);pref=click(baseline['photon_X_plus'])
 scan=[]
 for t in (.5,1.,2.):
  cc=math.exp(-.3*t)
  scan.append({'t':t,'candidate':observed(joint(cc,s,theta))['photon_X_plus'],
               'standard_visibility':(1+s*cc*math.cos(theta))/2})
 grad=np.array([s,c])*(.99*.9*math.cos(theta)/2)
 f=1000*np.outer(grad,grad)/(pg*(1-pg))
 k=int(np.random.default_rng(20261119).binomial(10000,pg))
 detuned=observed(joint(c,s,theta,write(delta=.8)))
 selective=observed(joint(c,s,theta,write(g1=.7)))
 return {
 'v2.72':{'write_unitarity_error':float(np.max(abs(w.conj().T@w-I4))),'matter_probability':float((st[2,2]+st[3,3]).real)},
 'v2.73':{'reverse_trace_distance':float(sum(abs(np.linalg.eigvalsh(back-rho(PSI))))/2)},
 'v2.74':{'effective_dephasing':c*s,'normalization':float(np.trace(trace_probe(joint(c,s,theta))).real)},
 'v2.75':{'outputs':actual,'analytic_X_plus':(1+c*s*math.cos(theta))/2},
 'v2.76':{'probe_dephasing_drop':observed(joint(c,s,0))['photon_X_plus']-actual['photon_X_plus'],'joint_minus_product':actual['joint_photonX_probeX']-actual['photon_X_plus']*actual['probe_X_plus']},
 'v2.77':{'all_observed_fields_max_gap':max(abs(actual[z]-standard[z]) for z in actual),'standard_c_eff':c*s},
 'v2.78':{'fisher_rank':int(np.linalg.matrix_rank(f,tol=1e-8)),'fisher_eigenvalues':np.linalg.eigvalsh(f).tolist()},
 'v2.79':{'scan':scan,'max_scan_gap':max(abs(r['candidate']-r['standard_visibility']) for r in scan),'detuned':detuned,'selective':selective},
 'v2.80':{'n':10000,'seed':20261119,'synthetic_click_count':k,'candidate_click_probability':pg,'fixed_baseline_probability':pref,'KL_fixed_baseline':kl(pg,pref),'profiled_KL':0.},
 'v2.81':{'identity_specific_prediction':False,'standard_model_equivalence':True,'QED_verified':False}}
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
