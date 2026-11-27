"""Two distinguishable time bins with one delocalized excitation per bin."""
import json
import itertools
import numpy as np


def sector_state(p, copies, independent=False, differential_sigma=0.0):
    bits = np.array(list(itertools.product([0, 1], repeat=copies)))
    n = bits.sum(axis=1)
    amplitudes = np.sqrt(p**n * (1-p)**(copies-n))
    rho = np.outer(amplitudes, amplitudes) * (n[:, None] == n)
    if independent:
        rho = np.diag(np.diag(rho))
    # Additional zero-mean Gaussian phase on the last bin.
    difference = bits[:, -1, None] - bits[:, -1]
    return rho * np.exp(-0.5 * (differential_sigma * difference)**2)


def run():
    one = sector_state(.5, 1)
    common = sector_state(.37, 2)
    block = common[1:3, 1:3]
    weight = np.trace(block)
    separate = sector_state(.37, 2, independent=True)[1:3, 1:3] / weight
    damped = sector_state(.37, 2, differential_sigma=.8)[1:3, 1:3] / weight
    # Beam splitter parity in the one-excitation sector measures X tensor X.
    visibility = float(2*damped[0, 1])
    return {'single': {'coherence': float(one[0, 1]), 'purity': float(np.trace(one@one))},
            'activation': {'weight': float(weight), 'fidelity': float(block.sum()/(2*weight)),
                           'independent_fidelity': float(separate.sum()/2)},
            'differential': {'exchange': visibility, 'equivalent_flip_probability': (1-visibility)/2}}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
