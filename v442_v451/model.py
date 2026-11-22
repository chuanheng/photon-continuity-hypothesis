"""Noncommuting environment operations and calibrated refitting."""
import json

import numpy as np
from scipy.optimize import linprog

I = np.eye(2)
X = np.array([[0, 1], [1, 0]])
Z = np.diag([1, -1])
PLUS = (I + X) / 2
CZ = np.diag([1, 1, 1, -1])


def response(theta, environment):
    c, s = np.cos(theta / 2), np.sin(theta / 2)
    rotation = np.array([[c, -s], [s, c]])
    initial = np.kron(PLUS, rotation @ environment @ rotation.T)
    output = CZ @ initial @ CZ
    return float(np.trace(np.kron(X, I) @ output))


def witness():
    angles = np.arange(5) * np.pi / 4
    differences = np.array([response(t, PLUS) - response(t, I / 2) for t in angles])
    return {"angles": angles.tolist(), "differences": differences.tolist(),
            "max_formula_error": float(np.max(abs(differences + np.sin(angles)))),
            "x_readout_total_variation_pi_over_2": float(abs(differences[2]) / 2)}


def constrained_refit():
    # Gain is measured and fixed in this example. Independent X tomography
    # bounds the magnitude of the device qubit's ordinary coherence.
    gain = 0.8
    target = np.array([0.0, -0.4])
    predictor = gain * np.array([[0, 1], [-1, 0]])
    A = np.vstack((np.column_stack((predictor, -np.ones(2))),
                   np.column_stack((-predictor, -np.ones(2)))))
    b = np.r_[target, -target]

    def fit(x_limit):
        result = linprog([0, 0, 1], A_ub=A, b_ub=b,
                         bounds=[(-x_limit, x_limit), (-1, 1), (0, None)], method="highs")
        if not result.success or np.linalg.norm(result.x[:2]) > 1 + 1e-12:
            raise RuntimeError("Expected the box relaxation to attain the physical Bloch-ball optimum")
        return result.x.tolist()

    return {"parameter_order": ["x", "z", "maximum_residual"],
            "target": target.tolist(), "calibrated_solution": fit(0.2),
            "ordinary_coherent_solution": fit(1.0)}


def run():
    return {"v4.42": witness(), "v4.43": constrained_refit()}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, allow_nan=False))
