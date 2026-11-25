"""Standard optical controls and synthetic calibration stress tests."""
import json

import numpy as np
from scipy.optimize import brentq
from scipy.stats import beta, binom

SEED = 522531


def narrowband_paths():
    delays = np.array([0., 1.])
    omega = np.linspace(-.04, .04, 41)
    design = np.exp(1j*omega[:, None]*delays)
    _, singular, right = np.linalg.svd(design, full_matrices=False)
    # Scale the least-observed coefficient change to the calibration tolerance.
    tolerance = .05
    perturbation = right[-1].conj()*tolerance/singular[-1]
    heldout = np.exp(1j*np.pi*delays)
    wide = np.exp(1j*np.linspace(-1, 1, 41)[:, None]*delays)
    return dict(calibration_l2=float(np.linalg.norm(design@perturbation)),
                narrow_condition=float(singular[0]/singular[-1]),
                wide_condition=float(np.linalg.cond(wide)),
                perturbation_norm=float(np.linalg.norm(perturbation)),
                heldout_gap=float(abs(heldout@perturbation)))


def passive_scattering():
    # Every column has power below one, but one coherent superposition has gain.
    scattering = np.array([[.7, .7j], [.5, .5j]])
    left, singular, right = np.linalg.svd(scattering)
    closest_passive = (left*np.minimum(singular, 1))@right
    coherent_input = right[0].conj()
    return dict(column_power=np.sum(abs(scattering)**2, axis=0).tolist(),
                coherent_output_power=float(np.linalg.norm(scattering@coherent_input)**2),
                distance_to_contraction=float(np.linalg.norm(scattering-closest_passive, 2)),
                spectral_lower_bound=float(singular[0]-1),
                passive_norm=float(np.linalg.norm(closest_passive, 2)))


def spectral_resolution():
    delay = 4.
    width = 2*np.pi/delay
    mean_frequencies = np.linspace(-2, 2, 9)
    amplitude = .12+.07j
    def channel_average(bin_width):
        return amplitude*np.exp(1j*delay*mean_frequencies)*np.sinc(delay*bin_width/(2*np.pi))
    coarse, fine = channel_average(width), channel_average(width/4)
    translation = 2*np.pi/.5
    sampled = np.exp(1j*delay*np.arange(9)*.5)
    aliased = np.exp(1j*(delay+translation)*np.arange(9)*.5)
    check = np.linspace(-width/2, width/2, 2049)
    integral = np.trapezoid(np.exp(1j*delay*check), check)/width
    return dict(amplitude=float(abs(amplitude)), coarse_max=float(np.max(abs(coarse))),
                fine_fraction=float(np.max(abs(fine))/abs(amplitude)),
                uniform_center_phase_alias=float(np.max(abs(sampled-aliased))),
                quadrature_at_zero=float(abs(integral)))


def injection_crosstalk():
    calibrated = np.array([[1., .05j], [.04, 1.]])
    drift = np.array([[0., 0.], [.10, 0.]])
    injection = np.array([1., 0.])
    observed = (calibrated+drift)@injection
    reconstructed = np.linalg.solve(calibrated, observed)
    error = np.linalg.norm(reconstructed-injection)
    norm_bound = np.linalg.norm(np.linalg.inv(calibrated), 2)*np.linalg.norm(drift, 2)
    expanded_model = np.linalg.solve(calibrated+drift, observed)
    return dict(nominal_science_port_amplitude=float(abs(reconstructed[1])),
                input_error=float(error), certified_input_error_bound=float(norm_bound),
                independently_allowed_matrix_drift=.03,
                observed_residual=float(np.linalg.norm(observed-calibrated@injection)),
                ordinary_drift_refit_error=float(np.linalg.norm(expanded_model-injection)))


def switching_order():
    angle = .4
    rotation = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    attenuation = np.diag([.9, .45])
    preparation = np.array([1., 0.])
    first = rotation@attenuation@preparation
    second = attenuation@rotation@preparation
    return dict(first_output=first.tolist(), second_output=second.tolist(),
                order_difference=float(np.linalg.norm(first-second)),
                identical_commutator_prediction_error=float(
                    np.linalg.norm(first-second-(rotation@attenuation-attenuation@rotation)@preparation)),
                commuting_equal_loss_difference=float(
                    np.linalg.norm(rotation@(.9*np.eye(2))-(.9*np.eye(2))@rotation)))


def zero_events_under_drift():
    # Fixed profile r_j = theta * shape_j; weights jump between two equal-size strata.
    efficiency = np.repeat([.85, .15], 100)
    shape = np.repeat([.2, 1.8], 100)
    exposure = efficiency*shape
    alpha = .05
    def exact(weights):
        return brentq(lambda theta: np.log1p(-theta*weights).sum()-np.log(alpha), 0., .5)
    wrong = exact(np.full(200, efficiency.mean()*shape.mean()))
    exact_bound = exact(exposure)
    envelope = -np.log(alpha)/exposure.sum()
    return dict(exposure=float(exposure.sum()), falsely_factorized_exposure=float(200*efficiency.mean()*shape.mean()),
                exact_profile_upper=exact_bound, exponential_envelope_upper=float(envelope),
                falsely_factorized_upper=wrong,
                zero_probability_at_wrong_upper=float(np.prod(1-wrong*exposure)))


def coherence_window():
    # Uniform average of exp(i*b*t), with endpoints agreeing for a 2*pi ramp.
    t = np.linspace(0., 1., 4097)
    b = 2*np.pi
    rotating = np.exp(1j*b*t)
    bound = .4
    verified = np.exp(1j*bound*(t-.5))
    # If each point remains inside a centered phase arc, its real projection is bounded.
    return dict(endpoint_gap=float(abs(rotating[-1]-rotating[0])),
                unmonitored_coherence=float(abs(np.trapezoid(rotating,t))),
                smooth_reference_coherence=float(abs(np.trapezoid(verified,t))),
                guaranteed_coherence=float(np.cos(bound/2)),
                midpoint_phase_error=float(abs(rotating[len(t)//2]-1.)))


def shared_systematic():
    sigma, systematic = .06, .10
    count = 8
    covariance = sigma**2*np.eye(count)+systematic**2*np.ones((count,count))
    ones = np.ones(count)
    weights = np.linalg.solve(covariance, ones)
    contrast = np.array([1.,-1.,0.,0.,0.,0.,0.,0.])
    return dict(experiments=count, joint_se=float(1/np.sqrt(ones@weights)),
                wrongly_independent_se=float(np.sqrt((sigma**2+systematic**2)/count)),
                common_offset_floor=systematic,
                paired_contrast_se=float(np.sqrt(contrast@covariance@contrast)),
                fixed_offset_rank=int(np.linalg.matrix_rank(np.column_stack((ones,ones)))))


def scalar_field_gap():
    # Weak-conversion transfer for phi F^2 with a static transverse magnetic background.
    frequency = 3.
    mass = .8
    scalar_k = np.sqrt(frequency**2-mass**2)
    q = frequency-scalar_k
    length = np.array([1., 3., 5.])
    coupling_squared = .003
    field_integral = length*np.exp(.5j*q*length)*np.sinc(q*length/(2*np.pi))
    # Production and reconversion use the same signed overlap in the specified geometry.
    candidate = coupling_squared*field_integral*field_integral.conj()*np.exp(1j*scalar_k*4)
    signs = np.array([1.,-1.])
    observed = signs[:,None]*candidate
    ordinary_signed_leakage = signs[:,None]*candidate
    odd_response = (observed[0]-observed[1])/2
    ordinary_bound = .025
    return dict(mass=mass, frequency=frequency, momentum_mismatch=float(q),
                signed_odd_magnitudes=abs(odd_response).tolist(),
                fixed_ordinary_odd_radius=ordinary_bound,
                fixed_family_global_gap=float(max(0.,abs(odd_response[-1])-ordinary_bound)),
                free_ordinary_refit_error=float(np.max(abs(observed-ordinary_signed_leakage))))


def frozen_design():
    rng = np.random.default_rng(SEED)
    shots = 1200
    alpha = .025
    nominal_null = .01
    threshold = int(binom.isf(alpha, shots, nominal_null))+1
    sham_trials, injected_trials = 400, 400
    sham = int(rng.binomial(sham_trials,.002))
    upstream = int(rng.binomial(injected_trials,.76))
    sham_upper = beta.ppf(1-alpha,sham+1,sham_trials-sham)
    power_lower = beta.ppf(alpha,upstream,injected_trials-upstream+1)
    weak_upstream = int(rng.binomial(injected_trials,.52))
    weak_lower = beta.ppf(alpha,weak_upstream,injected_trials-weak_upstream+1)
    return dict(seed=SEED, fixed_shots=shots, rejection_count=threshold,
                null_size=float(binom.sf(threshold-1,shots,nominal_null)),
                synthetic_science_power_at_p_003=float(binom.sf(threshold-1,shots,.03)),
                sham_hits=sham, sham_upper=float(sham_upper), allowed_sham_bound=nominal_null,
                upstream_hits=upstream, upstream_recovery_lower=float(power_lower), required_upstream_bound=.65,
                weak_upstream_hits=weak_upstream, weak_upstream_recovery_lower=float(weak_lower),
                joint_false_rejection_ceiling=float(alpha+binom.sf(threshold-1,shots,nominal_null)))


def run():
    return {
        'v5.22': narrowband_paths(), 'v5.23': passive_scattering(),
        'v5.24': spectral_resolution(), 'v5.25': injection_crosstalk(),
        'v5.26': switching_order(), 'v5.27': zero_events_under_drift(),
        'v5.28': coherence_window(), 'v5.29': shared_systematic(),
        'v5.30': scalar_field_gap(), 'v5.31': frozen_design(),
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, allow_nan=False))
