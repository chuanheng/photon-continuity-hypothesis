"""Correlation, exchange, drift, and matched-reference design calculations."""
import json
from statistics import NormalDist

import numpy as np

from v852_v861.model import SIGNS, run as calibration


def run():
    prior = calibration()
    effect = prior["v8.52"]["log_cross_ratio"]
    science_sd = prior["v8.59"]["science_log_sd_proxy"]

    modes = np.column_stack((
        np.ones(4),
        np.array([1.0, -1.0, 1.0, -1.0]),
        np.array([1.0, 1.0, -1.0, -1.0]),
        SIGNS,
    )) / 2
    mode_sd = np.array([0.10, 0.08, 0.06, 0.04])
    covariance = modes @ np.diag(mode_sd ** 2) @ modes.T
    contrast_sd = float(np.sqrt(SIGNS @ covariance @ SIGNS))

    cell_sd = 0.05
    worst_vectors = cell_sd * SIGNS
    worst_covariance = np.outer(worst_vectors, worst_vectors)
    worst_sd = float(np.sqrt(SIGNS @ worst_covariance @ SIGNS))

    science_only = np.array([[1.0, 1.0]])
    science_reference = np.array([[1.0, 1.0], [0.0, 1.0]])

    kappa, ordinary = effect, 0.12
    stable_plus = kappa + ordinary
    stable_minus = -kappa + ordinary
    unstable_minus = -kappa - ordinary

    times = np.array([-1.5, -0.5, 0.5, 1.5])
    abba = np.array([0.5, -0.5, -0.5, 0.5])
    moments = [float(abba @ times ** power) for power in range(4)]

    science_var, reference_var, covariance_sr = 0.04, 0.01, 0.015
    paired_var = science_var + reference_var - 2 * covariance_sr

    z_alpha = NormalDist().inv_cdf(0.975)
    z_power = NormalDist().inv_cdf(0.8)
    target_sd = effect / (z_alpha + z_power)
    reference_sd = 0.05
    exposure_multiplier = science_sd ** 2 / (target_sd ** 2 - reference_sd ** 2)

    protocol = np.array([
        [1.0, 1.0, 0.0],   # science normal: kappa + ordinary
        [-1.0, 1.0, 0.0],  # science swapped: -kappa + ordinary
        [0.0, 1.0, 1.0],   # matched reference plus drift
        [0.0, 0.0, 1.0],   # blank drift monitor
    ])

    return {
        "v8.62": {
            "mode_standard_deviations": mode_sd.tolist(),
            "cell_covariance": covariance.tolist(),
            "contrast_standard_deviation": contrast_sd,
        },
        "v8.63": {
            "equal_cell_marginal_sd": cell_sd,
            "worst_case_contrast_sd": worst_sd,
            "independent_contrast_sd": 2 * cell_sd,
        },
        "v8.64": {
            "main_effect_calibration_contrast_sensitivity": (SIGNS @ modes[:, :3]).tolist(),
            "interaction_unconstrained": True,
        },
        "v8.65": {
            "science_only_rank": int(np.linalg.matrix_rank(science_only)),
            "science_plus_reference_rank": int(np.linalg.matrix_rank(science_reference)),
            "determinant": float(np.linalg.det(science_reference)),
        },
        "v8.66": {
            "stable_swap_observations": [stable_plus, stable_minus],
            "recovered_candidate": (stable_plus - stable_minus) / 2,
            "recovered_ordinary": (stable_plus + stable_minus) / 2,
        },
        "v8.67": {
            "ordinary_odd_counterexample": [stable_plus, unstable_minus],
            "apparent_candidate": (stable_plus - unstable_minus) / 2,
            "true_candidate": kappa,
        },
        "v8.68": {
            "abba_drift_moments_orders_0_to_3": moments,
            "quadratic_coefficient_to_mimic_effect": effect / moments[2],
        },
        "v8.69": {
            "independent_difference_variance": science_var + reference_var,
            "paired_difference_variance": paired_var,
            "variance_reduction_fraction": 1 - paired_var / (science_var + reference_var),
        },
        "v8.70": {
            "target_total_sd_alpha05_power80": target_sd,
            "reference_sd": reference_sd,
            "required_science_exposure_multiplier": exposure_multiplier,
        },
        "v8.71": {
            "protocol_design": protocol.tolist(),
            "protocol_rank": int(np.linalg.matrix_rank(protocol)),
            "parameters": ["candidate", "ordinary_interaction", "drift"],
            "minimum_conditions": [
                "matched energy-direction reference",
                "physical detector-role exchange",
                "interleaved blank drift monitor",
                "held-out prediction fixed before unblinding",
            ],
        },
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
