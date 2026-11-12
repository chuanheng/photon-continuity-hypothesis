"""Energy and mass-shell bookkeeping for a hypothetical photon successor.

Illustrative only: no transition amplitude, scattering cross section, or
empirical evidence of a hidden particle. Energies are in consistent units.
"""
import math

def successor_energy(incident, material_gain, other_outgoing=0.0):
    values=(incident,material_gain,other_outgoing)
    if any(not math.isfinite(x) or x<0 for x in values) or incident<=0:
        raise ValueError("energies must be finite, nonnegative, incident > 0")
    residual=incident-material_gain-other_outgoing
    if residual<=0:
        raise ValueError("strict successor hypothesis requires positive residual energy")
    return residual

def massless_successor_momentum(energy, speed_of_light=299792458.0):
    if not math.isfinite(energy) or energy<=0:
        raise ValueError("energy must be finite and positive")
    if not math.isfinite(speed_of_light) or speed_of_light<=0:
        raise ValueError("speed_of_light must be finite and positive")
    return energy/speed_of_light

def detectable_above_threshold(successor, threshold):
    if any(not math.isfinite(x) for x in (successor,threshold)) or successor<=0 or threshold<0:
        raise ValueError("invalid energy or threshold")
    return successor>=threshold

if __name__=="__main__":
    for gain in (59.,59.9,59.999):
        residual=successor_energy(60.,gain)
        print(f"incident=60, material gain={gain:g}, residual={residual:.6g} (same energy units)")
    print("This is a conservation ledger, not evidence of photon persistence.")
