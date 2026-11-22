"""Deterministic theoretical calculations for v4.32–v4.41."""
import json

import numpy as np

from .controls import (bosonic_operator, correlated_trials, decision_gates,
                       dimension_witness, factorial, ordinary_dilation, route_swap, spectral_refit)

I = np.eye(2, dtype=complex)
Z = np.diag([1, -1])
SWAP = np.eye(4)[:, [0, 2, 1, 3]]
ZERO = np.diag([1, 0])
ONE = I - ZERO


def trace_distance(left, right):
    return float(np.linalg.norm(left - right, ord="nuc") / 2)


def trace_environment(state):
    return np.einsum("iaka->ik", state.reshape(2, 2, 2, 2))


def quantum_break():
    bell = np.eye(2).ravel() / np.sqrt(2)
    entangled = np.outer(bell, bell)
    mixed_pair = np.eye(4) / 4
    leakages = [0.0, 0.1, 0.25, 0.5, 1.0]
    distance = []
    for p in leakages:
        actual = (1 - p) * mixed_pair + p * entangled
        distance.append(trace_distance(actual, mixed_pair))

    # A perfect reset on S preserves information in E. One ordinary SWAP
    # makes E observable again even though post-reset S marginals agreed.
    first = np.kron(ZERO, ZERO)
    second = np.kron(ZERO, ONE)
    local_after_reset = trace_distance(trace_environment(first), trace_environment(second))
    after_swap = trace_distance(trace_environment(SWAP @ first @ SWAP),
                                trace_environment(SWAP @ second @ SWAP))
    return {"leakage": leakages, "bell_distance": distance,
            "unassisted_optimal_distance": [p / 2 for p in leakages],
            "local_distance_after_reset": local_after_reset,
            "distance_after_ordinary_swap": after_swap}


def apply_dephasing(state):
    return (state + Z @ state @ Z) / 2


def partial_transpose_output(state):
    return state.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)


def calibration_design():
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]])
    projectors = [ZERO, ONE, (I + X) / 2, (I + Y) / 2]
    design = np.array([[np.trace(state @ op).real for op in (I, X, Y, Z)]
                       for state in projectors])
    distances = [trace_distance(state, apply_dephasing(state)) for state in projectors]
    bell = np.eye(2).ravel() / np.sqrt(2)
    identity_choi = np.outer(bell, bell)
    phase_on_output = np.kron(I, Z)
    dephasing_choi = (identity_choi + phase_on_output @ identity_choi @ phase_on_output) / 2
    # Normalized Choi matrices have input marginal I/2.
    traces = [float(np.max(abs(trace_environment(state) - I / 2)))
              for state in (identity_choi, dephasing_choi)]
    return {"z_only_design_rank": int(np.linalg.matrix_rank(design[:2])),
            "four_state_design_rank": int(np.linalg.matrix_rank(design)),
            "distance_by_calibration_input": distances,
            "bell_distance": trace_distance(identity_choi, dephasing_choi),
            "minimum_choi_eigenvalues": [float(np.linalg.eigvalsh(c)[0])
                                         for c in (identity_choi, dephasing_choi)],
            "minimum_choi_ppt_eigenvalues": [
                float(np.linalg.eigvalsh(partial_transpose_output(c))[0])
                for c in (identity_choi, dephasing_choi)],
            "choi_trace_errors": traces}


def run():
    return {"evidence_scope": "finite-dimensional standard quantum theory, no optical data",
            "v4.32": quantum_break(), "v4.33": calibration_design(),
            "v4.34": factorial(), "v4.35": route_swap(), "v4.36": dimension_witness(),
            "v4.37": correlated_trials(), "v4.38": spectral_refit(),
            "v4.39": bosonic_operator(), "v4.40": ordinary_dilation(), "v4.41": decision_gates()}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, allow_nan=False))
