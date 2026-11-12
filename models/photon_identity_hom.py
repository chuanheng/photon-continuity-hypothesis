"""Ideal HOM coincidence model; overlap squared between 0 and 1."""
import math

def coincidence_probability(overlap_squared):
    if not math.isfinite(overlap_squared) or not 0 <= overlap_squared <= 1:
        raise ValueError('overlap_squared must be finite in [0,1]')
    return (1-overlap_squared)/2

def bunching_probability(overlap_squared):
    return 1-coincidence_probability(overlap_squared)

def gaussian_delay_coincidence(delay, coherence_time):
    if not math.isfinite(delay) or not math.isfinite(coherence_time) or coherence_time<=0:
        raise ValueError('finite delay and positive coherence time required')
    return coincidence_probability(math.exp(-(delay/coherence_time)**2))
