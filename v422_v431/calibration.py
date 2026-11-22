"""Synthetic reference calibration and finite-sample tests for v4.25, 27–29, 31."""
import numpy as np
from scipy.special import rel_entr, xlogy
from scipy.stats import beta, binom

REFERENCE_ALPHA = 0.025
TEST_ALPHA = 0.025
DRIFT = 0.006
NOMINAL = np.array([0.20, 0.80, 0.08, 0.30])
EDGE = np.array([0.22, 0.75, 0.10, 0.40])
REFERENCE_SIZES = np.array([6000, 6000, 6000, 6000])
SEEDS = {"calibration": 422425, "operating": 422428, "design": 422429,
         "design_validation": 431429, "blind": 422431}


def memory_amplitude(reference):
    contrast, reset, crosstalk, memory = np.moveaxis(np.asarray(reference), -1, 0)
    return contrast * ((1 - reset) * memory + crosstalk)


def probabilities(amplitude, offset):
    return np.stack((0.5 + 0.5 * amplitude + offset, 0.5 + amplitude + offset), axis=-1)


def reference_box(rates, sizes):
    radius = np.sqrt(np.log(8 / REFERENCE_ALPHA) / (2 * sizes))
    return np.clip(rates - radius, 0, 1), np.clip(rates + radius, 0, 1)


def amplitude_bounds(low, high):
    # Reset has negative sign; the other derivatives are nonnegative. The
    # upper cap retains a valid nested-word family for every allowed offset.
    lower = low.copy()
    upper = high.copy()
    lower[..., 1] = high[..., 1]
    upper[..., 1] = low[..., 1]
    return memory_amplitude(lower), np.minimum(memory_amplitude(upper), 0.5 - DRIFT)


def cp_interval(successes, trials, alpha=0.05):
    lower = beta.ppf(alpha / 2, successes, trials - successes + 1) if successes else 0.0
    upper = beta.ppf(1 - alpha / 2, successes + 1, trials - successes) if successes < trials else 1.0
    return [float(lower), float(upper)]


def describe(flags):
    count = int(np.sum(flags))
    total = len(flags)
    return {"count": count, "trials": total, "rate": count / total,
            "mc_95_interval": cp_interval(count, total)}


def calibration_audit():
    rng = np.random.default_rng(SEEDS["calibration"])
    rates = rng.binomial(REFERENCE_SIZES, NOMINAL, (4000, 4)) / REFERENCE_SIZES
    low, high = reference_box(rates, REFERENCE_SIZES)
    covered = np.all((low <= NOMINAL) & (NOMINAL <= high), axis=1)
    _, maximum = amplitude_bounds(low, high)
    nominal = memory_amplitude(NOMINAL)
    # This shared drift is an out-of-domain stress case. The hidden carrier
    # contributes additional amplitude invisible to all four reference channels.
    stressed = {
        "in_budget_shared_drift": nominal + 0.004,
        "out_of_budget_shared_drift": nominal + 0.028,
        "unmonitored_carrier": nominal + 0.055,
    }
    return {"joint_reference_coverage": describe(covered),
            "nominal_amplitude": float(nominal),
            "reference_radius": float(np.sqrt(np.log(8 / REFERENCE_ALPHA) / (2 * REFERENCE_SIZES[0]))),
            "main_upper_envelope_coverage": {
                name: describe(value <= maximum + DRIFT) for name, value in stressed.items()}}


def distance_certificate():
    # Ideal intervals; the distinct sampling problem is handled by reference_box.
    low = np.array([0.18, 0.75, 0.06, 0.20])
    high = np.array([0.22, 0.85, 0.10, 0.40])
    a_low, a_high = amplitude_bounds(low, high)
    candidate = probabilities(0.08, 0.0)
    upper = probabilities(a_high, DRIFT)
    per_protocol = rel_entr(candidate, upper) + rel_entr(1 - candidate, 1 - upper)
    # Both candidate marginals are above their respective maxima and both
    # maxima are attained at the same corner. Hence equality for this objective.
    unconstrained_fit = np.array([0.20, 0.80, 0.34, 0.30])
    matched = probabilities(memory_amplitude(unconstrained_fit), 0.0)
    return {"amplitude_range": [float(a_low), float(a_high)],
            "candidate": candidate.tolist(), "null_ceiling": upper.tolist(),
            "kl_each": per_protocol.tolist(), "exact_equal_weight_kl": float(per_protocol.mean()),
            "unrestricted_crosstalk_refit": unconstrained_fit.tolist(),
            "refit_max_error": float(np.max(abs(matched - candidate)))}


def sample_words(rng, n, p, repeats):
    # A=111 and B=11 overlap: A is a subset of B on the same trial.
    categories = np.array([p[0], p[1] - p[0], 1 - p[1]])
    counts = rng.multinomial(int(n), categories, size=repeats)
    return counts


def fit_training(counts, a_low, a_high):
    """Fit multinomial nested word likelihood on the amplitude/offset box."""
    observed = counts / counts.sum(axis=1, keepdims=True)
    amplitude = 2 * observed[:, 1]
    offset = observed[:, 0] - 0.5 - 0.5 * amplitude
    feasible = (a_low <= amplitude) & (amplitude <= a_high) & (abs(offset) <= DRIFT)
    results = [(np.where(feasible, 0.0, -np.inf), observed[:, 0], observed[:, :2].sum(axis=1))]
    for fixed_amplitude, bounds in (
        (True, ((a_low, -DRIFT, DRIFT), (a_high, -DRIFT, DRIFT))),
        (False, ((-DRIFT, a_low, a_high), (DRIFT, a_low, a_high))),
    ):
        direction = np.array([1.0, 0.0, -1.0]) if fixed_amplitude else np.array([0.5, 0.5, -1.0])
        for fixed, low, high in bounds:
            left, right = np.broadcast_to(low, a_low.shape).copy(), np.broadcast_to(high, a_low.shape).copy()

            def category(x):
                a, o = (fixed, x) if fixed_amplitude else (x, fixed)
                p_a, p_b = probabilities(a, o).T
                return np.stack((p_a, p_b - p_a, 1 - p_b), axis=1)

            for _ in range(32):
                middle = (left + right) / 2
                derivative = np.sum(counts * direction / np.maximum(category(middle), 1e-100), axis=1)
                left, right = np.where(derivative > 0, middle, left), np.where(derivative > 0, right, middle)
            fitted = category((left + right) / 2)
            score = xlogy(counts, fitted).sum(axis=1) - xlogy(counts, observed).sum(axis=1)
            results.append((score, fitted[:, 0], fitted[:, :2].sum(axis=1)))
    scores, pa, pb = np.array(results).transpose(1, 0, 2)
    idx = np.argmax(scores, axis=0)
    row = np.arange(len(counts))
    return np.stack((pa[idx, row], pb[idx, row]), axis=1)


def generate_records(rng, reference, main_prob, sizes, repeats):
    calibration, training, heldout = sizes[:4], int(sizes[4]), int(sizes[5])
    rates = rng.binomial(calibration, reference, (repeats, 4)) / calibration
    return (rates, sample_words(rng, training, main_prob, repeats),
            sample_words(rng, heldout, main_prob, repeats))


def analyze_records(records, sizes):
    rates, training_counts, observed_categories = records
    calibration, training, heldout = sizes[:4], int(sizes[4]), int(sizes[5])
    amin, amax = amplitude_bounds(*reference_box(rates, calibration))
    feasible = amin <= amax
    fit = fit_training(training_counts, np.minimum(amin, amax), amax)
    empirical = (training_counts @ np.array([[1, 1], [0, 1], [0, 0]])) / training
    ceiling = np.clip(probabilities(amax, DRIFT), 0, 1)
    residual = (empirical - fit) / np.sqrt(np.maximum(fit * (1 - fit), 1e-15))
    choice = np.argmax(residual, axis=1)
    observed = observed_categories @ np.array([[1, 1], [0, 1], [0, 0]])
    idx = np.arange(len(rates))
    upper = ceiling[idx, choice]
    p_value = binom.sf(observed[idx, choice] - 1, heldout, upper)
    return {"certified_reject": feasible & (p_value <= TEST_ALPHA),
            "naive_reject": binom.sf(observed[idx, choice] - 1, heldout, fit[idx, choice]) <= 0.05,
            "chosen_b": choice == 1}



def execute_protocol(rng, reference, main_prob, sizes, repeats):
    return analyze_records(generate_records(rng, reference, main_prob, sizes, repeats), sizes)


def operating_characteristics():
    rng = np.random.default_rng(SEEDS["operating"])
    sizes = np.r_[REFERENCE_SIZES, 4000, 6000]
    datasets = {
        "ordinary_interior": (NOMINAL, probabilities(memory_amplitude(NOMINAL), 0.0)),
        "ordinary_positive_drift_edge": (EDGE, probabilities(memory_amplitude(EDGE), DRIFT)),
        "ordinary_negative_drift_edge": (EDGE, probabilities(memory_amplitude(EDGE), -DRIFT)),
        "exact_refit_in_reference_domain": (EDGE, probabilities(0.044, 0.0)),
        "separated_positive_control": (EDGE, probabilities(0.09, 0.0)),
    }
    return {name: {key: describe(value) for key, value in
                   execute_protocol(rng, reference, p, sizes, 4000).items()}
            for name, (reference, p) in datasets.items()}


def optimize_allocation():
    rng = np.random.default_rng(SEEDS["design"])
    budget = 36000
    uniform = np.full(6, budget // 6, dtype=int)
    pool = (2400 + np.floor(rng.dirichlet(np.full(6, 2.5), size=3200)
                            * (budget - 6 * 2400))).astype(int)
    pool[:, -1] += budget - pool.sum(axis=1)
    pool = np.vstack((uniform, pool))

    def utility(sizes):
        # Planning-only expected precision, with two plausible pilot reference points.
        # Require both protocols to retain separation, with a training noise penalty.
        utilities = []
        for ref in (NOMINAL, EDGE):
            _, amp = amplitude_bounds(*reference_box(ref, sizes[:, :4]))
            ceiling = probabilities(amp, DRIFT)
            target = probabilities(0.083, 0)
            z_gap = (target - ceiling) / np.sqrt(ceiling * (1 - ceiling))
            utilities.append(np.min(z_gap, axis=1)
                             / np.sqrt(1 / sizes[:, 4] + 1 / sizes[:, 5]))
        return np.min(utilities, axis=0)

    score = utility(pool)
    winner = int(np.argmax(score))
    validation = np.random.default_rng(SEEDS["design_validation"])
    outcomes = {}
    for name, allocation in (("uniform", uniform), ("optimized", pool[winner])):
        for label, ref, drift in (("nominal", NOMINAL, 0.0), ("perturbed", EDGE, -0.004)):
            result = execute_protocol(validation, ref, probabilities(0.083, drift), allocation, 4000)
            outcomes[name + "_" + label] = describe(result["certified_reject"])
    return {"budget": budget, "uniform": uniform.tolist(), "optimized": pool[winner].tolist(),
            "design_points": len(pool), "uniform_proxy": float(score[0]),
            "optimized_proxy": float(score[winner]), "validation": outcomes}


def blind_challenge():
    rng = np.random.default_rng(SEEDS["blind"])
    sizes = np.array([6000, 6000, 6000, 6000, 6000, 6000])
    truth = [
        ("ordinary_calibrated", EDGE, probabilities(memory_amplitude(EDGE), DRIFT)),
        ("synthetic_separation", EDGE, probabilities(0.115, 0)),
        ("weak_separation", EDGE, probabilities(0.060, 0)),
        ("unmonitored_ordinary_drift", NOMINAL, probabilities(memory_amplitude(NOMINAL), 0.048)),
    ]
    # The analysis receives only samples and reference rates. Assign names
    # after the shared decision rule has returned on every shuffled input.
    order = rng.permutation(len(truth))
    samples = [generate_records(rng, truth[j][1], truth[j][2], sizes, 4000)
               for j in order]
    blinded = [analyze_records(sample, sizes) for sample in samples]
    return {"rule": "one-sided exact tail at 0.025 after 97.5% joint reference box",
            "unblinded_results": {truth[j][0]: describe(result["certified_reject"])
                                   for j, result in zip(order, blinded)}}
