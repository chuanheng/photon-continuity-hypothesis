"""Standard optical-channel, source and detector counterexamples."""
import json
import math

import numpy as np
from scipy.linalg import expm
from scipy.special import jv

SEED = 452461


def efficiency_product():
    # Independent click background d, pulse transmission t and conditional source yield p.
    transmission = np.array([0., .15, .5, .75, 1.])
    p, eta, dark = .7, .36, .013
    observed = dark + (1-dark)*transmission*p*eta
    refit = dark + (1-dark)*transmission*.42*.60
    derivative = transmission[:, None]*(1-dark)*np.array([[eta, p]])
    calibrated = np.vstack((derivative, [0, 1]))
    e_limits = np.array([.35, .37])
    return {"no_calibration_rank": int(np.linalg.matrix_rank(derivative)),
            "calibrated_rank": int(np.linalg.matrix_rank(calibrated)),
            "refit_max_error": float(np.max(abs(refit-observed))),
            "source_interval": (p*eta/e_limits[::-1]).tolist()}


def dead_time():
    # One-bin nonparalyzable dead time: next slot cannot click if this one did.
    p, trials = .28, 180000
    rng = np.random.default_rng(SEED)
    opportunities = rng.random(trials) < p
    clicks = np.zeros(trials, dtype=bool)
    for i, arrival in enumerate(opportunities[1:], 1):
        clicks[i] = arrival and not clicks[i-1]
    event_mean = p/(1+p)
    errors = {}
    for k in (1, 2, 3):
        simulated = np.mean(clicks[k:] & clicks[:-k]) - clicks.mean()**2
        expected = event_mean*(1-event_mean)*(-p)**k
        errors[str(k)] = [float(simulated), float(expected)]
    return {"seed": SEED, "trials": trials, "simulated_rate": float(clicks.mean()),
            "stationary_rate": event_mean, "lag_covariance_simulation_and_theory": errors}


def afterpulse_probe():
    # For one detector, compare avalanche-fed afterpulse against a real delayed click.
    base, extra = .03, .16
    target = np.array([base, base + (1-base)*extra])
    refit = 1-(1-base)*(1-extra*np.arange(2))
    # At a calibrated second detector the physical echo can route to B,
    # whereas electrically isolated afterpulses remain at A.
    b_efficiency = .55
    echo_b = 1-(1-base)*(1-extra*b_efficiency*np.arange(2))
    afterpulse_b = np.full(2, base)
    return {"passive_max_error": float(max(abs(target-refit))),
            "second_detector_contrast": float(np.ptp(echo_b)-np.ptp(afterpulse_b)),
            "transfer_needed_to_refit": extra*b_efficiency}


def thermal_loss():
    # A vacuum port mixed with a thermal bath. Each Fock component is binomially thinned.
    bath_mean, eta, cutoff = .8, .45, 55
    ratio = bath_mean/(1+bath_mean)
    probabilities = np.zeros(cutoff)
    for n in range(cutoff):
        w = (1-ratio)*ratio**n
        for k in range(n+1):
            probabilities[k] += w*math.comb(n, k)*(1-eta)**k*eta**(n-k)
    out_mean = (1-eta)*bath_mean
    ordinary_source = out_mean**np.arange(cutoff)/(1+out_mean)**(np.arange(cutoff)+1)
    return {"cutoff": cutoff, "bath_tail_bound": ratio**cutoff,
            "equivalent_source_mean": out_mean,
            "pmf_max_error": float(max(abs(probabilities-ordinary_source))),
            "click_probability": float(probabilities[1:].sum())}


def coherent_storage():
    # Ordered one-excitation basis |input>, |matter>, |output>.
    g = .83
    first = np.array([[0,g,0],[g,0,0],[0,0,0]], dtype=complex)
    last = np.array([[0,0,0],[0,0,g],[0,g,0]], dtype=complex)
    pulse = np.pi/(2*g)
    captured = expm(-1j*first*pulse)[:,0]
    outputs = []
    for phase in np.linspace(-np.pi, np.pi, 17):
        stored = np.diag([1, np.exp(1j*phase), 1]) @ captured
        released = expm(-1j*last*pulse) @ stored
        outputs.append([abs(released[2])**2, abs(released[2]+np.exp(1j*phase)),
                        abs(np.vdot(released,released)-1)])
    result = np.array(outputs)
    return {"max_capture_error": float(abs(abs(captured[1])**2-1)),
            "min_output_population": float(result[:,0].min()),
            "phase_transfer_error": float(result[:,1].max()),
            "excitation_error": float(result[:,2].max())}


def temporal_gate():
    # Normalized delayed decays have overlap 1 when gates share support by conditioning.
    dt = .0005
    grid = np.arange(0, 20, dt)
    shift, width, decay = .8, 1.1, 1.3
    f = np.sqrt(decay)*np.exp(-decay*grid/2)
    g = np.where(grid >= shift, np.sqrt(decay)*np.exp(-decay*(grid-shift)/2), 0)
    gate = (grid >= shift)&(grid < shift+width)
    ungated = (dt*np.dot(f, g))**2
    p1, p2 = [dt*np.dot(mode[gate],mode[gate]) for mode in (f,g)]
    gated = (dt*np.dot(f[gate],g[gate]))**2/(p1*p2)
    return {"grid_step": dt, "full_overlap_squared": float(ungated),
            "full_overlap_exact": math.exp(-decay*shift),
            "conditional_overlap_squared": float(gated),
            "acceptances": [float(p1),float(p2)], "acceptance_ratio": float(p1/p2)}


def gaussian_cp():
    # [x,p]=i and vacuum covariance I/2. X=sqrt(eta) I, Y=y I.
    eta, y = .58, .18
    symplectic = np.array([[0,1],[-1,0]])
    transform = np.sqrt(eta)*np.eye(2)
    noise = y*np.eye(2)
    cp_matrix = noise+.5j*(symplectic-transform@symplectic@transform.T)
    vacuum_out = transform@(np.eye(2)/2)@transform.T+noise
    valid_y = .27
    bath_var = valid_y/(1-eta)
    dilation_out = eta*np.eye(2)/2+(1-eta)*bath_var*np.eye(2)
    return {"cp_min_eigenvalue": float(np.linalg.eigvalsh(cp_matrix)[0]),
            "vacuum_output_variance": float(vacuum_out[0,0]), "minimum_noise": (1-eta)/2,
            "thermal_mean_for_valid_y": bath_var-.5,
            "ordinary_refit_error": float(max(abs(np.diag(dilation_out)-(eta/2+valid_y))))}


def phase_reference():
    # Basis |00>, |01>, |10>, |11>. Shared twirl dephases total number.
    state = np.array([0,1,1,0])/np.sqrt(2)
    rho = np.outer(state,state)
    number_a, number_b = np.array([0,0,1,1]), np.array([0,1,0,1])
    phases = 2*np.pi*np.arange(17)/17
    def rotations(number):
        return np.exp(1j*np.outer(phases, number))
    def twirl(phase_factors):
        return sum(w[:,None]*rho*w.conj()[None,:] for w in phase_factors)/len(phase_factors)
    common = twirl(rotations(number_a+number_b))
    separate = twirl((rotations(number_a)[:,None,:]*rotations(number_b)[None,:,:]).reshape(-1,4))
    return {"shared_visibility": float(2*common[1,2].real),
            "independent_visibility": float(2*abs(separate[1,2])),
            "population_error": float(max(abs(np.diag(common-separate))))}


def missing_bounds():
    # Known acceptance q and conditional success r. Free rejected-branch Bernoulli.
    q, r = np.array([.60,.50]), np.array([.62,.44])
    observed = q*r
    endpoints = np.array([observed, observed + 1 - q]).T
    candidates = np.array([observed+(1-q)*np.array([a,b])
                           for a in (0,1) for b in (0,1)])
    contrasts = candidates[:,0]-candidates[:,1]
    equal_target = .48
    reject_ps = (equal_target-observed)/(1-q)
    return {"accepted_contrast": float(r[0]-r[1]),
            "marginal_intervals": endpoints.tolist(),
            "sharp_contrast_interval": [float(min(contrasts)),float(max(contrasts))],
            "equal_marginal_refit": reject_ps.tolist(),
            "ordinary_refit_error": float(max(abs(observed+(1-q)*reject_ps-equal_target)))}


def driven_sidebands():
    # Phase modulator at Ω. Frequencies are indexed relative to a positive carrier.
    depth, steps = 1.4, 2048
    phase = 2*np.pi*np.arange(steps)/steps
    amplitudes = np.fft.fft(np.exp(1j*depth*np.sin(phase)))/steps
    orders = np.arange(-12,13)
    intensity = abs(amplitudes[orders % steps])**2
    detector = np.where(orders > 0, .9, .36)
    recorded = detector*intensity
    return {"sideband_cutoff": 12, "fft_points": steps,
            "sum_loss": float(abs(1-intensity.sum())),
            "bessel_max_error": float(max(abs(intensity-jv(orders,depth)**2))),
            "raw_mean_order": float(orders@intensity),
            "biased_mean_order": float(orders@recorded/recorded.sum()),
            "calibrated_mean_order": float(orders@(recorded/detector))}


MODELS = {
    "v4.52": efficiency_product, "v4.53": dead_time, "v4.54": afterpulse_probe,
    "v4.55": thermal_loss, "v4.56": coherent_storage, "v4.57": temporal_gate,
    "v4.58": gaussian_cp, "v4.59": phase_reference, "v4.60": missing_bounds,
    "v4.61": driven_sidebands,
}


def run():
    return {version: model() for version, model in MODELS.items()}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, allow_nan=False))
