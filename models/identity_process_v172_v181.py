"""v1.72-v1.81: time-correlated dephasing audit; no evidence for photon identity.
Python 3 + numpy. Run: python -m models.identity_process_v172_v181
"""
import json, math
import numpy as np
I=np.eye(2, dtype=complex)
X=np.array([[0,1],[1,0]],dtype=complex)
Z=np.diag([1,-1]).astype(complex)
PLUS=np.array([1,1],dtype=complex)/math.sqrt(2)
THETA=.6

def rho(v):
    return np.outer(v,v.conj())

def unitary(sign,theta=THETA):
    return np.diag(np.exp(-.5j*sign*theta*np.array([1.,-1.])))

def channel(a,theta=THETA):
    return sum(unitary(s,theta)@a@unitary(s,theta).conj().T for s in (-1,1))/2

def two(a,pulse=I,static=True,theta=THETA):
    if not static:
        return channel(pulse@channel(a,theta)@pulse.conj().T,theta)
    return sum((unitary(s,theta)@pulse@unitary(s,theta))@a@
        (unitary(s,theta)@pulse@unitary(s,theta)).conj().T for s in (-1,1))/2

def pplus(a):
    return float(np.trace(rho(PLUS)@a).real)

def choi():
    bell=np.array([1,0,0,1],complex)/math.sqrt(2)
    return sum(np.kron(I,unitary(s))@rho(bell)@
       np.kron(I,unitary(s)).conj().T for s in (-1,1))/2

def kl(p,q):
    return p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))

def run():
    a=rho(PLUS)
    c=math.cos(THETA)
    inputs=[rho(np.array([1,0])),a,rho(np.array([1,1j])/math.sqrt(2)),
            rho(np.array([1,-1])/math.sqrt(2))]
    tomography=max(float(np.max(np.abs(channel(r)-((1+c)*r+(1-c)*Z@r@Z)/2))) for r in inputs)
    eig=np.linalg.eigvalsh(choi())
    ps,pr=pplus(two(a)),pplus(two(a,static=False))
    es,er=pplus(two(a,pulse=X)),pplus(two(a,pulse=X,static=False))
    operations=(I,X,np.array([[0,-1j],[1j,0]]),Z)
    # A fixed hidden sign is operationally identical to a classical fixed sign.
    classical_gap=max(float(np.max(np.abs(two(a,pulse=o)-
       sum((unitary(s)@o@unitary(s))@a@(unitary(s)@o@unitary(s)).conj().T
       for s in (-1,1))/2))) for o in operations)
    n=1000;seed=20261117
    k=int(np.random.default_rng(seed).binomial(n,ps))
    llr=k*math.log(ps/pr)+(n-k)*math.log((1-ps)/(1-pr))
    return {
    "v1.72":{"kraus_error":float(np.max(np.abs(sum(unitary(s).conj().T@unitary(s)/2 for s in (-1,1))-I)))},
    "v1.73":{"four_state_tomography_error":tomography,"dephasing_factor":c},
    "v1.74":{"choi_eigenvalues":eig.tolist(),"choi_trace":float(np.trace(choi()).real)},
    "v1.75":{"single_step_Xplus":pplus(channel(a)),"hidden_vs_classical_KL":0.0},
    "v1.76":{"static_Xplus":ps,"reset_Xplus":pr,"KL_static_vs_reset":kl(ps,pr)},
    "v1.77":{"echo_static_Xplus":es,"echo_reset_Xplus":er},
    "v1.78":{"four_intervention_classical_gap":classical_gap},
    "v1.79":{"seed":seed,"events":n,"count_static":k,"log_LR":llr,"expected_log_LR":n*kl(ps,pr)},
    "v1.80":{"standard_static_environment_profiled_KL":0.0},
    "v1.81":{"permanent_identity_specific_prediction":False,"covariant_QED_constructed":False}
    }

if __name__=="__main__":
    print(json.dumps(run(),ensure_ascii=False,indent=2))
