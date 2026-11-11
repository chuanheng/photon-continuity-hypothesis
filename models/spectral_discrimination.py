"""Illustrative binned-count identifiability study; NOT a radiation-transport prediction.

A synthetic standard baseline and an arbitrary extra component are compared
with Poisson likelihood. All numbers are invented demonstration inputs.
No real XCOM cross-sections, detector response or material S(q,w) are used.
"""
import math

# Synthetic energy bins, keV, for a fictional detector
ENERGY_BINS_KEV = (10, 20, 30, 40, 50, 60)
# Hypothetical standard counts: arbitrary, not computed from XCOM
BASELINE = (80.0, 110.0, 170.0, 300.0, 550.0, 2400.0)
# Normalized hypothetical extra component: arbitrary shape
TEMPLATE = (0.28, 0.32, 0.24, 0.11, 0.04, 0.01)


def validate(baseline=BASELINE, template=TEMPLATE):
    if len(baseline) != len(template) or not baseline:
        raise ValueError("baseline and template need equal nonzero length")
    if any(not math.isfinite(v) or v <= 0 for v in baseline):
        raise ValueError("baseline counts must be positive and finite")
    if any(not math.isfinite(v) or v < 0 for v in template):
        raise ValueError("template entries must be nonnegative and finite")
    if not math.isclose(sum(template), 1, abs_tol=1e-10):
        raise ValueError("template must sum to 1")


def expected_counts(amplitude, baseline=BASELINE, template=TEMPLATE):
    validate(baseline, template)
    if not math.isfinite(amplitude) or amplitude < 0:
        raise ValueError("extra amplitude must be finite and nonnegative")
    return tuple(b + amplitude * t for b, t in zip(baseline, template))


def asimov_discovery_q(amplitude, baseline=BASELINE, template=TEMPLATE):
    """2*log(L(signal+baseline)/L(baseline)) on signal Asimov data.

    Assumes exact known baseline, independent Poisson bins, fixed template.
    NOT a calibrated discovery p-value or experimental significance.
    """
    observations = expected_counts(amplitude, baseline, template)
    return 2 * sum(
        n * math.log(n / b) - (n - b)
        for n, b in zip(observations, baseline)
    )


def fisher_information(baseline=BASELINE, template=TEMPLATE):
    """Local information for nonnegative amplitude at zero, fixed baseline."""
    validate(baseline, template)
    return sum(t*t / b for b, t in zip(baseline, template))


def nuisance_degeneracy(baseline=BASELINE, template=TEMPLATE):
    """Cosine similarity of extra template to free baseline normalization.

    1 means an unconstrained baseline normalization can absorb the signal
    in a local linearized Poisson model; 0 means orthogonal.
    """
    validate(baseline, template)
    tt = sum(t*t / b for b, t in zip(baseline, template))
    tb = sum(template)
    bb = sum(baseline)
    return tb / math.sqrt(tt * bb)


def profiled_information_free_normalization(baseline=BASELINE, template=TEMPLATE):
    """Schur complement after profiling a completely free background scale."""
    validate(baseline, template)
    return max(0.0, fisher_information(baseline, template) -
               sum(template)**2 / sum(baseline))


def main():
    print("SYNTHETIC COUNTS ONLY; no real experiment or validated transport.")
    print("energy_keV,baseline,template_fraction,expected_with_100_extra")
    with_signal = expected_counts(100)
    for e, b, t, n in zip(ENERGY_BINS_KEV, BASELINE, TEMPLATE, with_signal):
        print(f"{e},{b:.1f},{t:.3f},{n:.1f}")
    print(f"Asimov q(A=100; fixed background)={asimov_discovery_q(100):.4f}")
    print(f"Fisher information, fixed background={fisher_information():.8f}")
    print(f"Fisher information, free background scale={profiled_information_free_normalization():.8f}")
    print(f"Template-background normalization cosine={nuisance_degeneracy():.6f}")


if __name__ == "__main__":
    main()
