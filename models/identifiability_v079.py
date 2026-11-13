"""v0.79: phase-offset confounding and calibrated intervention.
Finite-dimensional statistical model, NOT photon-QED or evidence of identity.
"""
import numpy as np

def physical_prob(eta, visibility, dark, x, beta, delta=0., z=1.):
    """Dark counts as a symmetric, normalized background over 3 outcomes."""
    if not (0 <= eta <= 1 and 0 <= visibility <= 1 and 0 <= dark <= 1):
        raise ValueError('eta, visibility, dark must be in [0,1]')
    theta = x + beta + z * delta
    p = np.array([1-eta, eta * (1+visibility*np.cos(theta))/2,
                  eta * (1-visibility*np.cos(theta))/2])
    return (1-dark)*p + dark*np.ones(3)/3

def effective(eta, visibility, dark):
    return ((1-dark)*(1-eta)+dark/3, (1-dark)*eta*visibility)

def reduced_prob(loss, amplitude, x, beta, delta=0., z=1.):
    if not (0 <= loss < 1 and 0 <= amplitude <= 1-loss):
        raise ValueError('invalid effective parameters')
    contrast = amplitude*np.cos(x+beta+z*delta)
    return np.array([loss, (1-loss+contrast)/2, (1-loss-contrast)/2])

def kl(p, q):
    p, q = np.asarray(p,float), np.asarray(q,float)
    if p.shape != q.shape or np.any(p < 0) or np.any(q < 0) or not np.isclose(p.sum(),1) or not np.isclose(q.sum(),1):
        raise ValueError('invalid distributions')
    if np.any((p>0)&(q==0)):
        return np.inf
    mask=p>0
    return float(np.sum(p[mask]*np.log(p[mask]/q[mask])))

def grad_reduced(loss, amplitude, x, beta, delta, z):
    """Columns correspond to (loss, amplitude, beta, delta)."""
    t = x+beta+z*delta
    c, s = np.cos(t), np.sin(t)
    return np.array([[1,0,0,0],
       [-.5,c/2,-amplitude*s/2,-z*amplitude*s/2],
       [-.5,-c/2,amplitude*s/2,z*amplitude*s/2]],float)

def fisher_reduced(loss,amplitude,beta,delta,conditions,n_each=1000):
    """Expected Fisher for independent multinomial observations.
    Conditions: list of (phase x, intervention z).
    """
    fisher=np.zeros((4,4))
    for x,z in conditions:
        p=reduced_prob(loss,amplitude,x,beta,delta,z)
        if np.min(p) <= 0:raise ValueError('requires strictly positive probabilities')
        g=grad_reduced(loss,amplitude,x,beta,delta,z)
        fisher += n_each * g.T @ np.diag(1/p) @ g
    return fisher

def asimov_deviance(loss,amplitude,beta_true,delta_true,conditions,
                     beta_fit,delta_fit,n_each=1000):
    return float(sum(2*n_each*kl(reduced_prob(loss,amplitude,x,beta_true,delta_true,z),
        reduced_prob(loss,amplitude,x,beta_fit,delta_fit,z)) for x,z in conditions))

def profile_same_group(loss,amplitude,beta_true,delta_true,conditions,delta_grid,n_each=1000):
    """Exact phase reparameterization profile for experiments with z == 1."""
    if not all(z==1 for _,z in conditions):raise ValueError('requires z=1 for all settings')
    return np.array([asimov_deviance(loss,amplitude,beta_true,delta_true,conditions,
        beta_true+delta_true-d, d,n_each) for d in delta_grid])

def subspace_rank(fisher,rtol=1e-9):
    ev=np.linalg.eigvalsh(fisher)
    return int(np.sum(ev > rtol*max(1,float(np.max(np.abs(ev)))))),ev

def conditional_identity_fisher(fisher):
    """Schur complement of 3x3 nuisance block; zero iff identity confounded."""
    nuisance=fisher[:3,:3]
    return float(fisher[3,3]-fisher[3,:3]@np.linalg.pinv(nuisance,rcond=1e-12)@fisher[:3,3])

def summary():
    eta,v,d=.65,.8,.05
    loss,amp=effective(eta,v,d)
    beta,delta=.13,.2
    xs=[.15,.8,1.7,2.5]
    single=[(x,1) for x in xs]
    interventions=[(x,z) for x in xs for z in (0,1)]
    f0=fisher_reduced(loss,amp,beta,delta,single)
    f1=fisher_reduced(loss,amp,beta,delta,interventions)
    r0,e0=subspace_rank(f0)
    r1,e1=subspace_rank(f1)
    grid=np.linspace(-.5,.5,11)
    profile=profile_same_group(loss,amp,beta,delta,single,grid)
    return {'parameters':{'eta':eta,'visibility':v,'dark':d,'effective_loss':loss,
        'effective_amplitude':amp,'beta':beta,'delta':delta,'n_each':1000},
        'single_group_rank':r0,'single_group_fisher_eigenvalues':e0.tolist(),
        'single_group_profile_deviance_max_abs':float(np.max(np.abs(profile))),
        'intervention_rank':r1,'intervention_fisher_eigenvalues':e1.tolist(),
        'intervention_conditional_delta_fisher':conditional_identity_fisher(f1),
        'no_intervention_conditional_delta_fisher':conditional_identity_fisher(f0),
        'single_condition_example':physical_prob(eta,v,d,np.pi/2,beta,delta,1).tolist(),
        'intervention_asimov_deviance_delta_fixed_zero_beta_true':
        asimov_deviance(loss,amp,beta,delta,interventions,beta,0)}
