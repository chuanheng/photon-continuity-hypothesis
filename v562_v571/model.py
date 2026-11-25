"""Independent controls and finite comparison of ordinary response families."""
import json
from itertools import product
from math import sqrt

import numpy as np
from scipy.optimize import lsq_linear
from scipy.stats import binom


def controlled_paths():
    # Baseline, material reset and independent path shutter, all complex amplitudes.
    operators = np.array([[1.,1.],[.10,.96],[.92,.06]])
    true = np.array([.13+.07j,.09-.05j])
    measured = operators@true
    fitted = np.linalg.lstsq(operators,measured,rcond=None)[0]
    sigma = np.linalg.svd(operators,compute_uv=False)[-1]
    # Ordinary convention with reset leaking to a second coherent optical path.
    optical_two_path = operators@true
    baseline_relabel = operators[:1]@np.array([0.,true.sum()])
    return dict(single_setting_gap=float(abs(baseline_relabel[0]-measured[0])),
                recovered_components=[[float(c.real),float(c.imag)] for c in fitted],
                smallest_singular_value=float(sigma), error_under_joint_response_radius=float(.02/sigma),
                ordinary_two_path_refit=float(np.max(abs(optical_two_path-measured))))


def auxiliary_port():
    # A qubit is hidden in either of two ordinary memories; the optical port is reset.
    plus = np.array([1.,1.])/sqrt(2)
    ground = np.array([1.,0.])
    initial = np.kron(np.kron(plus,ground),ground).reshape(2,2,2)

    def recover(memory, reset_memories):
        stored = np.swapaxes(initial,0,memory)
        wave = np.expand_dims(stored.take(0,axis=0),0)
        wave = np.concatenate((wave,np.zeros_like(wave)),axis=0)
        for target in reset_memories:
            # Product states here allow resetting the only populated memory exactly.
            if target == memory:
                wave = np.kron(np.kron(ground,ground),ground).reshape(2,2,2)
        readout = np.swapaxes(wave,0,memory)
        return float(np.vdot(readout,readout[::-1]).real)

    return dict(without_selective_reset=[recover(m,()) for m in (1,2)],
                with_reset_on_first_memory=[recover(m,(1,)) for m in (1,2)],
                with_common_reset=[recover(m,(1,2)) for m in (1,2)])


def mode_leakage():
    weights = np.array([.82,.18])
    visibility_by_stratum = np.array([.81,0.])
    physical_coincidence = (1-weights@visibility_by_stratum)/2
    stated_window_coincidence = (1-visibility_by_stratum[0])/2
    return dict(full_window_coincidence=float(physical_coincidence),
                main_window_only_coincidence=float(stated_window_coincidence),
                unbiased_resolved_weights=weights.tolist(),
                matched_ordinary_overlap_squared=float(weights@visibility_by_stratum))


def blocked_randomization():
    # Within-block differences under a sharp null are fixed up to the random sign.
    differences = np.array([.04,.06,.08,.09,.12,.15,.22,.38])
    all_signs = np.array(list(product((-1,1),repeat=len(differences))))
    statistics = np.abs(all_signs@differences)
    ordered = np.sort(statistics)
    pvalues = (len(ordered)-np.searchsorted(ordered,statistics-1e-12))/len(ordered)
    negative = differences*np.array([-1,1,1,1,1,1,1,1])
    p_observed = np.mean(statistics>=abs(negative.sum())-1e-12)
    shared = np.linspace(-30,50,len(differences))
    paired = ((shared+differences)-shared)
    return dict(assignments=len(ordered), observed_pvalue=float(p_observed),
                exact_null_rejection_fraction=float(np.mean(pvalues<=.05)),
                invariance_to_additive_drift=float(np.max(abs(paired-differences))))


def intervention_rank():
    design = np.array([[1.,1.,1.],[0.,1.,1.],[1.,0.,1.]])
    parameters = np.array([.30,.12,.07])
    meas = design@parameters
    null_direction = np.array([0.,1.,-1.])
    return dict(rank_first_two=int(np.linalg.matrix_rank(design[:2])),
                rank_all=int(np.linalg.matrix_rank(design)),
                recovered_effects=np.linalg.solve(design,meas).tolist(),
                two_control_alternative_gap=float(np.max(abs(design[:2]@(.04*null_direction)))),
                third_control_alternative_gap=float(abs(design[-1]@(.04*null_direction))))


def stratum_power():
    samples, null = 900, .10
    threshold = int(binom.isf(.05,samples,null))+1
    alternatives = np.array([.15,.12,.105])
    powers = binom.sf(threshold-1,samples,alternatives)
    return dict(shots_per_stratum=samples,rejection_threshold=threshold,
                null_size=float(binom.sf(threshold-1,samples,null)), powers=powers.tolist(),
                worst_condition_power=float(powers.min()))


def dictionary_certificate():
    dictionary = np.array([[1.,0.],[0.,1.],[.6,.8]])
    measured = np.array([.11,.08,.42])
    limits = np.array([.15,.15])
    fit = lsq_linear(dictionary,measured,bounds=(-limits,limits),tol=1e-13)
    residual = measured-dictionary@fit.x
    witness = residual/np.linalg.norm(residual)
    discrepancy = .02
    support = limits@abs(dictionary.T@witness)+discrepancy
    witness_gap = witness@measured-support
    extra = measured-dictionary@fit.x
    return dict(witness=witness.tolist(), lower_distance=float(witness_gap),
                matching_upper_distance=float(np.linalg.norm(residual)-discrepancy),
                uncalibrated_extra_mode_refit=float(np.linalg.norm(measured-(dictionary@fit.x+extra))))


def identified_interval():
    ylo,yhi=.29,.31
    elo,ehi=.55,.85
    clo,chi=.02,.10
    low=(ylo-chi)/ehi
    high=(yhi-clo)/elo
    nominal=(.30-.06)/.70
    return dict(identified_interval=[low,high], nominal=nominal,
                endpoint_predictors=[ehi*low+chi,elo*high+clo],
                naive_fixed_calibration_interval=[(ylo-.06)/.70,(yhi-.06)/.70])


def charge_echo():
    # Ramsey phase on a logical dual rail, transferred to ordinary matter then recovered.
    u = np.array([1.,1.])/sqrt(2)
    phases = np.array([0.,np.pi/2,np.pi])
    material = np.eye(2)
    probabilities = [abs(np.vdot(u,material.T@np.diag([1.,np.exp(1j*p)])@material@u))**2 for p in phases]
    tagged_candidates=(1+np.cos(phases))/2
    return dict(phases=phases.tolist(),ordinary_storage_echo=probabilities,
                phase_blind_probability=float(probabilities[0]),
                ordinary_refit_error=float(np.max(abs(probabilities-tagged_candidates))),
                contrast=float(probabilities[0]-probabilities[-1]))


def eligibility_intersection():
    # Candidate fit to a probability schedule and a constrained ordinary response box.
    values=np.array([.31,.42,.28])
    ordinary_center=np.array([.26,.37,.29])
    ordinary_radius=np.array([.025,.030,.040])
    candidate_center=np.array([.30,.43,.28])
    observation_radius=.015
    residual=abs(values-ordinary_center)-ordinary_radius-observation_radius
    relaxed=np.clip(values,ordinary_center-.06,ordinary_center+.06)
    return dict(max_calibrated_ordinary_gap=float(residual.max()),
                candidate_margin=float(observation_radius-abs(values-candidate_center).max()),
                relaxed_ordinary_exact_refit=float(np.max(abs(relaxed-values))))


def run():
    experiments=(controlled_paths,auxiliary_port,mode_leakage,blocked_randomization,intervention_rank,
                 stratum_power,dictionary_certificate,identified_interval,charge_echo,eligibility_intersection)
    return {f'v5.{n}':experiment() for n,experiment in enumerate(experiments,62)}


if __name__=='__main__':
    print(json.dumps(run(),indent=2,allow_nan=False))
