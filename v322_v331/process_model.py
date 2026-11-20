"""Exact finite-dimensional synthetic processes. Tensor order S,E."""
import csv
from itertools import product
from math import log
from pathlib import Path

import numpy as np

I = np.eye(2)
X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.diag([1, -1])
ZERO = (I + Z) / 2
PLUS = (I + X) / 2
SWAP = np.eye(4)[[0, 2, 1, 3]]
CNOT_E = np.eye(4)[[0, 3, 2, 1]]
BASIS = [ZERO, I - ZERO, PLUS, (I + Y) / 2]


def evolve(rho, unitary):
    return unitary @ rho @ unitary.conj().T


def intervention(rho, prepared, effect):
    """A single measure-and-prepare branch, with probability retained."""
    environment = np.einsum("ji,iajb->ab", effect, rho.reshape(2, 2, 2, 2))
    return np.kron(prepared, environment)


def probability(rho, gates, operations, effect):
    if len(gates) != len(operations):
        raise ValueError("Each operation must have a following gate")
    for gate, (prepared, measured) in zip(gates, operations):
        rho = evolve(intervention(rho, prepared, measured), gate)
    return np.trace(np.kron(effect, I) @ rho).real.item()


def response_tensor(rho, gates):
    """Full multilinear response coordinates in physical CP-map bases."""
    shape = (4,) * (2 * len(gates) + 1)
    values = np.empty(shape)
    for indices in np.ndindex(shape):
        operations = [(BASIS[a], BASIS[b]) for a, b in zip(indices[:-1:2], indices[1::2])]
        values[indices] = probability(rho, gates, operations, BASIS[indices[-1]])
    return values


def coordinates(matrix):
    basis = np.stack(BASIS).reshape(4, 4).T
    return np.linalg.solve(basis, matrix.reshape(4))


def contract(tensor, operations, effect):
    for prepared, measured in operations:
        for matrix in (prepared, measured):
            tensor = np.tensordot(coordinates(matrix), tensor, axes=1)
    return float(np.real_if_close(coordinates(effect) @ tensor))


def pauli_state(sign):
    return (np.kron(I, I) + sign * np.kron(Z, Z)) / 4


def causal_gap(gate):
    return abs(
        probability(np.eye(4) / 4, [gate, SWAP], [(ZERO, I), (ZERO, I)], ZERO)
        - probability(np.eye(4) / 4, [gate, SWAP], [(I-ZERO, I), (ZERO, I)], ZERO)
    )


def parity_table(constrained):
    return {bits: (1/4 if sum(bits) % 2 == 0 else 0) if constrained else 1/8
            for bits in product(range(2), repeat=3)}


def marginal(table, indices):
    return [sum(p for bits, p in table.items() if tuple(bits[i] for i in indices) == key)
            for key in product(range(2), repeat=len(indices))]


def coherence_readout(sign, effect):
    ket = np.array([1, 0, 0, sign]) / np.sqrt(2)
    rho = np.outer(ket, ket)
    return probability(rho, [SWAP], [(ZERO, effect)], PLUS)


def shared_phase_echo():
    return (np.trace(PLUS @ PLUS).real + np.trace(PLUS @ evolve(PLUS, Z @ Z)).real) / 2


def slip_table(rate):
    return np.array([1 - rate, rate, rate, 1 - rate])


def kl(p, q):
    return p * log(p / q) + (1-p) * log((1-p) / (1-q))


def results():
    gates = [SWAP, CNOT_E]
    rho = pauli_state(1)
    operations = [(PLUS, (I-Y)/2), ((I-Y)/2, I)]
    tensor = response_tensor(rho, gates)
    parity, iid = parity_table(True), parity_table(False)
    erased = response_tensor(np.kron(I/2, I/2), [SWAP])
    silent = response_tensor(np.kron(I/2, ZERO), [np.eye(4)])
    silent_other = response_tensor(np.kron(I/2, PLUS), [np.eye(4)])
    rate = 0.2
    candidate = slip_table(rate)
    memoryless = np.full(4, 0.5)
    # Standard environment bit toggles the stored preparation on readout.
    quantum = np.array([probability(np.kron(I/2, np.diag([1-rate, rate])),
                                    [CNOT_E], [(s, I)], m)
                        for s, m in product([ZERO, I-ZERO], repeat=2)])
    return [
        ('3.22', 'tensor_contraction_error', abs(contract(tensor, operations, PLUS) - probability(rho, gates, operations, PLUS))),
        ('3.23', 'causal_break_gap', causal_gap(SWAP)),
        ('3.23', 'uncoupled_gap', causal_gap(np.eye(4))),
        ('3.24', 'pairwise_max_gap', max(abs(a-b) for pair in [(0,1),(0,2),(1,2)] for a,b in zip(marginal(parity,pair), marginal(iid,pair)))),
        ('3.24', 'triple_tv', sum(abs(parity[b]-iid[b]) for b in parity)/2),
        ('3.25', 'bell_x_branch_gap', abs(coherence_readout(1, PLUS)-coherence_readout(-1, PLUS))),
        ('3.25', 'bell_z_branch_gap', abs(coherence_readout(1, ZERO)-coherence_readout(-1, ZERO))),
        ('3.26', 'shared_phase_echo', shared_phase_echo()),
        ('3.26', 'fresh_phase_echo', np.trace(PLUS @ (PLUS+Z@PLUS@Z)/2).real),
        ('3.27', 'silent_label_tensor_gap', np.max(abs(silent-silent_other))),
        ('3.28', 'correlated_vs_product_tensor_gap', np.max(abs(response_tensor(rho, [SWAP])-erased))),
        ('3.29', 'memoryless_mean_kl', np.mean([kl(p,q) for p,q in zip(candidate,memoryless)])),
        ('3.29', 'shared_memory_mean_kl', np.mean([kl(p,q) for p,q in zip(candidate,quantum)])),
        ('3.30', 'nominal_residual', candidate[1] - 0.15),
        ('3.30', 'profiled_residual', abs(candidate[1] - np.clip(candidate[1], 0.10, 0.25))),
        ('3.31', 'causal_prefix_error', max(
            abs(contract(tensor, [(PLUS, PLUS), (prepared, I)], I)
                - probability(rho, [SWAP], [(PLUS, PLUS)], I))
            for prepared in BASIS)),
    ]


if __name__ == '__main__':
    with Path(__file__).with_name('results.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream, lineterminator='\n')
        writer.writerow(('version', 'metric', 'value', 'provenance'))
        writer.writerows((v, m, format(float(x), '.15g'), 'synthetic') for v, m, x in results())
