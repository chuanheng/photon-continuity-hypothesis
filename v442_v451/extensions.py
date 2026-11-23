"""Controlled optics counterexamples and bounded calibration comparisons."""
from itertools import product

import numpy as np
from scipy.optimize import linprog
from scipy.special import voigt_profile
from scipy.stats import t

SEED = 442451


def probe_rank():
    phi = np.arange(8) * np.pi / 4
    col = np.sin(phi)
    base = np.column_stack((col, col, np.ones(8), np.cos(phi)))
    # A matched reference run disables the target coupling, retaining the probe.
    joint = np.vstack((base, [0, 1, 1, 0], [0, -1, 1, 0]))
    null = np.array([1, -1, 0, 0])
    return {"signal_rank": int(np.linalg.matrix_rank(base)),
            "joint_rank": int(np.linalg.matrix_rank(joint)),
            "null_error": float(np.max(abs(base @ null))),
            "joint_sigma_min": float(np.linalg.svd(joint, compute_uv=False)[-1]),
            "reference_mismatch_bias_per_unit": 1.0}


def bypass_cuts():
    # Convex family over mutually exclusive material, optical and electronic paths.
    masks = np.array(list(product((0, 1), repeat=3)))
    transmissions = np.column_stack((1 - masks, np.ones(8)))
    widths = []
    for row in transmissions:
        fit = linprog(-row, A_ub=[np.ones(4)], b_ub=[1],
                      bounds=[(0, .12), (0, .08), (0, .05), (0, 1)])
        if not fit.success:
            raise RuntimeError(fit.message)
        widths.append(float(-fit.fun))
    caps = np.minimum(1, transmissions @ [.12, .08, .05, 1])
    calibrated = np.minimum(1, transmissions @ [.12, .08, .05, .025])
    return {"cut_order": masks.tolist(), "uncalibrated_upper": widths,
            "formula_error": float(max(abs(caps - widths))),
            "fourth_path_calibrated_upper": calibrated.tolist()}


def clustered_phase():
    rng = np.random.default_rng(SEED)
    runs, shots, replicas = 24, 128, 2400
    # A common random session phase converted linearly by the fringe slope.
    slope, sigma_phase, sigma_read = .7, .18, .30
    phase = rng.normal(0, sigma_phase, (replicas, runs, 1))
    readings = slope * phase + rng.normal(0, sigma_read, (replicas, runs, shots))
    mean = readings.mean(axis=(1, 2))
    naive = readings.std(axis=(1, 2), ddof=1) / np.sqrt(runs * shots)
    cluster = readings.mean(axis=2).std(axis=1, ddof=1) / np.sqrt(runs)
    # Cross-session prediction, all observations from the held-out sessions excluded.
    groups = readings.mean(axis=2)
    train, holdout = groups[:, :16], groups[:, 16:]
    pred = (holdout.mean(axis=1) - train.mean(axis=1)) / (
        train.std(axis=1, ddof=1) * np.sqrt(1/16 + 1/8))
    theoretical = ((slope * sigma_phase)**2 + sigma_read**2 / shots) / runs
    return {"seed": SEED, "replicas": replicas, "sessions": runs,
            "naive_rejection": float(np.mean(abs(mean) > 1.96 * naive)),
            "cluster_rejection": float(np.mean(abs(mean) > t.ppf(.975, runs-1) * cluster)),
            "holdout_rejection": float(np.mean(abs(pred) > t.ppf(.975, 15))),
            "theoretical_mean_variance": theoretical,
            "simulated_mean_variance": float(np.var(mean, ddof=1))}


def spectral_refit():
    from scipy.integrate import quad
    x = np.linspace(-3, 3, 31)
    s0, sd, g0, gd, delta = .27, .19, .11, .07, .13
    # Evaluate convolution over detuning independently of the refit formula.
    def gaussian(q):
        return np.exp(-q*q/(2*sd*sd)) / (sd*np.sqrt(2*np.pi))

    target = np.array([quad(lambda q: gaussian(q) * voigt_profile(
        f - delta - q, s0, g0 + gd), -np.inf, np.inf, epsabs=1e-12)[0] for f in x])
    sigma = np.hypot(s0, sd)
    ordinary = voigt_profile(x-delta, sigma, g0+gd)
    frozen = voigt_profile(x, s0, g0)
    return {"bins": len(x), "fitted_center": delta, "fitted_gaussian_width": float(sigma),
            "fitted_lorentz_width": g0+gd, "frozen_max_error": float(max(abs(frozen-target))),
            "ordinary_max_error": float(max(abs(ordinary-target)))}


def exchange_modes():
    rng = np.random.default_rng(SEED + 1)
    trials = 32
    errors, rotation_errors, contrasts = [], [], []
    for _ in range(trials):
        u, v = rng.normal(size=(2, 3)) + 1j*rng.normal(size=(2, 3))
        u, v = u/np.linalg.norm(u), v/np.linalg.norm(v)
        # Spatial ports first, internal modes second; bosonic symmetrization explicit.
        a, b = np.r_[u, np.zeros(3)], np.r_[np.zeros(3), v]
        bs = np.kron(np.array([[1., 1.], [1., -1.]])/np.sqrt(2), np.eye(3))

        def coincidence(left, right):
            p, q = bs @ left, bs @ right
            state = (np.outer(p, q) + np.outer(q, p))/np.sqrt(2)
            return float(2*np.sum(abs(state[:3, 3:])**2))

        observed = coincidence(a, b)
        errors.append(abs(observed - (1 - abs(np.vdot(u, v))**2)/2))
        rotation, _ = np.linalg.qr(rng.normal(size=(3, 3)) + 1j*rng.normal(size=(3, 3)))
        rotation_errors.append(abs(observed - coincidence(
            np.r_[rotation @ u, np.zeros(3)], np.r_[np.zeros(3), rotation @ v])))
        # A port-selective projection provides additional access to the mode.
        contrasts.append(abs(abs(u[0])**2 - abs((rotation @ u)[0])**2))
    # All modes addressable: bunched projectors sample the full real observable span.
    analyzer = rng.normal(size=(64, 3)) + 1j*rng.normal(size=(64, 3))
    analyzer /= np.linalg.norm(analyzer, axis=1, keepdims=True)
    fock = np.column_stack((*analyzer.T**2, *(np.sqrt(2)*analyzer[:, i]*analyzer[:, j]
                                            for i, j in ((0, 1), (0, 2), (1, 2)))))
    projectors = np.einsum("ni,nj->nij", fock, fock.conj())
    design = np.column_stack((projectors.real.reshape(64, -1),
                              projectors.imag.reshape(64, -1)))
    return {"bunched_projector_rank": int(np.linalg.matrix_rank(design)),
            "bunched_projector_dimension": fock.shape[1]**2,
            "seed": SEED+1, "trials": trials, "formula_error": max(errors),
            "common_rotation_error": max(rotation_errors),
            "mode_resolved_max_contrast": float(max(contrasts))}


def history_cp():
    # A reset-fixed qubit dephasing channel is TP and CP iff |c| <= 1.
    # Ordinary dilation: mix I and Z with weights (1+c)/2 and (1-c)/2.
    outcomes = []
    bell = np.array([1, 0, 0, 1])/np.sqrt(2)
    projector = np.outer(bell, bell)
    for c in (-.8, .35, 1.15):
        choi = projector.copy()
        choi[0, 3] *= c
        choi[3, 0] *= c
        z = np.diag([1, -1, 1, -1])
        refit = (1+c)/2*projector+(1-c)/2*(z @ projector @ z)
        outcomes.append({"c": c, "min_choi": float(np.linalg.eigvalsh(choi)[0]),
                         "tp_error": float(np.max(abs(np.trace(choi.reshape(2,2,2,2),
                                                               axis1=1,axis2=3)-np.eye(2)/2))),
                         "pauli_formula_error": float(np.max(abs(choi-refit))),
                         "x_plus_probability": (1+c)/2})
    # An earlier fair coin cannot acquire a setting-dependent marginal.
    earlier = np.array([.5, .5])
    conditional_readout = np.array([[.2, .9], [.8, .1]])
    joint = earlier[None, :, None] * np.stack(
        (conditional_readout, 1-conditional_readout), axis=-1)
    later_marginals = joint.sum(axis=-1)
    return {"parameters": outcomes,
            "causal_prefix_error": float(max(abs(later_marginals[1]-later_marginals[0])))}


def distance_profile():
    # Parameter boxes for material/instrument signal and bounded readout leakage.
    design = np.array([[1., 1., 0.], [1., -1., 0.], [0., 0., 1.]])
    target = np.array([.31, .13, .04])
    caps = np.linspace(.08, .28, 11)
    distances = []
    for cap in caps:
        bounds = [(0, cap), (-.20, .20), (-.10, .10), (0, None)]
        a = np.column_stack((np.vstack((design, -design)), -np.ones(6)))
        fit = linprog([0, 0, 0, 1], A_ub=a, b_ub=np.r_[target, -target], bounds=bounds)
        if not fit.success:
            raise RuntimeError(fit.message)
        distances.append(float(fit.fun))
    exact = np.maximum(0, .22-caps)
    return {"caps": caps.tolist(), "expectation_linf": distances,
            "binary_tv_at_first_cap": distances[0]/2,
            "formula_error": float(max(abs(distances-exact)))}


def selection_control():
    # Branch probabilities of ordinary heralding depending on a fair hidden bit.
    herald = np.array([[.9, .1], [.1, .9]])
    all_trials = np.stack((.5*herald, .5*(1-herald)), axis=-1)
    conditional = all_trials[:, 1, 0]/all_trials[:, :, 0].sum(axis=1)
    totals = all_trials.sum(axis=-1)
    return {"joint_probabilities": all_trials.tolist(),
            "accepted_rate": all_trials[:, :, 0].sum(axis=1).tolist(),
            "accepted_contrast": float(np.ptp(conditional)),
            "all_trial_contrast": float(np.ptp(totals[:, 1]))}


ROUNDS = {
    "v4.44": probe_rank, "v4.45": bypass_cuts, "v4.46": clustered_phase,
    "v4.47": spectral_refit, "v4.48": exchange_modes, "v4.49": history_cp,
    "v4.50": distance_profile, "v4.51": selection_control,
}
