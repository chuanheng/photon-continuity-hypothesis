"""v1.22-v1.31: operational identity and conservation toy-model research.
Standard-library only. All units arbitrary; not a QED calculation or laboratory data.
Run: python3 models/identity_mechanisms_v122_v131.py
"""
import json
import math
import random
from itertools import product

SEED=20261116
HARD=3.0
SOFT=1.0
E3=3.0
E2=2.0
BASE_SOFT=.04
EXTRA=.015
EFF=.7
DARK=.01
N=10000

def kl_bernoulli(p,q):
    if not (0<p<1 and 0<q<1):
        raise ValueError("probabilities must be interior")
    return p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))

def norm(v):
    return math.sqrt(sum(x*x for x in v))

def householder_to(v):
    """Orthogonal 3x3 reflection taking e0 to normalized real v."""
    if abs(norm(v)-1)>1e-11: raise ValueError("v must be normalized")
    e=(1.,0.,0.)
    a=[x-y for x,y in zip(e,v)]
    length=norm(a)
    if length<1e-12:return [[float(i==j) for j in range(3)] for i in range(3)]
    u=[x/length for x in a]
    return [[float(i==j)-2*u[i]*u[j] for j in range(3)] for i in range(3)]

def matmul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

def scatter_matrix(transmit=.7, absorb=.25, soft=.05):
    if min(transmit,absorb,soft)<0 or abs(transmit+absorb+soft-1)>1e-11:
        raise ValueError("probabilities must be nonnegative and normalized")
    v=[math.sqrt(transmit),math.sqrt(absorb),math.sqrt(soft)]
    return householder_to(v)

def detector_prob(soft_probability,eta=EFF,dark=DARK):
    """A soft hit detected with eta OR independent dark click with prob dark."""
    if not all(0<=x<=1 for x in (soft_probability,eta,dark)):
        raise ValueError("probability out of range")
    return dark+(1-dark)*soft_probability*eta

def count_clicks(n,p,seed):
    rng=random.Random(seed)
    return sum(rng.random()<p for _ in range(n))

def log_lr(count,n,p1,p0):
    return count*math.log(p1/p0)+(n-count)*math.log((1-p1)/(1-p0))

def approx_detection_power(n,p0,p1,alpha=.05):
    """Normal approximation to one-sided binomial score test, not exact power."""
    z=1.6448536269514722 if alpha==.05 else None
    if z is None: raise ValueError("only alpha=.05 supported")
    threshold=n*p0+z*math.sqrt(n*p0*(1-p0))
    mean=n*p1
    std=math.sqrt(n*p1*(1-p1))
    return .5*math.erfc((threshold-mean)/(std*math.sqrt(2)))

def gram2(J):
    return [[sum(row[i]*row[j] for row in J) for j in range(len(J[0]))] for i in range(len(J[0]))]

def eig2_sym(M):
    a,b=M[0];c=M[1][1]
    return ((a+c)-math.sqrt((a-c)**2+4*b*b))/2,((a+c)+math.sqrt((a-c)**2+4*b*b))/2

def run():
    out={}
    # v1.22: labels not coupled to observables
    out["v1.22"]={"operational_KL_if_label_only":0.0,"conclusion":"identical likelihood for any sample size"}
    # v1.23: impossible fixed-hard-photon plus target excitation without energy sink
    out["v1.23"]={"initial_energy":HARD,"hard_plus_excitation":HARD+E2,
                  "energy_mismatch":E2,"conclusion":"requires energy source/sink"}
    # v1.24: an energy-conserving exit channel, not a new identity effect
    out["v1.24"]={"absorption_branch":E3,"soft_branch":E2+SOFT,
                  "both_equal_initial":abs(E3-HARD)<1e-12 and abs(E2+SOFT-HARD)<1e-12}
    # v1.25: exact energy conserving unitary *within degenerate three-state subspace*
    U=scatter_matrix(.7,.25,.05)
    orth=matmul(U,[[U[j][i] for j in range(3)] for i in range(3)])
    out["v1.25"]={"maximum_orthogonality_error":max(abs(orth[i][j]-int(i==j)) for i,j in product(range(3),repeat=2)),
                  "first_column_probabilities":[U[i][0]**2 for i in range(3)]}
    # v1.26: detector + backgrounds
    p0=detector_prob(BASE_SOFT)
    p1=detector_prob(BASE_SOFT+EXTRA)
    out["v1.26"]={"b0":BASE_SOFT,"b1":BASE_SOFT+EXTRA,"p0":p0,"p1":p1,
                  "KL_per_trial":kl_bernoulli(p1,p0),"expected_log_LR_at_10k":N*kl_bernoulli(p1,p0)}
    # v1.27: calibration mismatch causes exact observational degeneracy
    # Identity model b0+delta vs standard model b0'=b0+delta.
    out["v1.27"]={"alternative_soft_probability":BASE_SOFT+EXTRA,
                  "standard_refit_soft_probability":BASE_SOFT+EXTRA,
                  "best_fit_KL":0.0,"conclusion":"additional soft channel alone does not identify persistent identity"}
    # v1.28: same eta, unknown dark & soft b => rank 1 in one Bernoulli channel
    b=BASE_SOFT
    d=DARK
    deriv_b=(1-d)*EFF
    deriv_d=1-b*EFF
    j1=[[deriv_b,deriv_d]]
    lam1=eig2_sym(gram2(j1))
    out["v1.28"]={"one_setting_Fisher_JtJ_eigenvalues":list(lam1),"rank":1}
    # v1.29: two different efficiencies and shared dark => rank 2 locally
    eta2=.9
    J=[[(1-d)*e,1-b*e] for e in (EFF,eta2)]
    lam2=eig2_sym(gram2(J))
    out["v1.29"]={"efficiencies":[EFF,eta2],"two_setting_JtJ_eigenvalues":list(lam2),
                  "determinant":lam2[0]*lam2[1],"rank":2 if lam2[0]>1e-12 else 1}
    # v1.30: actual seeded count sampling + fixed-hypothesis power proxy
    count0=count_clicks(N,p0,SEED)
    count1=count_clicks(N,p1,SEED+1)
    out["v1.30"]={"n":N,"count_null":count0,"count_alternative":count1,
                  "alt_logLR":log_lr(count1,N,p1,p0),
                  "normal_approx_one_sided_power":approx_detection_power(N,p0,p1)}
    # v1.31: explicit decision gate: b0 unknown => no unique signature
    out["v1.31"]={"novel_identity_specific_observable":False,
                  "identifiable_new_parameter_without_baseline_constraint":False,
                  "scientific_status":"untested; no distinct prediction from standard optics/QED"}
    return out

if __name__=="__main__":
    print(json.dumps(run(),ensure_ascii=False,indent=2,sort_keys=True))
