"""Phenomenological successor-channel detection model, not derived from QED."""
import math

def _check(kappa, absorption, efficiency):
    if not all(math.isfinite(v) for v in (kappa,absorption,efficiency)):
        raise ValueError("finite parameters required")
    if kappa<0 or absorption<0 or kappa+absorption==0 or not 0<=efficiency<=1:
        raise ValueError("invalid coupling or efficiency")

def branch_probabilities(kappa, absorption):
    _check(kappa,absorption,1)
    norm=math.hypot(kappa,absorption)
    return (kappa/norm)**2,(absorption/norm)**2

def successor_click_probability(kappa, absorption, efficiency, successor_energy, threshold):
    _check(kappa,absorption,efficiency)
    if not math.isfinite(successor_energy) or not math.isfinite(threshold) or successor_energy<=0 or threshold<0:
        raise ValueError("invalid energy or threshold")
    return efficiency*branch_probabilities(kappa,absorption)[0] if successor_energy>=threshold else 0.0

def binomial_log_likelihood(clicks,trials,probability):
    if (not isinstance(clicks,int) or isinstance(clicks,bool) or
        not isinstance(trials,int) or isinstance(trials,bool) or
        trials<0 or not 0<=clicks<=trials):
        raise ValueError("invalid counts")
    if not math.isfinite(probability) or not 0<=probability<=1:
        raise ValueError("invalid probability")
    if probability==0: return 0.0 if clicks==0 else -math.inf
    if probability==1: return 0.0 if clicks==trials else -math.inf
    return (math.lgamma(trials+1)-math.lgamma(clicks+1)-math.lgamma(trials-clicks+1)
            +clicks*math.log(probability)+(trials-clicks)*math.log1p(-probability))

def log_likelihood_ratio(clicks,trials,probability_a,probability_reference):
    return binomial_log_likelihood(clicks,trials,probability_a)-binomial_log_likelihood(clicks,trials,probability_reference)
