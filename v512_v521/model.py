"""Synthetic joint calibration and candidate-separation examples."""
import json

import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm

SEED = 512521


def shared_leakage():
    direction = np.array([1., 1j, -1.])
    candidate = .09*np.array([1j, 1., -1j])
    observed = .07*direction + candidate
    projected = np.vdot(direction, observed)/np.vdot(direction, direction)
    fit = projected*direction
    return dict(shared_residual=float(np.linalg.norm(observed-fit)),
                per_setting_max_amplitude=float(np.max(abs(observed))),
                per_setting_bound=.2,
                per_setting_refit_error=float(np.max(abs(observed-observed/direction*direction))),
                projected_residual_dot=float(abs(np.vdot(direction, observed-fit))))


def calibration_ellipse():
    angle = .65
    rotation = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    radii = np.array([.12, .03])
    shape = rotation @ np.diag(radii**2) @ rotation.T
    witness = rotation[:, 1]
    support = np.sqrt(witness @ shape @ witness)
    boundary = shape @ witness/support
    observed = boundary+.04*witness
    phases = 2*np.pi*np.arange(1000)/1000
    perimeter = rotation @ (radii[:, None]*np.array([np.cos(phases), np.sin(phases)]))
    return dict(support=float(support), global_distance=float(witness@observed-support),
                attainable_residual=float(np.linalg.norm(observed-boundary)),
                circular_outer_radius=float(radii.max()), observed_norm=float(np.linalg.norm(observed)),
                sampled_support=float(np.max(witness@perimeter)))


def reference_slope():
    settings = np.linspace(-2, 2, 101)
    beta = .21
    observed = np.exp(1j*beta*settings)
    ordinary_reference = np.exp(1j*beta*settings)
    bound = .03
    # Each accessible endpoint phase difference lies between zero and pi.
    guaranteed_endpoint_gap = 2*np.sin((beta-bound)*settings[-1]/2)
    return dict(offset_only_endpoint_gap=float(abs(observed[-1]-1)),
                free_reference_refit_error=float(np.max(abs(observed-ordinary_reference))),
                independently_allowed_slope=bound, calibrated_endpoint_gap=float(guaranteed_endpoint_gap))


def nuisance_contrast():
    basis = np.array([[1., -1.], [1., 0.], [1., 1.]])
    contrast = np.array([1., -2., 1.])
    candidate = np.array([1., 0., 1.])
    linear_background = basis @ np.array([.5, .2])
    observed = linear_background+.08*candidate
    ordinary_curvature = np.array([1., 0., 1.])
    matched = linear_background+.08*ordinary_curvature
    return dict(null_response=float(contrast@linear_background), signal_response=float(contrast@observed),
                normalized_noise_gain=float(np.linalg.norm(contrast)),
                curvature_refit_error=float(np.max(abs(observed-matched))))


def selection_error():
    settings = 20
    nominal = .05
    cutoff = norm.ppf(1-nominal)
    adjusted = norm.ppf((1-nominal)**(1/settings))
    return dict(settings=settings, nominal=nominal, single_cutoff=float(cutoff),
                uncorrected_family_error=float(1-norm.cdf(cutoff)**settings),
                independent_adjusted_cutoff=float(adjusted),
                corrected_family_error=float(1-norm.cdf(adjusted)**settings),
                bonferroni_cutoff=float(norm.ppf(1-nominal/settings)))


def reference_blocks():
    rng = np.random.default_rng(SEED)
    replications, blocks, repeats = 3000, 24, 16
    common_sd, residual_sd = .4, .2
    shared = rng.normal(0, common_sd, (replications, blocks, 1))
    independent = rng.normal(0, residual_sd, (replications, blocks, repeats))
    first, second = shared+independent, shared+rng.normal(0, residual_sd, independent.shape)
    means = first.mean(axis=(1, 2))
    naive_se = np.sqrt((common_sd**2+residual_sd**2)/(blocks*repeats))
    exact_se = np.sqrt((common_sd**2+residual_sd**2/repeats)/blocks)
    paired = (first-second).mean(axis=(1, 2))
    paired_se = np.sqrt(2*residual_sd**2/(blocks*repeats))
    cutoff = norm.ppf(.975)
    return dict(seed=SEED, replications=replications, blocks=blocks, repeats_per_block=repeats,
                correct_se=float(exact_se), naive_se=float(naive_se), paired_se=float(paired_se),
                naive_coverage=float(np.mean(abs(means)<=cutoff*naive_se)),
                valid_coverage=float(np.mean(abs(means)<=cutoff*exact_se)),
                paired_coverage=float(np.mean(abs(paired)<=cutoff*paired_se)))


def signed_power():
    alpha, sigma, effect = .05, .3, .05
    critical = norm.ppf(1-alpha/2)
    def power(count, signed_effect):
        standardized_mean = signed_effect*np.sqrt(count)/sigma
        return norm.sf(critical-standardized_mean)+norm.cdf(-critical-standardized_mean)
    count = int(np.ceil(brentq(lambda n: power(n, effect)-.9, 1, 10000)))
    return dict(noise_sd=sigma, target_magnitude=effect, required_count=count,
                positive_power=float(power(count, effect)), negative_power=float(power(count, -effect)),
                previous_count_power=float(power(count-1, effect)), size=float(power(count, 0)))


def candidate_intersection():
    null_radius, difference_radius = .10, .07
    shifts = np.array([.13, .21])
    # Distance between compact disks of freely fitted nuisance amplitudes.
    gaps = np.maximum(0., shifts-null_radius-difference_radius)
    midpoint = shifts[0]*null_radius/(null_radius+difference_radius)
    return dict(null_radius=null_radius, alternative_radius=difference_radius, shifts=shifts.tolist(),
                global_gaps=gaps.tolist(), overlap_point=float(midpoint),
                distance_to_alternative_center=float(abs(shifts[0]-midpoint)))


def calibration_priority():
    projections = np.array([.9, .2, .5])
    errors = np.array([.08, .1, .07])
    cost = np.array([5., 1., 2.])
    signal = .15
    budget = 5.
    reduction = projections*errors/2
    # One calibration intervention may be chosen in this design.
    baseline = signal-projections@errors
    margins = baseline+reduction
    order = np.argsort(-margins)
    choice = next(int(i) for i in order if cost[i] <= budget)
    return dict(signal=signal, budget=budget, baseline_margin=float(baseline),
                intervention_cost=cost.tolist(), margins=margins.tolist(), chosen_index=choice,
                chosen_margin=float(margins[choice]))


def injection_recovery():
    rng = np.random.default_rng(SEED+1)
    count = 4000
    noise_sd, gain, injected = .02, .7, .15
    cutoff = .04+norm.ppf(.99)*noise_sd
    labels = rng.permutation(np.repeat([False, True], count//2))
    ordinary = rng.uniform(-.04, .04, count)
    noise = rng.normal(0, noise_sd, count)
    signal = ordinary+gain*injected*labels+noise
    sham = signal>cutoff
    bypassed = ordinary+injected*labels+noise > cutoff
    return dict(seed=SEED+1, trials=count, injected_amplitude=injected, chain_gain=gain, threshold=float(cutoff),
                sham_false_positive=float(np.mean(sham[~labels])),
                full_chain_recovery=float(np.mean(sham[labels])),
                downstream_recovery=float(np.mean(bypassed[labels])))


def run():
    return {
        "v5.12": shared_leakage(),
        "v5.13": calibration_ellipse(),
        "v5.14": reference_slope(),
        "v5.15": nuisance_contrast(),
        "v5.16": selection_error(),
        "v5.17": reference_blocks(),
        "v5.18": signed_power(),
        "v5.19": candidate_intersection(),
        "v5.20": calibration_priority(),
        "v5.21": injection_recovery(),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, allow_nan=False))
