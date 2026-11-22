"""Standard quantum counterexamples in v4.26 and v4.30."""
from itertools import product

import numpy as np
from scipy.linalg import expm

X = np.array([[0, 1], [1, 0]])
Z = np.diag([1, -1])
I = np.eye(2)


def quantum_memory():
    inputs = list(product(range(2), repeat=2))
    encoded = [(I + ((-1)**x * X + (-1)**z * Z) / np.sqrt(2)) / 2 for x, z in inputs]
    choi = sum(np.kron(np.diag(np.eye(4)[i]), state) for i, state in enumerate(encoded))
    partial_trace = np.einsum("iaka->ik", choi.reshape(4, 2, 4, 2))
    unnormalized_bell = np.eye(2).ravel()
    storage_choi = np.outer(unnormalized_bell, unnormalized_bell)
    storage_trace = np.einsum("iaka->ik", storage_choi.reshape(2, 2, 2, 2))
    success = np.array([
        [np.trace(state @ (I + (-1)**bits[y] * measurement) / 2)
         for y, measurement in enumerate((X, Z))]
        for bits, state in zip(inputs, encoded)
    ])

    # A one-bit memory permits two decoded answer pairs. Enumerate all
    # deterministic encoders and decoders; shared randomness takes convex mixtures.
    optimum = max(
        sum(decoder[encoder[i]][y] == bits[y] for i, bits in enumerate(inputs) for y in (0, 1)) / 8
        for encoder in product(range(2), repeat=4) for decoder in product(inputs, repeat=2)
    )
    # Two ordinary bits store the pair exactly, then add the observed error rate.
    ordinary_reconstruction = np.full_like(success, np.mean(success))
    return {"quantum_success": float(success.mean()), "classical_one_bit_maximum": optimum,
            "two_bit_match_error": float(np.max(abs(success - ordinary_reconstruction))),
            "preparation_choi_min_eigenvalue": float(np.linalg.eigvalsh(choi)[0]),
            "preparation_trace_error": float(np.max(abs(partial_trace - np.eye(4)))),
            "storage_choi_min_eigenvalue": float(np.linalg.eigvalsh(storage_choi)[0]),
            "storage_trace_error": float(np.max(abs(storage_trace - I))),
            "measurement_commutator_norm": float(np.linalg.norm(X @ Z - Z @ X))}


def dispersive_identity_audit():
    # One excitation, in order photon and excited material. C is a separate
    # unresolved device memory. Units set hbar to one.
    omega, coupling, shift, prior = 2.0, 0.42, 0.17, 0.37
    number = np.diag([1, 0])
    exchange = X * coupling
    base = omega * I + exchange
    full = np.kron(base, I) + shift * np.kron(number, Z)
    # Include the zero- and two-excitation sectors of the two-level truncation.
    vacuum = np.zeros((2, 2))
    double = 2 * omega * I + shift * Z
    sectors = np.zeros((8, 8))
    sectors[:2, :2], sectors[2:6, 2:6], sectors[6:, 6:] = vacuum, full, double
    excitation = np.diag([0, 0, 1, 1, 1, 1, 2, 2])
    memory_rho = np.array([[prior, 0.2j], [-0.2j, 1 - prior]])
    photon = np.diag([1, 0])
    full_rho = np.kron(photon, memory_rho)
    projector = np.kron(photon, I)
    times = np.linspace(0, 12, 81)
    max_difference = 0.0
    max_coherent_difference = 0.0
    min_photonic = 1.0
    energy_error = 0.0
    for time in times:
        U = expm(-1j * time * full)
        actual = U @ full_rho @ U.conj().T
        actual_rho = np.einsum("iaka->ik", actual.reshape(2, 2, 2, 2))
        reference = np.zeros((2, 2), dtype=complex)
        for weight, sign in ((prior, 1), (1 - prior, -1)):
            Uc = expm(-1j * time * (base + sign * shift * number))
            reference += weight * (Uc @ photon @ Uc.conj().T)
        max_difference = max(max_difference, abs(np.trace(actual @ projector) - reference[0, 0]))
        max_coherent_difference = max(max_coherent_difference, np.max(abs(actual_rho - reference)))
        min_photonic = min(min_photonic, float(actual_rho[0, 0].real))
        energy_error = max(energy_error, abs(np.trace((actual - full_rho) @ full)))
    return {"detuning_mixture_population_error": float(max_difference),
            "detuning_mixture_full_reduced_state_error": float(max_coherent_difference),
            "energy_error": float(energy_error), "min_photonic_population": min_photonic,
            "number_commutator_norm": float(np.linalg.norm(sectors @ excitation - excitation @ sectors)),
            "memory_min_eigenvalue": float(np.linalg.eigvalsh(memory_rho)[0]),
            "time_samples": len(times)}
