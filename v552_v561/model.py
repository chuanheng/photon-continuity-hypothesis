"""Two-photon and finite-sample controls for provenance claims."""
import json
from math import cos, log, pi, sin, sqrt

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq

from v542_v551.model import binom_limit

SEED=552561


def bosonic_storage():
    # Fixed total excitation N=2, basis |2,0>, |1,1>, |0,2>.
    n=2
    angles=np.array([.2,.54,pi/2])
    interaction=np.array([[0.,sqrt(2),0.],[sqrt(2),0.,sqrt(2)],[0.,sqrt(2),0.]])
    states=np.vstack([expm(-1j*angle*interaction)[:,0] for angle in angles])
    expected=np.array([[cos(t)**4,2*cos(t)**2*sin(t)**2,sin(t)**4] for t in angles])
    charge=n*np.eye(3)
    return dict(probability_error=float(np.max(abs(abs(states)**2-expected))),
                final_material_two_probability=float(abs(states[-1,-1])**2),
                final_optical_number=float((abs(states[-1])**2)@np.array([2,1,0])),
                charge_expectation=(abs(states)**2@np.diag(charge)).tolist())


def exchange_counts():
    a=np.array([1.,0.])
    b=np.array([.7,sqrt(1-.7**2)])
    direct=np.outer(a,b)
    exchanged=np.outer(b,a)
    same_port_distribution=np.array([
        np.linalg.norm(direct+exchanged)**2/8,
        np.linalg.norm(direct-exchanged)**2/4,
        np.linalg.norm(direct+exchanged)**2/8,
    ])
    amplitude_swapped=[exchanged+direct,exchanged-direct]
    swapped=np.array([np.linalg.norm(amplitude_swapped[0])**2/8,
                      np.linalg.norm(amplitude_swapped[1])**2/4,
                      np.linalg.norm(amplitude_swapped[0])**2/8])
    return dict(same_port_and_coincidence=same_port_distribution.tolist(),
                coincidence_formula=float((1-abs(np.vdot(a,b))**2)/2),
                normalization=float(same_port_distribution.sum()),
                changed_by_input_marker_swap=float(np.max(abs(same_port_distribution-swapped))))


def path_marker():
    overlap=.55
    e0=np.array([1.,0.])
    e1=np.array([overlap,sqrt(1-overlap**2)])
    fringes=[]
    for phase in np.linspace(0,2*pi,81):
        amplitudes=(e0+np.exp(1j*phase)*e1)/2
        fringes.append(float(np.vdot(amplitudes,amplitudes).real))
    difference=np.outer(e0,e0)-np.outer(e1,e1)
    distinguishability=np.linalg.norm(difference,ord='nuc')/2
    visibility=(max(fringes)-min(fringes))/(max(fringes)+min(fringes))
    return dict(optical_visibility=visibility, physical_marker_distinguishability=float(distinguishability),
                squared_sum=float(visibility**2+distinguishability**2),
                minimum_port_probability=min(fringes),maximum_port_probability=max(fringes))


def marker_gauge():
    markers=np.array([[1.,.6,.3],[0.,.8,0.],[0.,0.,sqrt(.91)]],dtype=complex)
    rotation=np.array([[0.,0.,1.],[1.,0.,0.],[0.,1j,0.]])
    transformed=rotation@markers
    gram=lambda states: states.T@states.conj()
    channel_a, channel_b=gram(markers),gram(transformed)
    probe=np.diag([1.,0.,0.])
    independent_gap=abs((markers[:,0].conj()@probe@markers[:,0])-(transformed[:,0].conj()@probe@transformed[:,0]))
    return dict(all_path_coherence_channel_gap=float(np.max(abs(channel_a-channel_b))),
                independently_fixed_marker_probe_gap=float(independent_gap),
                optical_marker_overlap_magnitudes=abs(channel_a[0]).tolist())


def conditional_interference():
    phases=np.linspace(0,2*pi,81)
    plus=(1+np.cos(phases))/4
    minus=(1-np.cos(phases))/4
    return dict(plus_fringe_span=float(np.ptp(2*plus)),minus_fringe_span=float(np.ptp(2*minus)),
                unconditioned_span=float(np.ptp(plus+minus)),
                opposite_phase_joint_difference=float(plus[0]-minus[0]),
                unconditioned_output_probability=float((plus+minus)[0]))


def source_transition():
    early=np.array([[.80,.30],[.20,.70]])
    late=np.array([[.90,.10],[.10,.90]])
    observed=late@early
    ordinary_early=np.eye(2)
    ordinary_late=observed
    return dict(final_transition=observed.tolist(),end_only_refit_error=float(np.max(abs(observed-ordinary_late@ordinary_early))),
                independently_probed_intermediate_gap=float(np.max(abs(early-ordinary_early))),
                input_outcome_conventions=['ordinary destination port 0','ordinary destination port 1'])


def simultaneous_separation():
    rng=np.random.default_rng(SEED)
    ordinary=np.array([.4,.4,.4,.4])
    alternative=ordinary+np.array([.018,.0,.073,.0])
    count=5000
    observed=rng.binomial(count,alternative)/count
    alpha=.05
    radii=np.array([.010,.010,.010,.010])
    pair_error=sqrt(2*log(2*len(ordinary)/alpha)/(4*count))
    residual=abs(observed-ordinary)
    gap=residual-radii-pair_error
    return dict(seed=SEED,samples_per_condition=count, observed=observed.tolist(),
                simultaneous_sampling_radius=pair_error,
                per_condition_separation_lower=gap.tolist(),family_separation_lower=float(max(0,gap.max())))


def source_contamination():
    null_contrast=.035
    max_tainted=1.
    contrast_lower=.085
    # Both terms are conditional means over the same accepted population.
    threshold=(contrast_lower-null_contrast)/(max_tainted-null_contrast)
    f_tight=binom_limit(17,1000,.025)
    f_weak=binom_limit(45,1000,.025)
    return dict(contamination_threshold=threshold, certified_fraction=f_tight, weak_fraction=f_weak,
                tight_margin=contrast_lower-((1-f_tight)*null_contrast+f_tight*max_tainted),
                weak_margin=contrast_lower-((1-f_weak)*null_contrast+f_weak*max_tainted))


def zero_event_coupling():
    # Weak conversion takes two amplitudes proportional to g, hence a g^4 count term.
    exposures=np.array([40.,75.,120.])
    k_nominal=np.array([.8,.65,.5])
    k_lower=np.array([.45,.4,.3])
    alpha=.025
    exact=lambda weights: (-log(alpha)/(exposures@weights))**.25
    worst=exact(k_lower)
    nominal=exact(k_nominal)
    # Numerical inversion of the all-zero Poisson likelihood supplies an independent check.
    numeric=brentq(lambda g: np.exp(-(exposures@k_lower)*g**4)-alpha,0.,1.)
    return dict(nominal_upper=nominal,worst_case_upper=worst,numerical_upper=numeric,
                envelope_zero_probability=float(np.exp(-(exposures@k_lower)*worst**4)),
                zero_probability_at_nominal_using_lower=float(np.exp(-(exposures@k_lower)*nominal**4)),
                joint_error_budget=.05)


def heldout_audit():
    # Freeze one scalar prediction per alignment and independently certify ordinary ranges.
    measured=np.array([.118,.084,-.023])
    ordinary_centers=np.array([.03,.02,-.02])
    ordinary_radii=np.array([.025,.035,.030])
    measurement_radii=np.array([.020,.020,.020])
    candidate=np.array([.10,.09,-.025])
    margins=abs(measured-ordinary_centers)-ordinary_radii-measurement_radii
    candidate_slack=measurement_radii-abs(measured-candidate)
    expanded_radii=np.array([.09,.07,.030])
    ordinary_refit=np.clip(measured,ordinary_centers-expanded_radii,ordinary_centers+expanded_radii)
    return dict(ordinary_interval_separation=margins.tolist(),candidate_compatibility_margin=candidate_slack.tolist(),
                relaxed_ordinary_refit_residual=float(np.max(abs(measured-ordinary_refit))))


def run():
    operations=(bosonic_storage,exchange_counts,path_marker,marker_gauge,conditional_interference,
                source_transition,simultaneous_separation,source_contamination,zero_event_coupling,heldout_audit)
    return {f'v5.{number}': operation() for number,operation in enumerate(operations,52)}


if __name__=='__main__':
    print(json.dumps(run(),indent=2,allow_nan=False))
