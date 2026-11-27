"""Multi-copy delocalised excitations under local-number superselection."""
import itertools
import json
import math
import numpy as np

SEED = 113241

def sector_state(p, copies, independent=False, differential_sigma=0.0):
    bits = np.array(list(itertools.product([0, 1], repeat=copies)))
    n = bits.sum(axis=1)
    amplitudes = np.sqrt(p**n * (1-p)**(copies-n))
    rho = np.outer(amplitudes, amplitudes) * (n[:, None] == n)
    if independent:
        rho = np.diag(np.diag(rho))
    difference = bits[:, -1, None] - bits[:, -1]
    return rho * np.exp(-0.5 * (differential_sigma * difference)**2)

def binary_entropy(p):
    return 0.0 if p in (0.0, 1.0) else -p*math.log2(p)-(1-p)*math.log2(1-p)

def accessible_entanglement(p, copies):
    weights = [math.comb(copies,k)*p**k*(1-p)**(copies-k) for k in range(copies+1)]
    direct = sum(w*math.log2(math.comb(copies,k)) for k,w in enumerate(weights))
    entropy_form = copies*binary_entropy(p) + sum(w*math.log2(w) for w in weights if w > 0)
    return direct, entropy_form

def all_event_chsh(p, survival=1.0, phase_visibility=1.0, dark_flip=0.0):
    useful = survival**2 * 2*p*(1-p)
    visibility = phase_visibility*(1-2*dark_flip)**2
    conditional = 2*math.sqrt(1+visibility**2)
    return 2*(1-useful)+useful*conditional, useful, conditional

def crosstalk_chsh(c):
    contrast = (1-2*c)**2
    return 2*math.sqrt(1+contrast**2), contrast

def calibration_trial(seed=SEED, shots=20000, sigma=0.18):
    rng = np.random.default_rng(seed)
    phase = rng.normal(0, sigma, shots)
    outcomes = np.where(rng.random(shots) < (1+np.cos(phase))/2, 1, -1)
    estimate = float(outcomes.mean())
    expected = math.exp(-sigma**2/2)
    standard_error = math.sqrt((1-estimate**2)/shots)
    return estimate, expected, standard_error

def identifiability_audit():
    t = np.array([-1.5, -.5, .5, 1.5])
    candidate = np.array([1., -1., -1., 1.])
    linear = np.column_stack([np.ones(4), t])
    quadratic = np.column_stack([np.ones(4), t, t*t])
    return {'candidate_residual_linear': float(np.linalg.norm(candidate-linear@np.linalg.lstsq(linear,candidate,rcond=None)[0])),
            'candidate_residual_quadratic': float(np.linalg.norm(candidate-quadratic@np.linalg.lstsq(quadratic,candidate,rcond=None)[0])),
            'rank_with_candidate': int(np.linalg.matrix_rank(np.column_stack([quadratic,candidate])))}

def permutation_audit():
    z = np.diag([1., -1.]); identity = np.eye(2)
    swap = np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]], float)
    labelled = np.kron(z, identity)
    symmetric = np.kron(z, identity)+np.kron(identity, z)
    return {'labelled_swap_commutator': float(np.linalg.norm(labelled@swap-swap@labelled)),
            'symmetric_swap_commutator': float(np.linalg.norm(symmetric@swap-swap@symmetric))}

def run():
    one = sector_state(.5, 1); common = sector_state(.37, 2); block = common[1:3,1:3]
    weight = np.trace(block); separate = sector_state(.37,2,True)[1:3,1:3]/weight
    damped = sector_state(.37,2,differential_sigma=.8)[1:3,1:3]/weight
    ideal = all_event_chsh(.5); imperfect = all_event_chsh(.5,.82,.9,.015)
    scaling = {str(n): accessible_entanglement(.37,n)[0] for n in (1,2,4,8,16,32)}
    estimate, expected, se = calibration_trial(); cross, contrast = crosstalk_chsh(.08)
    return {'single': {'coherence': float(one[0,1]), 'purity': float(np.trace(one@one))},
            'activation': {'weight': float(weight), 'fidelity': float(block.sum()/(2*weight)), 'independent_fidelity': float(separate.sum()/2)},
            'differential': {'exchange': float(2*damped[0,1]), 'equivalent_flip_probability': float((1-2*damped[0,1])/2)},
            'all_event_bell': {'S': ideal[0], 'useful_weight': ideal[1], 'conditional_S': ideal[2]},
            'multicopy': {'entanglement_ebit': scaling, 'n32_per_copy': scaling['32']/32, 'identity_error': max(abs(accessible_entanglement(.37,n)[0]-accessible_entanglement(.37,n)[1]) for n in range(1,33))},
            'loss_dark': {'S': imperfect[0], 'useful_weight': imperfect[1], 'conditional_S': imperfect[2]},
            'crosstalk': {'Smax': cross, 'yz_contrast': contrast},
            'calibration': {'seed': SEED, 'shots': 20000, 'estimate': estimate, 'expected': expected, 'standard_error': se, 'z_score': (estimate-expected)/se},
            'identifiability': identifiability_audit(), 'permutation': permutation_audit()}

if __name__ == '__main__': print(json.dumps(run(), indent=2))
