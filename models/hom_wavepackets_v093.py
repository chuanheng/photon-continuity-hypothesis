"""v0.93 — HOM of causal Wigner–Weisskopf exponential photon modes.
Gamma is population linewidth. The observable is wavepacket indistinguishability,
not the alleged persistence of a historical photon identity.
"""
import numpy as np
from scipy.special import erfcx
from scipy.integrate import quad

def pure_overlap(g1=1.,g2=1.,detuning=0.,delay=0.):
    """Squared causal exponential-mode inner product, delay=onset2-onset1."""
    if min(g1,g2)<=0:raise ValueError('positive rates')
    return float(4*g1*g2/((g1+g2)**2+4*detuning**2)*
                 np.exp(-g1*max(delay,0.)+g2*min(delay,0.)))

def coincidence(overlap,background_fraction=0.):
    """Ideal two-single-photon coincidence probability per input pair."""
    if not (0<=overlap<=1+1e-12 and 0<=background_fraction<=1):
        raise ValueError('physical parameters required')
    return float((1-(1-background_fraction)*overlap)/2)

def time_jitter_average(gamma=1.,onset_std=0.,correlation=0.):
    if gamma<=0 or onset_std<0 or not(-1<=correlation<=1):
        raise ValueError('invalid jitter')
    relative_sd=np.sqrt(2*(1-correlation))*onset_std
    return float(erfcx(gamma*relative_sd/np.sqrt(2)))

def spectral_jitter_average(gamma=1.,frequency_std=0.,correlation=0.):
    if gamma<=0 or frequency_std<0 or not(-1<=correlation<=1):
        raise ValueError('invalid spectral jitter')
    relative_sd=np.sqrt(2*(1-correlation))*frequency_std
    if relative_sd==0:return 1.
    return float(np.sqrt(np.pi/2)*gamma/relative_sd*
                 erfcx(gamma/(np.sqrt(2)*relative_sd)))

def ensemble_overlap(gamma=1.,onset_std=0.,frequency_std=0.,
                     arrival_correlation=0.,frequency_correlation=0.):
    """Factorization ONLY if relative temporal/frequency noises are independent."""
    return (time_jitter_average(gamma,onset_std,arrival_correlation)*
            spectral_jitter_average(gamma,frequency_std,frequency_correlation))

def monte_carlo_ensemble(n=100000,gamma=1.,onset_std=.2,frequency_std=.3,
                         arrival_correlation=0.,frequency_correlation=0.,seed=9301):
    if n<10 or gamma<=0 or min(onset_std,frequency_std)<0:raise ValueError('simulation settings')
    if not all(-1<=x<=1 for x in (arrival_correlation,frequency_correlation)):
        raise ValueError('correlations')
    rng=np.random.default_rng(seed)
    dt=rng.normal(0,np.sqrt(2*(1-arrival_correlation))*onset_std,n)
    dw=rng.normal(0,np.sqrt(2*(1-frequency_correlation))*frequency_std,n)
    v=gamma**2/(gamma**2+dw**2)*np.exp(-gamma*np.abs(dt))
    return {'mean_overlap':float(v.mean()),
            'mc_standard_error':float(v.std(ddof=1)/np.sqrt(n)),
            'mean_coincidence':float(np.mean((1-v)/2)),
            'n':int(n)}

def numerical_pure_overlap(g1=1.,g2=1.,detuning=0.,delay=0.):
    """Independent complex numerical integral of wavepacket overlap."""
    if min(g1,g2)<=0:raise ValueError('positive rates')
    def fun(t):
        return (np.sqrt(g1*g2)*np.exp(-g1*t/2-g2*(t-delay)/2)*
                np.exp(-1j*detuning*(t-delay)))
    t0=max(0.,delay)
    real=quad(lambda t:fun(t).real,t0,np.inf,epsabs=1e-11)[0]
    imag=quad(lambda t:fun(t).imag,t0,np.inf,epsabs=1e-11)[0]
    return float(abs(real+1j*imag)**2)

def probability_from_states(modes1,modes2,internal1=None,internal2=None):
    """Real physical per-photon internal states DO affect HOM.
    An inaccessible and uncoupled spectator identity is NOT such a state.
    """
    a,b=np.asarray(modes1,complex),np.asarray(modes2,complex)
    if a.ndim!=1 or a.shape!=b.shape or not np.isclose(np.vdot(a,a),1) or not np.isclose(np.vdot(b,b),1):
        raise ValueError('normalized optical modes required')
    m=float(abs(np.vdot(a,b))**2)
    if internal1 is not None or internal2 is not None:
        if internal1 is None or internal2 is None:raise ValueError('both internal states')
        x,y=np.asarray(internal1,complex),np.asarray(internal2,complex)
        if x.shape!=y.shape or not np.isclose(np.vdot(x,x),1) or not np.isclose(np.vdot(y,y),1):
            raise ValueError('normalized internal modes')
        m*=float(abs(np.vdot(x,y))**2)
    return coincidence(m)

def summary():
    names={'identical':(1,1,0,0),
           'detuning_1_gamma':(1,1,1,0),
           'linewidth_1_to_2':(1,2,0,0),
           'arrival_delay_1_lifetime':(1,1,0,1)}
    cases={}
    for name,args in names.items():
        m=pure_overlap(*args)
        cases[name]={'overlap':m,'ideal_coincidence':coincidence(m)}
    scenarios={'no_noise':(0,0,0),
               'independent_noise':(.2,.3,0),
               'fully_common_mode':(.2,.3,1),
               'partially_correlated_08':(.2,.3,.8),
               'independent_more_noise':(.4,.5,0)}
    ensembles={}
    for name,(ts,fs,c) in scenarios.items():
        m=ensemble_overlap(onset_std=ts,frequency_std=fs,
                           arrival_correlation=c,frequency_correlation=c)
        ensembles[name]={'mean_overlap':m,'ideal_coincidence':coincidence(m)}
    return {'version':'v0.93','pure_cases':cases,'ensemble_cases':ensembles,
            'simulation_independent':monte_carlo_ensemble(),
            'physics_note':'Standard HOM mode overlap; no permanent photon identity prediction.'}
