"""Minimal three-state quantum toy model for direction A; not QED.

Basis: |g,1H,0L>, |e,0H,1L>, |e,0H,0L>.
Hamiltonian hbar=1:
[[0, k, a],
 [k, d, b],
 [a, b, D]]
The last basis state has no photons. The 'survival-only' model sets a=b=0,
which is a stipulated selection rule, not a derived physical mechanism.
Only the survival subblock is analytically propagated here.
"""
import math

def survival_populations(k, detuning, time):
    """Exact populations (high photon, low photon, vacuum) when a=b=0."""
    if any(not math.isfinite(v) for v in (k,detuning,time)):
        raise ValueError("finite parameters required")
    if k<0 or time<0:
        raise ValueError("k and time must be nonnegative")
    omega=math.hypot(detuning,2*k)
    low=0. if omega==0 else (2*k/omega)**2*math.sin(omega*time/2)**2
    return (1-low,low,0.)

def forbidden_channel_population(coupling, time):
    """Resonant 2-state absorption |g,1H> <-> |e,0> for contrast."""
    if not math.isfinite(coupling) or not math.isfinite(time) or coupling<0 or time<0:
        raise ValueError("invalid parameters")
    return math.sin(coupling*time)**2

def energy_bookkeeping(high_energy,low_energy,atomic_gap):
    """Detuning between high photon and excited atom plus low photon."""
    if any(not math.isfinite(v) or v<=0 for v in (high_energy,low_energy,atomic_gap)):
        raise ValueError("energies must be positive finite")
    return atomic_gap+low_energy-high_energy

if __name__=="__main__":
    print("Ideal toy model; photon persistence is imposed, not proven")
    for t in (0.,math.pi/4,math.pi/2,math.pi):
        print(f"kt={t:.6f}, probabilities={survival_populations(1.,0.,t)}")
    print("Example detuning:",energy_bookkeeping(60.,.001,59.999))
