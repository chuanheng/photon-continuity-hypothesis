"""Robust control selection, finite power, and an operational stopping condition."""
import json
from itertools import combinations
from math import sqrt

import numpy as np
from scipy.stats import binom, norm


def optimal_design():
    choices=np.array([[1.,1.],[1.,.8],[.2,.9],[.9,.2],[-.6,.6]])
    pairs=list(combinations(range(len(choices)),2))
    scales=np.array([np.linalg.svd(choices[list(pair)],compute_uv=False)[-1] for pair in pairs])
    index=int(np.argmax(scales))
    return dict(pair=list(pairs[index]), smallest_singular=float(scales[index]),
                calibration_error_bound=float(.03/scales[index]), close_controls_scale=float(scales[0]),
                all_pair_smallest=scales.tolist())


def matrix_uncertainty():
    nominal=np.array([[1.,1.],[.15,.9],[.92,.1]])
    theta=np.array([.19,.17])
    error=np.array([[.02,-.03],[.01,.02],[-.01,.01]])
    signal=nominal@theta
    altered=(nominal+error)@theta
    eps=.06
    theta_radius=.35
    normal_fit=np.linalg.lstsq(nominal,altered,rcond=None)[0]
    sigma=np.linalg.svd(nominal,compute_uv=False)[-1]
    return dict(nominal_sigma_min=float(sigma), robust_sigma_min_lower=float(sigma-eps),
                matrix_error=float(np.linalg.norm(error,2)), actual_response_shift=float(np.linalg.norm(signal-altered)),
                response_shift_bound=eps*theta_radius,
                nominal_coefficient_bias=float(np.linalg.norm(theta-normal_fit)),
                coefficient_bias_bound=float(eps*theta_radius/sigma))


def preparation_leakage():
    decision=np.array([[.91,.13],[.09,.87]])
    true_paths=np.array([.7,.3])
    data=decision@true_paths
    preparation_purity=.88
    flipped=(1-preparation_purity)
    prepared=preparation_purity*true_paths+flipped*true_paths[::-1]
    return dict(clean_target_click=float(data[0]), wrongly_perfect_assumption=float(true_paths[0]),
                composite_target_click=float((decision@prepared)[0]),
                ordinary_false_path_probability=float(decision[0,1]))


def joint_region():
    # Marginal bounds allow any box point; calibrated linear correlations restrict the ellipse.
    sigma=np.array([[.01,.008],[.008,.01]])
    axis=np.array([1.,-1.])/sqrt(2)
    ellipse_support=sqrt(axis@sigma@axis)
    box_support=float(abs(axis)@np.sqrt(np.diag(sigma)))
    alleged=.09
    return dict(ellipse_support=ellipse_support, marginal_box_support=box_support,
                distance_lower=alleged-ellipse_support, box_contains_projection=box_support-alleged)


def helstrom():
    a=np.array([[.5,.28],[.28,.5]])
    b=np.array([[.5,-.12j],[.12j,.5]])
    eig,U=np.linalg.eigh(a-b)
    projector=np.outer(U[:,-1],U[:,-1].conj())
    optimal=(np.trace(a@projector)+np.trace(b@(np.eye(2)-projector))).real/2
    old=abs(a[0,0]-b[0,0])
    return dict(minimal_error=float(1-optimal),trace_distance=float(abs(eig).sum()/2),
                projective_prediction_gap=float(np.trace((a-b)@projector).real), old_population_gap=float(old))


def exact_power():
    p0,p1=.10,.13
    alpha,target=.05,.9
    candidates=np.arange(1,6001)
    threshold=binom.isf(alpha,candidates,p0).astype(int)+1
    all_power=binom.sf(threshold-1,candidates,p1)
    chosen=int(np.flatnonzero(all_power>=target)[0])
    return dict(first_n=int(candidates[chosen]),threshold=int(threshold[chosen]),
                power=float(all_power[chosen]),max_smaller_n_power=float(all_power[:chosen].max()),
                null_probability=float(binom.sf(threshold[chosen]-1,candidates[chosen],p0)))


def correlated_repetitions():
    blocks=24
    sigma_block=.10
    sigma_shot=.08
    repeats=np.array([1,4,16,64])
    correct=np.sqrt((sigma_block**2+sigma_shot**2/repeats)/blocks)
    wrong=np.sqrt((sigma_block**2+sigma_shot**2)/(blocks*repeats))
    contrast=.045
    powers=norm.sf(norm.ppf(.95)-contrast/correct)
    return dict(blocks=blocks,repeats=repeats.tolist(),correct_se=correct.tolist(),
                naive_se=wrong.tolist(), power=powers.tolist(),se_floor=sigma_block/sqrt(blocks))


def transfer_calibration():
    # A transferable unit-gain injection, bounded by independent process drift.
    reference=.20
    sample=.34
    residual=sample-reference
    error=.03
    tight=.06
    broad=.15
    return dict(residual=residual,calibrated_margin=residual-error-tight,
                unmonitored_margin=residual-error-broad,
                ordinary_shift_exact_refit=float(abs(sample-(reference+residual))))


def spectral_holdout():
    # A normalized Gaussian signal and an ordinary narrow line with shifted centroid.
    centers=np.array([0.,1.,2.])
    def resolved_spectrum(centroid):
        weights=np.exp(-.5*(centers-centroid)**2/.35**2)
        return weights/weights.sum()

    signal=resolved_spectrum(.7)
    ordinary=resolved_spectrum(1.3)
    merged=np.array([[1.,1.,1.]])
    limited_center=resolved_spectrum(.9)
    unrestricted_refit=resolved_spectrum(.7)
    return dict(coarse_bin_gap=float(np.max(abs(merged@(signal-ordinary)))),
                resolved_total_variation=float(np.linalg.norm(signal-ordinary,1)/2),
                ordinary_unbounded_centroid_refit=float(np.linalg.norm(signal-unrestricted_refit)),
                bounded_centroid_first_bin_certificate=float(signal[0]-limited_center[0]))


def operational_stop():
    # One uncontrolled ordinary parameter absorbs the candidate; a second calibrated operation does not.
    candidate=np.array([.35,.47])
    admissible=np.linspace(.1,.6,501)
    matched=np.column_stack((admissible,admissible+.12))
    controlled=np.column_stack((admissible,admissible+.05))
    def minimum(matrix):
        return float(np.linalg.norm(matrix-candidate,axis=1).min())
    return dict(single_operational_gap=float(abs(admissible-candidate[0]).min()),
                enlarged_ordinary_gap=minimum(matched), independently_constrained_gap=minimum(controlled),
                analytic_constrained_gap=.07/sqrt(2), uniform_power_ceiling_at_intersection=.05)


def run():
    operations=(optimal_design,matrix_uncertainty,preparation_leakage,joint_region,helstrom,
                exact_power,correlated_repetitions,transfer_calibration,spectral_holdout,operational_stop)
    return {f'v5.{n}':operation() for n,operation in enumerate(operations,72)}


if __name__=='__main__':
    print(json.dumps(run(),indent=2,allow_nan=False))
