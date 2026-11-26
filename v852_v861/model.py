"""Independent-calibration requirements for the published four-cell contrast."""
import json
from statistics import NormalDist

import numpy as np

from v702_v711.model import run as published


SIGNS = np.array([1.0, -1.0, -1.0, 1.0])


def run():
    old = published()
    contrast = old["v7.02"]["log_ratio"]
    science_sd = old["v7.06"]["independent_log_sd"]
    z95 = NormalDist().inv_cdf(0.975)

    common = np.ones(4)
    detector = np.array([1.0, -1.0, 1.0, -1.0])
    line = np.array([1.0, 1.0, -1.0, -1.0])
    modes = np.column_stack((common, detector, line, SIGNS))
    interaction_bias = contrast * SIGNS / (SIGNS @ SIGNS)

    per_cell_sd_limit = abs(contrast) / (2 * z95)
    counts_per_cell = int(np.floor((2 * z95 / abs(contrast)) ** 2) + 1)
    combined_sd = float(np.hypot(science_sd, 2 * per_cell_sd_limit))
    combined_z = abs(contrast) / combined_sd

    # Candidate kappa and ordinary response interaction h enter with the same column.
    candidate_ordinary_design = np.column_stack((SIGNS, SIGNS))

    calibration_sd = 0.05
    difference_sd = float(np.hypot(science_sd, calibration_sd))
    target_half_width = z95 * difference_sd

    return {
        "v8.52": {
            "log_cross_ratio": contrast,
            "cross_ratio": float(np.exp(contrast)),
            "contrast_vector": SIGNS.tolist(),
        },
        "v8.53": {
            "min_linf_log_bias": abs(contrast) / 4,
            "symmetric_cell_multipliers": np.exp(interaction_bias).tolist(),
        },
        "v8.54": {
            "min_l2_log_bias": abs(contrast) / 2,
            "min_l1_log_bias": abs(contrast),
            "l2_solution": interaction_bias.tolist(),
        },
        "v8.55": {
            "mode_gram": (modes.T @ modes).tolist(),
            "contrast_on_common_detector_line": (SIGNS @ modes[:, :3]).tolist(),
        },
        "v8.56": {
            "interaction_projection": float(SIGNS @ interaction_bias),
            "ordinary_exact_refit": (-interaction_bias).tolist(),
            "post_refit_contrast": float(contrast + SIGNS @ (-interaction_bias)),
        },
        "v8.57": {
            "per_cell_independent_log_sd_limit_95pct": per_cell_sd_limit,
            "contrast_sd_at_limit": 2 * per_cell_sd_limit,
        },
        "v8.58": {
            "poisson_counts_per_cell_95pct": counts_per_cell,
            "poisson_contrast_sd": float(2 / np.sqrt(counts_per_cell)),
        },
        "v8.59": {
            "science_log_sd_proxy": science_sd,
            "combined_log_sd_at_calibration_limit": combined_sd,
            "observed_z_proxy": combined_z,
        },
        "v8.60": {
            "candidate_ordinary_rank": int(np.linalg.matrix_rank(candidate_ordinary_design)),
            "candidate_column_equals_ordinary": bool(np.array_equal(
                candidate_ordinary_design[:, 0], candidate_ordinary_design[:, 1]
            )),
        },
        "v8.61": {
            "independent_reference_log_sd": calibration_sd,
            "science_minus_reference_sd": difference_sd,
            "two_sided_95pct_half_width": target_half_width,
            "falsification_requires_abs_difference_gt": target_half_width,
        },
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
