"""Finite-dimensional calibration and identity-identifiability controls."""
import json
from itertools import product
from math import cos, log, pi, sin, sqrt

import numpy as np
from scipy.stats import beta, norm

from v532_v541.model import BELL, I, X, Y, Z, partial_transpose

SEED = 542551


def probe_angle():
    contrast = .62
    uncertainty = .4
    angles = np.linspace(-uncertainty, uncertainty, 501)
    # Each model has the same nuisance quadrature; only the X projection reverses.
    plus = .2*np.sin(angles)+contrast*np.cos(angles)/2
    minus = .2*np.sin(angles)-contrast*np.cos(angles)/2
    # A shared physical angle and independently profiled angles give different bounds.
    independent_gap = contrast*cos(uncertainty)-.4*sin(uncertainty)
    return dict(common_angle_gap=float(np.min(plus-minus)), independently_profiled_gap=independent_gap,
                numerical_independent_gap=float(np.min(plus)-np.max(minus)),
                uncalibrated_perpendicular_gap=contrast*cos(pi/2), angle_uncertainty=uncertainty)


def hidden_fragment():
    results = []
    for sign in (1,-1):
        ket = np.zeros(8)
        ket[0], ket[-1] = 1/sqrt(2), sign/sqrt(2)
        state = np.outer(ket,ket)
        visible = np.trace(state.reshape(4,2,4,2),axis1=1,axis2=3)
        parity = float(np.trace(state@np.kron(np.kron(X,X),X)))
        results.append((visible,parity))
    return dict(visible_trace_distance=float(np.linalg.norm(results[0][0]-results[1][0],ord='nuc')/2),
                coherent_parities=[item[1] for item in results],
                visible_diagonal=np.diag(results[0][0]).tolist())


def phase_reference():
    # Linearized phases in a locked unwrap interval, with a separate reference observation.
    science, reference = .28, .10
    science_sd, reference_sd = .04, .05
    covariance = .5*science_sd*reference_sd
    allowed_untracked = .2
    z97 = norm.ppf(.975)
    estimate = science-reference
    se = sqrt(science_sd**2+reference_sd**2-2*covariance)
    design = np.array([[1.,1.],[0.,1.]])
    return dict(estimate=estimate, joint_standard_error=se, interval=[estimate-z97*se,estimate+z97*se],
                falsely_fixed_reference_se=science_sd,
                science_only_rank=int(np.linalg.matrix_rank(design[:1])), joint_rank=int(np.linalg.matrix_rank(design)),
                untracked_reference_refit_error=abs(estimate-min(allowed_untracked,estimate)))


def multi_pair_limit():
    calibration_shots, tagged = 2000, 55
    # One-sided Clopper–Pearson inversion. The tag is assumed perfect on the same sampling population.
    upper = binom_limit(tagged,calibration_shots,.025)
    benchmark = .75+.25*upper
    science_shots, wins = 5000, 3975
    holdout_lower = 1-binom_limit(science_shots-wins,science_shots,.025)
    return dict(calibration_shots=calibration_shots, multi_pair_upper=upper,
                contamination_adjusted_bound=benchmark, science_lower=holdout_lower,
                certified_gap=holdout_lower-benchmark, worst_case_mixture_at_10_percent=.75+.25*.10)


def binom_limit(count, trials, alpha):
    return float(beta.ppf(1-alpha,count+1,trials-count)) if count<trials else 1.


def setting_dependent_flags():
    # Device measures in its own random basis; software accepts only matching bases.
    success_by_basis = np.zeros(2)
    correct_and_accepted = 0.
    for basis, bit, device_basis, outcome in product((0,1),repeat=4):
        matching = (basis == device_basis)
        outcome_probability = float(bit == outcome) if matching else .5
        accepted_probability = outcome_probability*matching/8
        success_by_basis[basis] += accepted_probability
        correct_and_accepted += accepted_probability*(outcome == bit)
    return dict(basis_success_rates=(2*success_by_basis).tolist(),
                conditioned_correct_rate=correct_and_accepted/float(success_by_basis.sum()),
                all_trials_score=correct_and_accepted, classical_all_trials_bound=.75)


def pt_confidence():
    rng = np.random.default_rng(SEED)
    visibility = .49
    rho = visibility*BELL+(1-visibility)*np.eye(4)/4
    operators = [np.kron(a,b) for a,b in list(product((I,X,Y,Z),repeat=2))[1:]]
    true_means = np.array([np.trace(rho@operator).real for operator in operators])
    trials, alpha = 5000, .05
    means = 2*rng.binomial(trials,(1+true_means)/2)/trials-1
    rho_hat = (np.eye(4)+sum(mean*operator for mean,operator in zip(means,operators)))/4
    epsilon = sqrt(2*log(30/alpha)/trials)
    radius = sqrt(15)*epsilon/2  # Orthogonal Pauli coefficients in Frobenius norm.
    minimum = float(np.linalg.eigvalsh(partial_transpose(rho_hat,2))[0])
    sparse_radius = 15*epsilon/4
    return dict(trials_per_setting=trials, alpha=alpha, estimated_pt_minimum=minimum,
                true_pt_minimum=float(np.linalg.eigvalsh(partial_transpose(rho,2))[0]),
                simultaneous_operator_radius=radius, eigenvalue_upper=minimum+radius,
                weaker_triangle_radius=sparse_radius)


def cross_calibration():
    # Two independent routes infer the same physical phase; signed bounds cover drift jointly.
    end_to_end = .31
    input_phase, readout_phase, pulse_phase = .12, -.04, .19
    radii = np.array([.018,.020,.022,.012])
    calibrated = input_phase+readout_phase+pulse_phase
    residual = end_to_end-calibrated
    altered_pulse = pulse_phase+residual
    return dict(predicted_phase=calibrated, observed_phase=end_to_end, residual=residual,
                joint_radius=float(radii.sum()), valid_margin=float(radii.sum()-abs(residual)),
                falsely_ignored_readout_residual=float(end_to_end-input_phase-pulse_phase),
                untracked_pulse_exact_refit_error=float(abs(end_to_end-input_phase-readout_phase-altered_pulse)))


def temporal_rank():
    relaxation = np.diag([.14,.54,.92])
    reads = np.array([.9,.7,.5])
    controls = np.array([[.9,.1,.15],[.05,.8,.15],[.05,.1,.7]])
    # A trial survives in its initial ordinary mode with a mode-specific probability.
    observation = np.vstack([reads@np.linalg.matrix_power(relaxation,k) for k in range(3)])
    table = observation@controls
    singular = np.linalg.svd(table,compute_uv=False)
    fixed_preparation = np.repeat(table[:,[0]],3,axis=1)
    return dict(singular_values=singular.tolist(), entry_radius=.001,
                simultaneous_op_radius=.003, certified_gap=float(singular[-1]-.003),
                without_control_singular=np.linalg.svd(fixed_preparation,compute_uv=False).tolist())


def conserved_label():
    # One-excitation sector of three ordinary bosonic modes: light 0, light 1, material excitation.
    charge = np.diag([0.,1.,1.])
    photon_number = np.diag([1.,1.,0.])
    resonant_energy = 2*np.eye(3)
    conversion = np.array([[0.,0.,0.],[0.,0.,1.],[0.,1.,0.]])
    wrong_charge = np.array([[0.,0.,1.],[0.,0.,0.],[1.,0.,0.]])
    writer = np.array([[1.,0.,0.],[0.,0.,-1j],[0.,-1j,0.]])
    initial = np.array([0.,1.,0.])
    stored = writer@initial
    observed = writer.conj().T@stored
    # An ordinary two-polarization label uses the same input-output map.
    ordinary = np.eye(3)@initial
    return dict(allowed_charge_commutator=float(np.linalg.norm(conversion@charge-charge@conversion)),
                wrong_charge_commutator=float(np.linalg.norm(wrong_charge@charge-charge@wrong_charge)),
                free_energy_commutator=float(np.linalg.norm(conversion@resonant_energy-resonant_energy@conversion)),
                stored_optical_population=float(np.vdot(stored,photon_number@stored).real),
                stored_charge=float(np.vdot(stored,charge@stored).real),
                ordinary_port_refit_error=float(np.linalg.norm(observed-ordinary)))


def blind_holdout():
    rng = np.random.default_rng(SEED+1)
    trials, alpha = 12000, .05
    # An ordinary background sign contrast survives both physical arrangements.
    ordinary = .03
    candidate = .10
    dark_probability = .3
    means = np.array([dark_probability+ordinary+candidate,dark_probability+ordinary,dark_probability,dark_probability])
    samples = rng.binomial(trials,means)/trials
    contrast_weights = np.array([1,-1,-1,1])
    contrast = float(samples@contrast_weights)
    # A two-sided bound on the weighted sum of independent Bernoulli shots.
    radius = sqrt(2*log(2/alpha)/trials)
    ordinary_radius = .04
    failed = samples.copy()
    failed[0] = failed[1]
    return dict(seed=SEED+1, shots_per_cell=trials, readout_means=samples.tolist(),
                contrast=contrast, sampling_radius=radius, validated_ordinary_radius=ordinary_radius,
                exclusion_margin=contrast-radius-ordinary_radius,
                matched_ordinary_contrast=float(failed@contrast_weights))


def run():
    return {f'v5.{number}': operation() for number,operation in enumerate((
        probe_angle,hidden_fragment,phase_reference,multi_pair_limit,setting_dependent_flags,
        pt_confidence,cross_calibration,temporal_rank,conserved_label,blind_holdout,
    ),42)}


if __name__ == '__main__':
    print(json.dumps(run(),indent=2,allow_nan=False))
