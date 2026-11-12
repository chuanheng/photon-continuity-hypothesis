"""Exact closed single-excitation Jaynes-Cummings populations, hbar=1.
One field mode only; not a model of all photon modes or photon identity.
"""
import math

def populations(coupling, detuning, time):
    """Return P(|g,1>), P(|e,0>) for initial |g,1>."""
    if any(not math.isfinite(v) for v in (coupling,detuning,time)):
        raise ValueError("inputs must be finite")
    if coupling<0 or time<0:
        raise ValueError("coupling and time must be nonnegative")
    omega=math.hypot(detuning,2*coupling)
    if omega==0:
        return 1.0,0.0
    excited=(2*coupling/omega)**2*math.sin(omega*time/2)**2
    return 1.0-excited,excited

def minimum_mode_photon_probability(coupling,detuning):
    if any(not math.isfinite(v) for v in (coupling,detuning)) or coupling<0:
        raise ValueError("invalid parameters")
    omega=math.hypot(detuning,2*coupling)
    return 1.0 if omega==0 else 1.0-(2*coupling/omega)**2

if __name__=="__main__":
    print("gt,P_mode_1,P_atom_excited (resonant ideal JC model)")
    for i in range(13):
        x=math.pi*i/12
        a,b=populations(1,0,x)
        print(f"{x:.6f},{a:.8f},{b:.8f}")
