"""Leading-log independent soft-photon Poisson toy and an extra-successor toy.
Not a full QED calculation. The additional successor is a distinct, assumed signal.
"""
import math

def mean_resolved_photons(beta, threshold, upper):
    if not all(math.isfinite(x) for x in (beta,threshold,upper)) or beta<0 or threshold<=0 or upper<=0:
        raise ValueError('invalid inputs')
    if threshold>=upper: return 0.0
    return beta*math.log(upper/threshold)

def standard_click_probability(beta, threshold, upper, efficiency=1.0):
    if not math.isfinite(efficiency) or not 0<=efficiency<=1: raise ValueError('invalid efficiency')
    return -math.expm1(-efficiency*mean_resolved_photons(beta,threshold,upper))

def successor_click_probability(beta, threshold, upper, successor_energy, successor_efficiency=1.0, soft_efficiency=1.0):
    if not math.isfinite(successor_energy) or successor_energy<=0: raise ValueError('invalid successor energy')
    if not math.isfinite(successor_efficiency) or not 0<=successor_efficiency<=1: raise ValueError('invalid successor efficiency')
    baseline=standard_click_probability(beta,threshold,upper,soft_efficiency)
    detected=successor_efficiency if successor_energy>=threshold else 0.0
    return 1-(1-baseline)*(1-detected)

def click_excess(beta, threshold, upper, successor_energy, successor_efficiency=1.0, soft_efficiency=1.0):
    return successor_click_probability(beta,threshold,upper,successor_energy,successor_efficiency,soft_efficiency)-standard_click_probability(beta,threshold,upper,soft_efficiency)
