"""Reachable-effect algebra for a controlled optical phase with binary memory."""
import json
import numpy as np

I = np.eye(2)
X = np.array([[0, 1], [1, 0]])
Z = np.diag([1, -1])
PLUS = (I + X) / 2


def reachable(effects, controls):
    """Close the real Hermitian effect span under Heisenberg pullback."""
    basis = []
    pending = list(effects)
    while pending:
        residual = pending.pop().copy().astype(complex)
        for old in basis:
            residual -= np.vdot(old, residual).real * old
        norm = np.linalg.norm(residual)
        if norm > 1e-10:
            new = residual / norm
            basis.append(new)
            pending.extend(u.conj().T @ new @ u for u in controls)
    return basis


def run():
    phase = np.diag([1, 1, 1, -1])
    states = [np.kron(PLUS, (I + sign * Z) / 2) for sign in [1, -1]]
    contrast = states[0] - states[1]
    outputs = {}
    for name, axis in [('count', Z), ('ramsey', X)]:
        effects = [np.kron((I + sign * axis) / 2, I) for sign in [1, -1]]
        basis = reachable(effects, [phase])
        coeff = [np.vdot(b, contrast).real for b in basis]
        probabilities = [float(np.trace(effects[0] @ phase @ s @ phase).real) for s in states]
        outputs[name] = dict(rank=len(basis), projection_norm=float(np.linalg.norm(coeff)),
                             probability_plus=probabilities)
    return outputs


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
