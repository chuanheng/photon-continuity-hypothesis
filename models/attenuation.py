"""Illustrative toy Monte Carlo, NOT a validated X-ray transport simulator.

Run: python3 models/attenuation.py
Outputs results.csv in the current directory.
"""
import csv
import math
import random

N = 100_000
E0_KEV = 60.0
MU_CM_INV = 0.2778 * 2.699  # NIST Al mass attenuation at 60 keV * density
LAMBDA_CM_INV = 0.75  # free, unmeasured toy parameter
ALPHA = 0.20          # free, unmeasured toy parameter
SEED = 20261111
THICKNESSES_CM = [0, 0.5, 1, 2, 3, 5, 7, 10]


def poisson(mean, rng):
    if mean == 0:
        return 0
    limit = math.exp(-mean)
    product = 1.0
    count = 0
    while product > limit:
        product *= rng.random()
        count += 1
    return count - 1


def simulate(x):
    rng = random.Random(SEED + int(x * 100))
    energies = [
        E0_KEV * (1 - ALPHA) ** poisson(LAMBDA_CM_INV * x, rng)
        for _ in range(N)
    ]
    return {
        "thickness_cm": x,
        "standard_expected_uncollided_count": N * math.exp(-MU_CM_INV * x),
        "toy_expected_mean_energy_keV": E0_KEV * math.exp(-LAMBDA_CM_INV * ALPHA * x),
        "toy_simulated_mean_energy_keV": sum(energies) / N,
        "toy_count_above_10keV": sum(e >= 10 for e in energies),
        "toy_count_above_30keV": sum(e >= 30 for e in energies),
        "toy_zero_event_expected_count": N * math.exp(-LAMBDA_CM_INV * x),
    }


def main():
    rows = [simulate(x) for x in THICKNESSES_CM]
    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    for row in rows:
        print(
            f"x={row['thickness_cm']:>4} cm | "
            f"standard uncollided={row['standard_expected_uncollided_count']:>9.1f} | "
            f"toy mean E={row['toy_simulated_mean_energy_keV']:>7.3f} keV"
        )
    print("Saved results.csv")


if __name__ == "__main__":
    main()
