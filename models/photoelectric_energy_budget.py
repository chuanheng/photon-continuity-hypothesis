"""Simplified photoelectric energy accounting (illustrative, NOT a cross-section model).

The budget omits relativistic recoil kinematics and cannot establish a
physical extra-photon emission process. Energies in keV.
"""
import math

def electron_energy_budget(incident_kev, binding_kev, extra_photon_kev=0.,
                           recoil_kev=0., other_kev=0.):
    values=(incident_kev,binding_kev,extra_photon_kev,recoil_kev,other_kev)
    if any(not math.isfinite(v) or v<0 for v in values):
        raise ValueError("all energy inputs must be finite and nonnegative")
    electron_kev=incident_kev-binding_kev-extra_photon_kev-recoil_kev-other_kev
    if electron_kev<0:
        raise ValueError("energy budget has no nonnegative electron kinetic energy")
    return electron_kev

def difference_from_standard(extra_photon_kev,recoil_kev=0.,other_kev=0.):
    """Shift relative to a zero-recoil, no-extra-radiation baseline."""
    return -(extra_photon_kev+recoil_kev+other_kev)

if __name__=="__main__":
    e,b=60.,1.56 # binding energy is an illustrative input, not a calibrated Al subshell
    print("Toy energy accounting only; no experimental inference")
    for extra in (0.,0.001,0.01,0.1):
        print(f"extra photon {extra:g} keV: electron budget {electron_energy_budget(e,b,extra):.6f} keV")
