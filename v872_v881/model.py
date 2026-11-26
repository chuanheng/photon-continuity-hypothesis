"""Operational tests for a putative permanent photon-identity label."""
import json

import numpy as np


SEED = 872881


def trace_distance(a, b):
    singular = np.linalg.svd(a - b, compute_uv=False)
    return float(0.5 * singular.sum())


def partial_trace_label(rho):
    return np.trace(rho.reshape(2, 2, 2, 2), axis1=1, axis2=3)


def run():
    zero = np.array([1.0, 0.0], dtype=complex)
    one = np.array([0.0, 1.0], dtype=complex)
    rho = np.outer(zero, zero.conj())
    label0 = np.outer(zero, zero.conj())
    label1 = np.outer(one, one.conj())
    global0 = np.kron(rho, label0)
    global1 = np.kron(rho, label1)
    reduced0 = partial_trace_label(global0)
    reduced1 = partial_trace_label(global1)

    x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    label_only = np.kron(np.eye(2), x)
    moved0 = label_only @ global0 @ label_only.conj().T

    rng = np.random.default_rng(SEED)
    raw = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    q, r = np.linalg.qr(raw)
    q = q @ np.diag(np.exp(-1j * np.angle(np.diag(r))))
    factorized = np.kron(q, x)
    factor0 = partial_trace_label(factorized @ global0 @ factorized.conj().T)
    factor1 = partial_trace_label(factorized @ global1 @ factorized.conj().T)

    # Basis order is system,label. Label 1 controls a system bit flip.
    controlled = np.zeros((4, 4), dtype=complex)
    for s in range(2):
        for lab in range(2):
            source = 2 * s + lab
            target_s = s ^ lab
            controlled[2 * target_s + lab, source] = 1.0
    coupled0 = partial_trace_label(controlled @ global0 @ controlled.conj().T)
    coupled1 = partial_trace_label(controlled @ global1 @ controlled.conj().T)

    # An ordinary internal two-state memory implements the identical dilation.
    ordinary0, ordinary1 = coupled0.copy(), coupled1.copy()

    labeled_assignment_a = np.array([1.0, 0.0])
    labeled_assignment_b = np.array([0.0, 1.0])
    accessible_occupation_a = np.array([1.0, 1.0])
    accessible_occupation_b = np.array([1.0, 1.0])

    replacement_output0 = rho.copy()
    replacement_output1 = rho.copy()
    replacement_choi = np.kron(np.eye(2), rho) / 2

    sequential_candidate = np.array([1.0, 0.0])
    sequential_ordinary_memory = sequential_candidate.copy()
    sequential_memoryless = np.array([0.5, 0.5])

    candidate_table = np.array([[0.8, 0.2], [0.3, 0.7]])
    ordinary_table = candidate_table.copy()

    y = np.array([0.8, 0.2, 0.6])
    restricted = np.column_stack(([1.0, 0.0, 0.5], [0.0, 1.0, 0.5]))
    beta = np.linalg.lstsq(restricted, y, rcond=None)[0]
    restricted_distance = float(np.linalg.norm(y - restricted @ beta))
    expanded = np.column_stack((restricted, [0.0, 0.0, 1.0]))
    expanded_distance = float(np.linalg.norm(y - expanded @ np.linalg.lstsq(expanded, y, rcond=None)[0]))

    return {
        "seed": SEED,
        "v8.72": {"global_trace_distance": trace_distance(global0, global1), "accessible_trace_distance": trace_distance(reduced0, reduced1)},
        "v8.73": {"label_only_accessible_change": trace_distance(partial_trace_label(moved0), reduced0)},
        "v8.74": {"random_factorized_accessible_distance": trace_distance(factor0, factor1), "unitarity_error": float(np.linalg.norm(q.conj().T @ q - np.eye(2)))},
        "v8.75": {"coupled_accessible_trace_distance": trace_distance(coupled0, coupled1), "coupling_unitarity_error": float(np.linalg.norm(controlled.conj().T @ controlled - np.eye(4)))},
        "v8.76": {"candidate_ordinary_max_difference": float(max(np.max(abs(coupled0 - ordinary0)), np.max(abs(coupled1 - ordinary1))))},
        "v8.77": {"labeled_assignment_distance": float(0.5 * abs(labeled_assignment_a - labeled_assignment_b).sum()), "accessible_occupation_distance": float(0.5 * abs(accessible_occupation_a - accessible_occupation_b).sum())},
        "v8.78": {"replacement_output_distance": trace_distance(replacement_output0, replacement_output1), "choi_rank": int(np.linalg.matrix_rank(replacement_choi)), "choi_trace": float(np.trace(replacement_choi).real)},
        "v8.79": {"candidate_vs_ordinary_memory_tv": float(0.5 * abs(sequential_candidate - sequential_ordinary_memory).sum()), "candidate_vs_memoryless_tv": float(0.5 * abs(sequential_candidate - sequential_memoryless).sum())},
        "v8.80": {"finite_control_max_difference": float(np.max(abs(candidate_table - ordinary_table))), "candidate_table": candidate_table.tolist()},
        "v8.81": {"restricted_ordinary_distance": restricted_distance, "expanded_ordinary_distance": expanded_distance, "required_claim_elements": ["defined label Hilbert space", "specified accessible coupling", "conservation-compatible dilation", "preregistered sign and magnitude", "positive distance from a complete ordinary family"]},
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
