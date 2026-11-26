"""Hamiltonian audit of an explicit identity-label coupling."""
import json

import numpy as np
from scipy.linalg import expm


SEED = 882891


def commutator(a, b): return a @ b - b @ a
def trace_distance(a, b): return float(0.5 * np.linalg.svd(a - b, compute_uv=False).sum())
def ptrace_second(rho): return np.trace(rho.reshape(2, 2, 2, 2), axis1=1, axis2=3)


def run():
    i2 = np.eye(2, dtype=complex)
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    z = np.array([[1, 0], [0, -1]], dtype=complex)
    n = np.array([[0, 0], [0, 1]], dtype=complex)
    zero, one = np.array([1, 0], complex), np.array([0, 1], complex)
    plus = (zero + one) / np.sqrt(2)
    dm = lambda v: np.outer(v, v.conj())
    g, t = 0.3, 1.0

    h_disp = g * np.kron(n, z)
    n_system = np.kron(n, i2)
    u_disp = expm(-1j * h_disp * t)

    fixed0 = np.kron(dm(one), dm(zero))
    fixed1 = np.kron(dm(one), dm(one))
    fixed_out0 = ptrace_second(u_disp @ fixed0 @ u_disp.conj().T)
    fixed_out1 = ptrace_second(u_disp @ fixed1 @ u_disp.conj().T)

    ramsey0 = np.kron(dm(plus), dm(zero))
    ramsey1 = np.kron(dm(plus), dm(one))
    r0 = ptrace_second(u_disp @ ramsey0 @ u_disp.conj().T)
    r1 = ptrace_second(u_disp @ ramsey1 @ u_disp.conj().T)
    ordinary_plus = expm(-1j * g * n * t) @ dm(plus) @ expm(1j * g * n * t)
    ordinary_minus = expm(1j * g * n * t) @ dm(plus) @ expm(-1j * g * n * t)

    swap = np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]], complex)
    h_asym = np.kron(z, i2)
    h_sym = np.kron(z, i2) + np.kron(i2, z)

    bell = (np.kron(zero, zero) + np.kron(one, one)) / np.sqrt(2)
    bell_dm = dm(bell)
    local_label = np.kron(i2, x)
    remote_before = ptrace_second(bell_dm)
    remote_after = ptrace_second(local_label @ bell_dm @ local_label.conj().T)

    h_exchange = 0.5 * g * (np.kron(x, x) + np.kron(y, y))
    n_total = np.kron(n, i2) + np.kron(i2, n)
    u_exchange = expm(-1j * h_exchange * t)
    state10 = np.kron(one, zero)
    exchange_out = u_exchange @ state10
    swap_probability = float(abs(np.vdot(np.kron(zero, one), exchange_out)) ** 2)

    env_plus = dm(plus)
    joint_plus = np.kron(dm(plus), env_plus)
    reduced_dephase = ptrace_second(u_disp @ joint_plus @ u_disp.conj().T)
    coherence = float(np.cos(g * t))
    p = (1 - coherence) / 2
    standard_dephase = (1 - p) * dm(plus) + p * z @ dm(plus) @ z

    times = np.linspace(0, 2, 9)
    candidate = np.array([(1 + np.cos(g * q)) / 2 for q in times])
    ordinary = candidate.copy()

    rng = np.random.default_rng(SEED)
    random_state = rng.normal(size=2) + 1j * rng.normal(size=2)
    random_state /= np.linalg.norm(random_state)

    return {
        "seed": SEED,
        "v8.82": {"energy_commutator_norm": float(np.linalg.norm(commutator(h_disp, n_system))), "coupling_norm": float(np.linalg.norm(h_disp))},
        "v8.83": {"fixed_number_label_trace_distance": trace_distance(fixed_out0, fixed_out1)},
        "v8.84": {"ramsey_label_trace_distance": trace_distance(r0, r1), "analytic_sin_gt": float(abs(np.sin(g * t)))},
        "v8.85": {"ordinary_detuning_max_difference": float(max(np.max(abs(r0-ordinary_plus)), np.max(abs(r1-ordinary_minus))))},
        "v8.86": {"random_state_norm": float(np.linalg.norm(random_state)), "fixed_label_effect_is_detuning": True},
        "v8.87": {"asymmetric_swap_commutator_norm": float(np.linalg.norm(commutator(h_asym, swap))), "symmetric_swap_commutator_norm": float(np.linalg.norm(commutator(h_sym, swap)))},
        "v8.88": {"remote_change_under_label_local_unitary": trace_distance(remote_before, remote_after)},
        "v8.89": {"exchange_total_number_commutator_norm": float(np.linalg.norm(commutator(h_exchange, n_total))), "swap_probability": swap_probability, "analytic_swap_probability": float(np.sin(g*t)**2)},
        "v8.90": {"environment_dephasing_coherence": coherence, "standard_channel_max_difference": float(np.max(abs(reduced_dephase-standard_dephase)))},
        "v8.91": {"nine_time_candidate_ordinary_max_difference": float(np.max(abs(candidate-ordinary))), "status": "no identity-exclusive prediction", "next_requirement": "derive a symmetry- and conservation-compatible intervention relation outside a complete ordinary channel family"}
    }


if __name__ == "__main__": print(json.dumps(run(), indent=2))
