"""Markovian undriven two-level spontaneous emission; no photon identity claim."""
import math

def _validate(rate,time):
    if not math.isfinite(rate) or not math.isfinite(time) or rate<0 or time<0:
        raise ValueError('rate and time must be finite and nonnegative')

def excited_population(rate,time):
    _validate(rate,time)
    return math.exp(-rate*time)

def emitted_by_time(rate,time):
    _validate(rate,time)
    return -math.expm1(-rate*time)

def waiting_time_density(rate,time):
    _validate(rate,time)
    return rate*math.exp(-rate*time)

def emission_quantile(rate,probability):
    if not math.isfinite(rate) or rate<=0:
        raise ValueError('rate must be finite and positive')
    if not math.isfinite(probability) or not 0<=probability<1:
        raise ValueError('probability must be in [0,1)')
    return -math.log1p(-probability)/rate

def density_matrix(initial_excited,initial_coherence,rate,time):
    """((rho_ee,rho_eg),(rho_ge,rho_gg)) in rotating frame."""
    _validate(rate,time)
    if not isinstance(initial_coherence,complex):
        initial_coherence=complex(initial_coherence)
    if not math.isfinite(initial_excited) or not 0<=initial_excited<=1:
        raise ValueError('initial population outside [0,1]')
    if not all(math.isfinite(x) for x in (initial_coherence.real,initial_coherence.imag)):
        raise ValueError('nonfinite coherence')
    if abs(initial_coherence)**2>initial_excited*(1-initial_excited)+1e-14:
        raise ValueError('initial density matrix is not positive')
    e=math.exp(-rate*time)
    rho_ee=initial_excited*e
    rho_eg=initial_coherence*math.exp(-rate*time/2)
    return ((rho_ee,rho_eg),(rho_eg.conjugate(),1-rho_ee))
