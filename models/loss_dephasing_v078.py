"""v0.78: open-system interference counts with loss and dephasing.
Identical permanent-label and ordinary-memory predictions are statistically
indistinguishable. Toy model, NOT QED.
"""
import numpy as np

def validate(eta,visibility):
    if not (0<=eta<=1 and 0<=visibility<=1):raise ValueError('probability range')

def state(eta,visibility,phase):
    validate(eta,visibility)
    rho=np.zeros((3,3),complex)
    rho[0,0]=1-eta
    rho[1,1]=rho[2,2]=eta/2
    rho[1,2]=eta*visibility*np.exp(1j*phase)/2
    rho[2,1]=rho[1,2].conjugate()
    return rho

def probabilities(eta,visibility,phase):
    rho=state(eta,visibility,phase)
    plus=np.array([0,1,1])/np.sqrt(2)
    minus=np.array([0,1,-1])/np.sqrt(2)
    return np.array([float(rho[0,0].real),
        float(np.vdot(plus,rho@plus).real),
        float(np.vdot(minus,rho@minus).real)])

def memory_probabilities(eta,visibility,phase):
    return probabilities(eta,visibility,phase)

def total_variation(p,q):
    return float(np.abs(np.asarray(p)-np.asarray(q)).sum()/2)

def kl_divergence(p,q):
    p,q=np.asarray(p,float),np.asarray(q,float)
    if p.shape!=q.shape or not np.allclose(p.sum(),1) or not np.allclose(q.sum(),1):
        raise ValueError('not normalized')
    if np.any(p<0) or np.any(q<0):raise ValueError('negative probability')
    if np.any((p>0)&(q==0)):return float('inf')
    mask=p>0
    return float(np.sum(p[mask]*np.log(p[mask]/q[mask])))

def expected_llr(n,alternative,null):
    return n*kl_divergence(alternative,null)

def sample_counts(n,p,seed=77):
    if n<0 or int(n)!=n:raise ValueError('nonnegative integer count required')
    return np.random.default_rng(seed).multinomial(n,p)

def log_likelihood_ratio(counts,alternative,null):
    counts=np.asarray(counts,int)
    if np.any(counts<0):raise ValueError('negative counts')
    pa,pn=np.asarray(alternative,float),np.asarray(null,float)
    if np.any((counts>0)&(pn==0)):return float('inf')
    if np.any((counts>0)&(pa==0)):return -float('inf')
    mask=counts>0
    return float(np.sum(counts[mask]*np.log(pa[mask]/pn[mask])))

def fisher_phase(eta,visibility,phase):
    p=probabilities(eta,visibility,phase)
    dp=np.array([0,-eta*visibility*np.sin(phase)/2,
                    eta*visibility*np.sin(phase)/2])
    if np.any((p==0)&(dp!=0)):return float('inf')
    mask=p>0
    return float(np.sum(dp[mask]**2/p[mask]))

def summary():
    eta,v,phi,delta,n=.65,.8,np.pi/2,.2,1000
    p0=probabilities(eta,v,phi)
    p1=probabilities(eta,v,phi+delta)
    return {'eta':eta,'visibility':v,'phase_rad':float(phi),
        'alternative_phase_offset_rad':delta,'n':n,
        'identity_probability':p0.tolist(),
        'memory_probability':memory_probabilities(eta,v,phi).tolist(),
        'alternative_probability':p1.tolist(),
        'identity_vs_memory_total_variation':
             total_variation(p0,memory_probabilities(eta,v,phi)),
        'identity_vs_memory_kl':kl_divergence(p0,memory_probabilities(eta,v,phi)),
        'phase_offset_kl_per_trial':kl_divergence(p1,p0),
        'expected_twice_llr_n1000':2*expected_llr(n,p1,p0),
        'fisher_phase_per_trial':fisher_phase(eta,v,phi),
        'fisher_phase_n1000':n*fisher_phase(eta,v,phi),
        'simulated_counts_alternative':sample_counts(n,p1).tolist()}
