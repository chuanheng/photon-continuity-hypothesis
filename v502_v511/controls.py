"""Synthetic propagation, readout and decision controls for v5.05–v5.11."""
import numpy as np
from scipy.linalg import hankel


def propagation_planes():
    """Two guided paths combine into one measured output-mode projection."""
    amplitude = .25 + .15j
    kz = 2.0
    shift = .7
    planes = np.array([0., 1., 2., 2*np.pi/shift])
    reference = np.exp(1j*kz*planes)
    data = reference * (1 + amplitude*np.exp(1j*shift*planes))
    # Divide out calibrated free propagation; ordinary null is a complex constant.
    reduced = data/reference
    two_planes = reduced[:2]
    # The minimum maximum distance of two points to a common center is half their separation.
    one_mode_radius = abs(two_planes[1] - two_planes[0])/2
    ordinary_two_path = reference + amplitude*np.exp(1j*(kz+shift)*planes)
    return dict(planes=planes.tolist(), amplitude=[amplitude.real, amplitude.imag],
                single_plane_error=float(abs(data[0] - (1+amplitude))),
                two_plane_minimax_radius=float(one_mode_radius), calibration_radius=.03,
                margin=float(one_mode_radius-.03),
                aliased_plane_error=float(abs(reduced[-1]-reduced[0])),
                ordinary_two_path_error=float(np.max(abs(data-ordinary_two_path))))


def chopping_parity():
    """Resolved Fourier coefficients of a biased ordinary square-law response."""
    phase = 2*np.pi*np.arange(512)/512
    offset, modulation, coefficient = .6, .3, 1.4
    plus = coefficient*(offset+modulation*np.cos(phase))**2
    minus = coefficient*(offset-modulation*np.cos(phase))**2
    odd = (plus-minus)/2
    even = (plus+minus)/2
    harmonics = lambda waveform: [2*np.mean(waveform*np.cos(order*phase)) for order in (1, 2)]
    ordinary_mixer = 2*coefficient*offset*modulation*np.cos(phase)
    return dict(odd_harmonics=harmonics(odd), even_harmonics=harmonics(even),
                ideal_unbiased_fundamental=float(harmonics(coefficient*(modulation*np.cos(phase))**2)[0]),
                ordinary_mixer_error=float(np.max(abs(odd-ordinary_mixer))))


def reset_logs():
    """Compare ordinary SWAP and SWAP after dephasing in the one-excitation basis."""
    before = np.array([[.5, .5j], [-.5j, .5]])
    swap = np.array([[0, 1], [1, 0]])
    coherent = swap @ before @ swap
    dephased = swap @ np.diag(np.diag(before)) @ swap
    energy = np.diag([0, 1])
    quadrature = np.array([[0, -1j], [1j, 0]])
    def observe(state, observable):
        return float(np.trace(state@observable).real)
    return dict(initial_energy=observe(before, energy),
                final_energies=[observe(state, energy) for state in (coherent, dephased)],
                initial_quadrature=observe(before, quadrature),
                final_quadratures=[observe(state, quadrature) for state in (coherent, dephased)],
                ordinary_swap_trace_error=float(abs(np.trace(coherent)-1)))


def zero_event_limit():
    """Use separately covered transfer efficiency and event probability bounds."""
    alpha_counts, alpha_calibration = .025, .025
    # Independent Bernoulli calibration in target arm: 60 successful transfers in 60 trials.
    calibration_trials, count_trials = 60, 2000
    efficiency_lower = alpha_calibration**(1/calibration_trials)
    event_upper = -np.expm1(np.log(alpha_counts)/count_trials)
    clustered_upper = -np.expm1(np.log(alpha_counts)/20)
    return dict(efficiency_lower=efficiency_lower, observed_event_upper=float(event_upper),
                rate_upper=float(event_upper/efficiency_lower),
                wrongly_pooled_cluster_upper=float(event_upper),
                independent_cluster_upper=float(clustered_upper),
                joint_coverage_lower=1-alpha_counts-alpha_calibration,
                reported_trials=count_trials, independent_blocks_counterexample=20)


def lifetime_mixture():
    """A positive lifetime mixture also describes ordinary electronics latency."""
    rates = np.array([.25, 2.])
    weights = np.array([.22, .78])
    times = np.linspace(0, 12, 241)
    surviving = weights*np.exp(-times[:, None]*rates)
    survival = surviving.sum(axis=1)
    conditional_weights = surviving/survival[:, None]
    hazard = conditional_weights@rates
    negative_variance = hazard**2 - conditional_weights@(rates**2)
    edges = np.arange(7.)
    stored = np.exp(-edges[:, None]*rates)@weights
    detect = weights@(1-np.exp(-rates[:, None]*edges))
    # Include the late complement to keep all the probability mass.
    bin_probabilities = np.r_[-np.diff(stored), stored[-1]]
    detector_bins = np.r_[np.diff(detect), 1-detect[-1]]
    return dict(rates=rates.tolist(), weights=weights.tolist(), early_hazard=float(hazard[0]),
                late_hazard=float(hazard[-1]), max_hazard_slope=float(np.max(negative_variance)),
                bins=bin_probabilities.tolist(),
                detector_latency_refit_error=float(np.max(abs(bin_probabilities-detector_bins))))


def memory_dimension():
    """A certified Hankel rank lower bound for controlled, LTI linear memory."""
    rates = np.array([.15, .55, .91])
    weights = np.array([.35, .45, .2])
    samples = weights@(rates[:, None]**np.arange(7))
    matrix = hankel(samples[:4], samples[3:])
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    entry_error = 1e-4
    operator_radius = 4*entry_error
    fitted_matrix = (rates[None, :]**np.arange(4)[:, None]*weights) @ (
        rates[:, None]**np.arange(4)[None, :])
    return dict(singular_values=singular_values.tolist(), entry_error=entry_error,
                operator_radius=operator_radius, certified_rank=int(np.sum(singular_values>operator_radius)),
                ordinary_three_pole_error=float(np.max(abs(matrix-fitted_matrix))))


def preregistered_disk():
    """Global exclusion over an independently calibrated sum of complex disks."""
    measurement = .12 + .16j
    radii = np.array([.06, .05, .03])  # Ordinary coherent amplitudes and measurement uncertainty.
    total_radius = radii.sum()
    direction = measurement/abs(measurement)
    nearest = total_radius*direction
    # Widen the ordinary path budget by opening a previously unmonitored port.
    extra_path = measurement-nearest
    worst_case_margin = abs(measurement)-total_radius
    circle = total_radius*np.exp(1j*np.linspace(0, 2*np.pi, 1000))
    error_budgets = [.01, .01, .03]
    return dict(measured_magnitude=abs(measurement), radii=radii.tolist(),
                global_distance=float(worst_case_margin),
                nearest_point_residual=float(abs(measurement-nearest)),
                grid_distance=float(np.min(abs(measurement-circle))),
                reopened_port_required=float(abs(extra_path)),
                reopened_port_refit_error=float(abs(measurement-(nearest+extra_path))),
                joint_false_exclusion_bound=sum(error_budgets), component_error_budgets=error_budgets)
