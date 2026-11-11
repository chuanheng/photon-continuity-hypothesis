"""NIST-based uncollided narrow-beam reference, not a full transport simulation.

Source: https://physics.nist.gov/PhysRefData/XrayMassCoef/ElemTab/z13.html
NIST Al at 0.060 MeV: mass attenuation = 0.2778 cm^2/g.
Al density 2.699 g/cm^3 is an illustrative bulk density.
"""
import math

AL_MASS_ATTENUATION_CM2_G = 0.2778
AL_DENSITY_G_CM3 = 2.699
AL_LINEAR_ATTENUATION_CM_INV = AL_MASS_ATTENUATION_CM2_G * AL_DENSITY_G_CM3


def uncollided_fraction(thickness_cm: float) -> float:
    if thickness_cm < 0 or not math.isfinite(thickness_cm):
        raise ValueError("thickness must be finite and nonnegative")
    return math.exp(-AL_LINEAR_ATTENUATION_CM_INV * thickness_cm)


def uncollided_count(initial_count: float, thickness_cm: float) -> float:
    if initial_count < 0 or not math.isfinite(initial_count):
        raise ValueError("initial count must be finite and nonnegative")
    return initial_count * uncollided_fraction(thickness_cm)


if __name__ == "__main__":
    print("thickness_cm,uncollided_fraction")
    for x in (0, 1, 2, 3, 5, 7, 10):
        print(f"{x},{uncollided_fraction(x):.9f}")
