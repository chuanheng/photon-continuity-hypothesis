"""Ideal one-shot emitter with independent Poisson dark counts.

No detector dead time, afterpulsing, or repeated excitation. The g2(0)
function applies only to a single-photon Fock-state source, not arbitrary light.
"""
import math

def _validate(rate, time, efficiency, dark_rate):
    if not all(math.isfinite(v) for v in (rate, time, efficiency, dark_rate)):
        raise ValueError('all parameters must be finite')
    if rate < 0 or time < 0 or dark_rate < 0 or not 0 <= efficiency <= 1:
        raise ValueError('invalid rate, time, dark rate, or efficiency')

def signal_click_probability(rate, time, efficiency):
    _validate(rate, time, efficiency, 0)
    return efficiency * (-math.expm1(-rate * time))

def no_click_probability(rate, time, efficiency, dark_rate=0):
    _validate(rate, time, efficiency, dark_rate)
    return math.exp(-dark_rate * time) * (1 - signal_click_probability(rate, time, efficiency))

def any_click_probability(rate, time, efficiency, dark_rate=0):
    return 1 - no_click_probability(rate, time, efficiency, dark_rate)

def first_signal_click_density(rate, time, efficiency):
    _validate(rate, time, efficiency, 0)
    return efficiency * rate * math.exp(-rate * time)

def fock_g2_zero(photon_number):
    """g2(0)=n(n-1)/n² for an exact n-photon number state; n>0."""
    if isinstance(photon_number, bool) or not isinstance(photon_number, int) or photon_number <= 0:
        raise ValueError('photon_number must be a positive integer')
    return (photon_number - 1) / photon_number
