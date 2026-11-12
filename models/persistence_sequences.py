"""Mathematical persistence sequences, not a physical photon interaction theory."""
import math

def fractional_energy(initial_energy, alpha, interactions):
    if not math.isfinite(initial_energy) or initial_energy<=0:
        raise ValueError("initial energy must be positive finite")
    if not math.isfinite(alpha) or not 0<alpha<1:
        raise ValueError("alpha must be between zero and one")
    if not isinstance(interactions,int) or interactions<0:
        raise ValueError("interactions must be a nonnegative integer")
    return initial_energy*(1-alpha)**interactions

def expected_poisson_energy(initial_energy, alpha, rate_per_length, length):
    if not math.isfinite(initial_energy) or initial_energy<=0:
        raise ValueError("initial energy must be positive finite")
    if not math.isfinite(alpha) or not 0<alpha<1:
        raise ValueError("alpha must be between zero and one")
    if any(not math.isfinite(x) or x<0 for x in (rate_per_length,length)):
        raise ValueError("rate and length must be nonnegative finite")
    return initial_energy*math.exp(-alpha*rate_per_length*length)

def fixed_gap_energy(initial_energy, gap, interactions):
    if not math.isfinite(initial_energy) or initial_energy<=0:
        raise ValueError("initial energy must be positive finite")
    if not math.isfinite(gap) or gap<=0:
        raise ValueError("gap must be positive finite")
    if not isinstance(interactions,int) or interactions<0:
        raise ValueError("interactions must be a nonnegative integer")
    remaining=initial_energy-gap*interactions
    if remaining<=0:
        raise ValueError("fixed gap events cannot continue with positive energy")
    return remaining

if __name__=="__main__":
    print("Illustrative mathematical sequences; NOT experimental evidence")
    for n in (0,1,10,100):
        print(n,fractional_energy(60,.1,n))
