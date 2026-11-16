"""v1.62-v1.71: reversible light/matter memory, dephasing, identifiability.
Synthetic finite-dimensional quantum information model; not QED or permanent identity evidence.
Requires NumPy. Run: python3 models/identity_memory_v162_v171.py
"""
import math,json,random
import numpy as np
SEED=20261116
def storage_unitary(theta):
    c,s=math.cos(theta),math.sin(theta)
    u=np.eye(4,dtype=complex)
    for p,m in ((0,2),(1,3)):
        u[p,p]=c;u[p,m]=-s;u[m,p]=s;u[m,m]=c
    return u
def input_state():return np.array([1,1,0,0],complex)/math.sqrt(2)
def density(v):return np.outer(v,v.conj())
def dephase(r,s):
    if abs(s)>1:raise ValueError('invalid pointer overlap')
    z=np.diag([1,-1]).astype(complex)
    return (1+s)/2*r+(1-s)/2*z@r@z
def fringe(s,mu):
    if abs(s)>1 or abs(mu)>1:raise ValueError('invalid overlap')
    return (1+s*mu)/2
def fisher(s,mu,n=1):
    p=fringe(s,mu);v=np.array([mu/2,s/2])
    return n*np.outer(v,v)/(p*(1-p))
def hom_fisher(mu,n):
    p=(1-mu*mu)/2
    out=np.zeros((2,2));out[1,1]=n*mu*mu/(p*(1-p))
    return out
def kl(p,q):
    return p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))
def count(n,p,seed):return sum(random.Random(seed).random()<p for _ in range(n)) # avoid for sampling; see below
def sample(n,p,seed):
    rng=random.Random(seed);return sum(rng.random()<p for _ in range(n))
def run():
    u=storage_unitary(math.pi/2)
    initial=input_state();stored=u@initial
    recovered=u.conj().T@stored
    memory=density(stored[2:]);s,mu=.6,.75
    tagged=dephase(memory,s)
    ordinary_environment=dephase(memory,s)
    f=fisher(s,mu);joint=f+hom_fisher(mu,1000)
    return {
      'v1.62':{'unitarity_max_error':float(np.max(np.abs(u.conj().T@u-np.eye(4))))},
      'v1.63':{'photonic_probability':float(sum(abs(stored[:2])**2)),
               'matter_probability':float(sum(abs(stored[2:])**2))},
      'v1.64':{'state_distance':float(np.linalg.norm(recovered-initial)),
               'fidelity':float(abs(np.vdot(recovered,initial))**2)},
      'v1.65':{'pointer_overlap':s,'coherence_visibility':float(2*abs(tagged[0,1]))},
      'v1.66':{'trace_distance':float(np.linalg.norm(tagged-ordinary_environment,ord='nuc')/2)},
      'v1.67':{'mode_efficiencies':[.92,.72], 'conditional_mode0_fraction':.92/(.92+.72)},
      'v1.68':{'fringe_probability':fringe(s,mu),
                'local_fisher_eigenvalues':list(map(float,np.linalg.eigvalsh(f)))},
      'v1.69':{'reference_hom_trials':1000,
                'joint_fisher_eigenvalues':list(map(float,np.linalg.eigvalsh(joint))),
                'joint_determinant':float(np.linalg.det(joint))},
      'v1.70':{'events':10000,'positive_count':sample(10000,fringe(s,mu),SEED),
                'candidate_probability':fringe(s,mu),
                'incorrect_fixed_baseline':fringe(1,mu),
                'KL_to_fixed_baseline':kl(fringe(s,mu),fringe(1,mu)),
                'profiled_KL':0.0},
      'v1.71':{'unique_identity_observable':False,
               'standard_dephasing_equivalence':True,
               'QED_consistency_verified':False}
    }
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
