"""Phenomenological two-channel Fermi-golden-rule model (not QED)."""
import math

def golden_rule_rate(matrix_element, density, hbar=1.0):
    """2*pi/hbar * |V|^2 * rho for nonnegative continuum density."""
    if not isinstance(matrix_element, (int, float, complex)):
        raise ValueError('invalid matrix element')
    vals=(complex(matrix_element).real, complex(matrix_element).imag, density, hbar)
    if not all(math.isfinite(x) for x in vals) or density < 0 or hbar <= 0:
        raise ValueError('invalid physical parameters')
    return (2*math.pi/hbar)*abs(matrix_element)**2*density

def branching_rates(successor_rate, absorption_rate):
    if not all(math.isfinite(x) for x in (successor_rate, absorption_rate)) or min(successor_rate, absorption_rate)<0:
        raise ValueError('rates must be nonnegative and finite')
    total=successor_rate+absorption_rate
    if not math.isfinite(total):
        raise ValueError('rate overflow')
    if total==0:
        return (0.0,0.0)
    return (successor_rate/total, absorption_rate/total)

def transition_probability(total_rate, time):
    if not all(math.isfinite(x) for x in (total_rate,time)) or total_rate<0 or time<0:
        raise ValueError('invalid rate or time')
    return -math.expm1(-total_rate*time)

def resolved_successor_probability(successor_rate, absorption_rate, time, efficiency):
    if not math.isfinite(efficiency) or not 0<=efficiency<=1:
        raise ValueError('invalid efficiency')
    b,_=branching_rates(successor_rate,absorption_rate)
    return efficiency*b*transition_probability(successor_rate+absorption_rate,time)

def continuum_density_3d(kinetic_energy, coefficient=1.0):
    """Illustrative nonrelativistic free-particle 3D DOS proportional to sqrt(K)."""
    if not all(math.isfinite(x) for x in (kinetic_energy,coefficient)) or kinetic_energy<0 or coefficient<0:
        raise ValueError('invalid energy or coefficient')
    return coefficient*math.sqrt(kinetic_energy)
