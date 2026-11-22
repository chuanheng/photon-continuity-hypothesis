"""Ordinary mechanisms and finite observation limits, v4.34–v4.41."""
from itertools import product

import numpy as np
from scipy.optimize import linprog
from scipy.stats import binom

X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.diag([1, -1])
I = np.eye(2)


def factorial():
    # Rows toggle material reset; columns toggle detector reset.
    def interaction(table):
        return float(table[0, 0] - table[0, 1] - table[1, 0] + table[1, 1])

    m = np.array([1.0, 0.2])
    d = np.array([1.0, 0.1])
    ordinary = 0.3 + 0.08 * m[:, None] + 0.06 * d + 0.1 * m[:, None] * d
    # Unmodelled timing offsets can correlate with both intervention bits.
    additive = np.array([[0.0, 0.02], [0.03, 0.05]])
    aliased = 0.02 * np.array([[1, -1], [-1, 1]])
    return {"table": ordinary.tolist(), "ordinary_interaction": interaction(ordinary),
            "with_additive_drift": interaction(ordinary + additive),
            "with_aliased_drift": interaction(ordinary + aliased),
            "drift_bias_bound": 4 * 0.02}


def route_swap():
    write = np.diag(np.sqrt([0.81, 0.25]))
    read = np.diag(np.sqrt([0.64, 0.36]))
    swap = X
    ordinary = [read @ s @ write for s in (I, swap)]
    changes = [(np.linalg.norm(channel, axis=0)**2).tolist() for channel in ordinary]
    # A consistent permutation of the internal storage basis is unobservable.
    refitted = [(read @ swap) @ (swap @ s @ swap) @ (swap @ write) for s in (I, swap)]
    return {"read_probabilities": changes,
            "basis_relabel_error": max(float(np.max(abs(a-b))) for a, b in zip(ordinary, refitted))}


def dimension_witness():
    states = [(I + z * op) / 2 for op in (X, Y, Z) for z in (1, -1)]
    effects = [(I + z * op) / 2 for op in (X, Y, Z) for z in (1, -1)]
    table = np.array([[np.trace(effect @ state).real for effect in effects] for state in states])
    minor = table[np.ix_([0, 1, 2, 4], [0, 1, 2, 4])]
    return {"full_rank": int(np.linalg.matrix_rank(table)),
            "z_only_rank": int(np.linalg.matrix_rank(table[4:, 4:])),
            "rank_four_minor": float(np.linalg.det(minor)),
            "table": table.tolist()}


def correlated_trials():
    p = 0.5
    blocks = 50
    length = 20
    alpha = 0.05
    n = blocks * length
    iid_threshold = int(binom.isf(alpha, n, p)) + 1
    wrong_size = float(binom.sf((iid_threshold - 1) // length, blocks, p))
    # Independent block means in [0,1] permit arbitrary within-block dependence.
    cutoff = p + np.sqrt(np.log(1 / alpha) / (2 * blocks))
    return {"blocks": blocks, "block_length": length, "iid_threshold": iid_threshold,
            "actual_size_using_iid": wrong_size, "block_mean_threshold": float(cutoff),
            "block_bound_actual_size": float(binom.sf(np.floor(blocks * cutoff), blocks, p))}


def spectral_refit():
    # Two broadened lines and independently bounded background. Entries are
    # normalized bin responses conditional on detection, not atomic data.
    line = np.array([[0.65, 0.15, 0.10], [0.25, 0.25, 0.80], [0.10, 0.60, 0.10]])
    weights = [(0.0, 1.0), (0.0, 1.0), (0.0, 0.05)]
    target = np.array([0.35, 0.35, 0.30])
    # Sum of the bin probabilities is identically one in this conditional model.
    def fit(response, values, bounds):
        return linprog(np.zeros(3), A_eq=np.vstack((np.ones(3), response)),
                       b_eq=np.r_[1.0, values], bounds=bounds, method="highs")

    total = fit(line.sum(axis=0, keepdims=True), [1.0], weights)
    spectrum = fit(line, target, weights)
    free_background = fit(line, target, [(0.0, 1.0)] * 3)
    maximum = linprog(-line[1], A_eq=[np.ones(3)], b_eq=[1.0], bounds=weights, method="highs")
    if not all(result.success for result in (total, free_background, maximum)):
        raise RuntimeError("ordinary reference optimization failed")
    return {"total_feasible": total.success, "spectrum_feasible": spectrum.success,
            "spectrum_solver_status": spectrum.status, "calibrated_middle_ceiling": -float(maximum.fun),
            "target_middle": target[1], "free_background_weights": free_background.x.tolist(),
            "free_background_residual": float(np.max(abs(line @ free_background.x - target)))}


def bosonic_operator():
    swap = np.eye(4)[:, [0, 2, 1, 3]]
    basis = np.array([[1, 0, 0], [0, 1/np.sqrt(2), 0],
                      [0, 1/np.sqrt(2), 0], [0, 0, 1]])
    first, second = np.kron(Z, I), np.kron(I, Z)
    difference = basis.T @ (first-second) @ basis
    number = basis.T @ (first+second) @ basis
    return {"symmetric_dimension": int(np.linalg.matrix_rank((np.eye(4)+swap)/2)),
            "slot_difference_norm": float(np.linalg.norm(difference)),
            "collective_eigenvalues": np.linalg.eigvalsh(number).tolist(),
            "unsymmetrized_commutator_norm": float(np.linalg.norm(first @ swap - swap @ first))}


def ordinary_dilation():
    # A persistent ordinary phase bit is given a coherent state in one
    # realization and a dephased initial state in the other.
    controls = [I, X, np.array([[1, 1], [1, -1]])/np.sqrt(2)]
    U = np.kron(I, np.diag([1, 0])) + np.kron(Z, np.diag([0, 1]))
    state = (I+X)/2
    pure_hidden = (I+X)/2
    classical_hidden = I/2

    def read(hidden, sequence):
        rho = np.kron(state, hidden)
        for control in sequence:
            step = U @ np.kron(control, I)
            rho = step @ rho @ step.conj().T
        return np.einsum("iaka->ik", rho.reshape(2, 2, 2, 2))

    errors = [np.max(abs(read(pure_hidden, steps)-read(classical_hidden, steps)))
              for n in range(5) for steps in product(controls, repeat=n)]
    # If the environment becomes addressable, measuring its X directly distinguishes them.
    return {"trajectories_checked": len(errors), "max_reduced_difference": float(max(errors)),
            "addressable_environment_x_difference": float(np.trace(X @ (pure_hidden-classical_hidden)))}


def decision_gates():
    # Illustrative one-sided 5% planning thresholds with independent blocks.
    ordinary_ceiling = 0.04
    blocks = 1000
    radius = float(np.sqrt(np.log(20)/(2*blocks)))
    inputs = [(True, 0.07), (True, 0.09), (False, 0.15)]
    decisions = ["calibration_inconclusive" if not calibration else
                 "reject_scoped_family" if estimate-radius > ordinary_ceiling else
                 "insufficient_separation" for calibration, estimate in inputs]
    return {"ordinary_ceiling": ordinary_ceiling, "one_sided_radius": radius,
            "synthetic_inputs": inputs, "decisions": decisions,
            "identity_mechanism_confirmed": False}
