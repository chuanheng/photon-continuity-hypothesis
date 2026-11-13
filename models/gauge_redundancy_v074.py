"""v0.74: Three-qubit Z2 lattice gauge toy model.

Hilbert-space order: (left matter, link, right matter).
Exact finite-dimensional mathematical example, NOT photon QED.
"""
from __future__ import annotations
import numpy as np

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
K0 = np.array([1, 0], dtype=complex)
K1 = np.array([0, 1], dtype=complex)
KPLUS = (K0 + K1) / np.sqrt(2)
KMINUS = (K0 - K1) / np.sqrt(2)
I8 = np.eye(8, dtype=complex)

def kron3(a, b, c):
    return np.kron(np.kron(a, b), c)

G_L = kron3(Z, X, I)
G_R = kron3(I, X, Z)
G_LR = G_L @ G_R
GAUGE_GROUP = (I8, G_L, G_R, G_LR)
P_PHYSICAL = (I8 + G_L) @ (I8 + G_R) / 4

PHYSICAL_BASIS = np.column_stack((
    kron3(K0, KPLUS, K0),
    kron3(K1, KMINUS, K1),
))

O_LEFT_CHARGE = kron3(Z, I, I)
O_HOP = kron3(X, Z, X)

def density(vector):
    vector = np.asarray(vector, dtype=complex)
    if vector.ndim != 1:
        raise ValueError('expected state vector')
    norm = np.vdot(vector, vector).real
    if not np.isclose(norm, 1.0):
        raise ValueError('state vector must be normalized')
    return np.outer(vector, vector.conj())

def commutator(a, b):
    return a @ b - b @ a

def is_gauge_invariant(operator, atol=1e-11):
    operator = np.asarray(operator, dtype=complex)
    if operator.shape != (8, 8):
        raise ValueError('operator must be 8x8')
    return bool(np.allclose(commutator(operator, G_L), 0, atol=atol)
                and np.allclose(commutator(operator, G_R), 0, atol=atol))

def physical_projector():
    return P_PHYSICAL.copy()

def physical_projection(rho):
    """Normalized physical-sector postselection, not a CPTP channel."""
    rho = np.asarray(rho, dtype=complex)
    if rho.shape != (8, 8):
        raise ValueError('rho must be 8x8')
    projected = P_PHYSICAL @ rho @ P_PHYSICAL
    weight = float(np.trace(projected).real)
    if weight < 1e-12:
        raise ValueError('state has zero physical-sector weight')
    return projected / weight, weight

def twirl(rho):
    """CPTP group average; does NOT enforce a selected Gauss sector."""
    rho = np.asarray(rho, dtype=complex)
    if rho.shape != (8, 8):
        raise ValueError('rho must be 8x8')
    return sum(g @ rho @ g.conj().T for g in GAUGE_GROUP) / 4

def physical_weight(rho):
    return float(np.trace(P_PHYSICAL @ rho).real)

def compress(operator):
    operator = np.asarray(operator, dtype=complex)
    if operator.shape != (8, 8):
        raise ValueError('operator must be 8x8')
    return PHYSICAL_BASIS.conj().T @ operator @ PHYSICAL_BASIS

def encode_logical(logical_rho):
    logical_rho = np.asarray(logical_rho, dtype=complex)
    if logical_rho.shape != (2, 2):
        raise ValueError('logical state must be 2x2')
    return PHYSICAL_BASIS @ logical_rho @ PHYSICAL_BASIS.conj().T

def expectation(rho, operator):
    return complex(np.trace(np.asarray(rho) @ np.asarray(operator)))

def ancilla_extension(logical_rho, label_bit):
    if label_bit not in (0, 1):
        raise ValueError('label must be 0 or 1')
    label = density(K0 if label_bit == 0 else K1)
    return np.kron(encode_logical(logical_rho), label)

def restricted_label_expectation(joint_rho, system_operator):
    """Accessible algebra: A_sys tensor identity_label."""
    joint_rho = np.asarray(joint_rho, dtype=complex)
    if joint_rho.shape != (16, 16):
        raise ValueError('joint state must be 16x16')
    system_operator = np.asarray(system_operator, dtype=complex)
    if system_operator.shape != (8, 8):
        raise ValueError('system operator must be 8x8')
    return expectation(joint_rho, np.kron(system_operator, I))

def extended_gauge_invariant_label_z():
    """Label-Z commutes with both extended Gauss generators."""
    obs = np.kron(I8, Z)
    return obs, np.kron(G_L, I), np.kron(G_R, I)

def summary():
    psi_bare = kron3(K0, K0, K0)
    bare = density(psi_bare)
    other = G_L @ bare @ G_L
    projected, success = physical_projection(bare)
    return {
        'extended_hilbert_dimension': 8,
        'gauss_constraint_count': 2,
        'physical_hilbert_dimension': int(round(np.trace(P_PHYSICAL).real)),
        'physical_projector_rank': int(np.linalg.matrix_rank(P_PHYSICAL)),
        'bare_physical_weight': success,
        'twirled_physical_weight': physical_weight(twirl(bare)),
        'twirl_vs_projector_frobenius_distance': float(np.linalg.norm(twirl(bare) - projected)),
        'gauge_related_bare_overlap': float(np.trace(bare @ other).real),
        'logical_left_charge': np.real_if_close(compress(O_LEFT_CHARGE)).tolist(),
        'logical_hopping': np.real_if_close(compress(O_HOP)).tolist(),
    }
