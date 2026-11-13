"""Finite-dimensional Rabi eigenspectrum and parity-resolved transition strengths."""
import numpy as np

def build(cutoff, omega=1.0, omega0=1.0, coupling=0.2):
    if isinstance(cutoff, bool) or not isinstance(cutoff, int) or cutoff < 2:
        raise ValueError('cutoff must be integer >= 2')
    if not np.all(np.isfinite([omega, omega0, coupling])):
        raise ValueError('parameters must be finite')
    a = np.diag(np.sqrt(np.arange(1, cutoff, dtype=float)), 1)
    x = a + a.T
    number = np.diag(np.arange(cutoff, dtype=float))
    z = np.diag([-1., 1.])
    sx = np.array([[0., 1.], [1., 0.]])
    identity = np.eye(cutoff)
    h = omega*np.kron(np.eye(2), number) + omega0/2*np.kron(z, identity) + coupling*np.kron(sx, x)
    parity = np.kron(z, np.diag((-1.)**np.arange(cutoff)))
    probe = np.kron(np.eye(2), x)
    return h, parity, probe

def spectrum(cutoff, omega=1.0, omega0=1.0, coupling=0.2):
    h, parity, probe = build(cutoff, omega, omega0, coupling)
    energies, vectors = np.linalg.eigh(h)
    expectations = np.real(np.sum(vectors.conj()*(parity@vectors), axis=0))
    signs = np.where(expectations >= 0, 1, -1)
    transition = vectors.conj().T @ probe @ vectors
    strengths = np.abs(transition)**2
    return energies, signs, strengths, expectations

def convergence(cutoffs, levels=4, omega=1.0, omega0=1.0, coupling=0.2):
    cutoffs = tuple(cutoffs)
    if len(cutoffs) < 2 or any(isinstance(n,bool) or not isinstance(n,int) or n<2 for n in cutoffs):
        raise ValueError('at least two valid cutoffs required')
    if levels < 1 or levels > 2*min(cutoffs):
        raise ValueError('invalid level count')
    reference = spectrum(max(cutoffs), omega, omega0, coupling)[0][:levels]
    return [(n, float(np.max(np.abs(spectrum(n, omega, omega0, coupling)[0][:levels]-reference)))) for n in cutoffs]
