"""v1.11 joint local Fisher experiment allocation (numpy required).
Run: python -m models.three_photon_v111
Synthetic standard-optics model, NOT an identity test.
"""
import math
import numpy as np
from models.three_photon_v110 import output_probabilities, detected_probabilities

THETA=np.array([.30,math.pi/3,.08,.86,.82,.90])
PARAMS=('r','phi','eps','eta0','eta1','eta2')
BASE=(10000,1000,1000,1000)

def distribution(t):
    r,phi,eps,*eta=map(float,t)
    raw=output_probabilities(r,phi,eps)
    detected=detected_probabilities(raw,eta)
    keys=[(a,b,c) for a in range(4) for b in range(4-a) for c in range(4-a-b)]
    return np.array([detected.get(k,0) for k in keys],dtype=float)

def main_info(t=THETA,step=1e-5):
    p=distribution(t)
    j=np.zeros((len(p),len(t)))
    for k in range(len(t)):
        x=t.copy();y=t.copy();x[k]+=step;y[k]-=step
        j[:,k]=(distribution(x)-distribution(y))/(2*step)
    assert np.all(p>0), 'strictly interior probability distribution required'
    return (j.T/p)@j

def bernoulli_info(p,dp):
    return np.outer(dp,dp)/(p*(1-p))

def ref_info(t=THETA):
    # HOM-type two-photon coincidence probability p=(1-r^2)/2
    r=t[0];dp=np.zeros(6);dp[0]=-r
    return bernoulli_info((1-r*r)/2,dp)

def eta_info(t=THETA):
    # One known photon per detector per calibration trial (3 photons total).
    z=np.zeros((6,6))
    for j in range(3):
        dp=np.zeros(6);dp[j+3]=1
        z+=bernoulli_info(t[j+3],dp)
    return z

def eps_info(t=THETA):
    # Dedicated single Bernoulli optical-angle reference, p=sin(pi/4+eps)^2
    eps=t[2];p=math.sin(math.pi/4+eps)**2
    dp=np.zeros(6);dp[2]=math.sin(2*(math.pi/4+eps))
    return bernoulli_info(p,dp)

def info(nmain,nref,neta,neps):
    return nmain*main_info()+nref*ref_info()+neta*eta_info()+neps*eps_info()

def metrics(allocation):
    f=info(*allocation); eig=np.linalg.eigvalsh(f)
    if eig[0]<=1e-8:return None
    cov=np.linalg.inv(f)
    return {'sd_phi':float(math.sqrt(cov[1,1])),
            'sd_r':float(math.sqrt(cov[0,0])),
            'min_eigenvalue':float(eig[0]),
            'cond':float(eig[-1]/eig[0])}

def allocations(total=10000,base=BASE,step=1000):
    """Grid across four integer shot allocations; 1 shot = 1 accounting unit."""
    if total%step:raise ValueError('total must be a multiple of step')
    res=[]
    for a in range(0,total+1,step):
        for b in range(0,total-a+1,step):
            for c in range(0,total-a-b+1,step):
                d=total-a-b-c
                inc=(a,b,c,d)
                m=metrics(tuple(x+y for x,y in zip(base,inc)))
                if m:res.append((inc,m))
    return res

def report():
    print('baseline',metrics(BASE))
    scenarios={'main':(10000,0,0,0),'HOM':(0,10000,0,0),
               'eta':(0,0,10000,0),'eps':(0,0,0,10000),
               'equal':(2500,2500,2500,2500)}
    for name,inc in scenarios.items():
        print(name,inc,metrics(tuple(a+b for a,b in zip(BASE,inc))))
    candidates=allocations()
    print('candidate_count',len(candidates))
    print('best',min(candidates,key=lambda t:t[1]['sd_phi']))
    print('main rank',np.linalg.matrix_rank(main_info(),tol=1e-8))
    print('main eigenvalues',np.linalg.eigvalsh(main_info()))

if __name__=='__main__':report()
