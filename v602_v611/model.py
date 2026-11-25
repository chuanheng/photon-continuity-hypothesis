"""Finite foil benchmark and independent bounding controls."""
import json

import numpy as np
from scipy.integrate import quad
from scipy.stats import norm, poisson

from v542_v551.model import binom_limit
from .transport import TABLE, DENSITY, attenuation, estimate, quadrature

SEED=602611


def cross_sections():
    e,p_total,p_compt,p_rayl,p_photo=TABLE[TABLE[:,0]==60][0]
    nist=.2778
    return dict(energy_kev=e, total_cm2_g=p_total, compton_cm2_g=p_compt, rayleigh_cm2_g=p_rayl,
                photoelectric_cm2_g=p_photo, sum_error=abs(p_total-p_compt-p_rayl-p_photo),
                nist_total_cm2_g=nist, relative_total_difference=p_total/nist-1)


def primary_beam():
    thickness=.10
    total=attenuation(60.)
    survival=np.exp(-total*thickness)
    tracked=quad(lambda z: attenuation(60.,2)*np.exp(-total*z),0,thickness)[0]
    return dict(thickness_cm=thickness, uncollided_survival=survival,
                first_compton_probability=tracked, analytic_first_compton=-np.expm1(-total*thickness)*attenuation(60.,2)/total,
                nist_survival=np.exp(-.2778*DENSITY*thickness))


def boundary_escape():
    seeds=range(SEED,SEED+4)
    rates=[estimate(seed=s) for s in seeds]
    narrow=estimate(radius=.10)
    wide=estimate(radius=1.)
    return dict(thickness_cm=.10,radius_cm=.50,energy_kev=60,cone_deg=3.,min_loss_kev=2.,
                reference_rate_per_incident=float(np.mean(rates)),replicate_values=rates,
                quadrature_standard_error=float(np.std(rates,ddof=1)/np.sqrt(len(rates))),
                narrow_radius_rate=narrow,wide_radius_rate=wide)


def response_tail():
    # Sensitivity to a stylized bound-electron broadened line; not a material calibration.
    sigmas=np.array([.35,.55,.75])
    leakage=norm.sf(2./sigmas)
    escape_fraction=.0004
    return dict(sigma_values_kev=sigmas.tolist(), survival_into_loss_window=leakage.tolist(),
                broadened_over_core=float(leakage[-1]/leakage[0]), example_secondary_escape_fraction=escape_fraction)


def polarization_aperture():
    polarized=estimate()
    erased=estimate(polarized=False)
    narrow=estimate(cone_deg=1.5)
    return dict(polarized_rate=polarized, erased_polarization_rate=erased, narrow_cone_rate=narrow,
                polarization_ratio=polarized/erased, aperture_ratio=narrow/polarized)


def independent_integrators():
    fixed=quadrature(order=24)
    estimates=[estimate(power=17,seed=SEED+i) for i in range(4)]
    aggregate=float(np.mean(estimates))
    return dict(tensor_quadrature=fixed,sobol_average=aggregate,relative_disagreement=abs(fixed-aggregate)/fixed,
                independent_material_engine=None)


def geometry_error():
    nominal=estimate()
    thicknesses=[estimate(thickness=t) for t in [.095,.105]]
    apertures=[estimate(cone_deg=c) for c in [2.9,3.1]]
    corner_values=[estimate(thickness=t,cone_deg=c) for t in [.095,.105] for c in [2.9,3.1]]
    return dict(nominal=nominal,thickness_cases=thicknesses,aperture_cases=apertures,
                scenario_min=min(corner_values),scenario_max=max(corner_values),
                counts_per_10m_low=.98e7*min(corner_values),counts_per_10m_high=1.02e7*max(corner_values))


def independent_background():
    # Clopper-Pearson for a synthetic independent detector-tail calibration.
    tail=binom_limit(4,1000000,.025)
    no_plate=binom_limit(1,1000000,.025)
    pair = estimate()
    return dict(detector_tail_upper=tail,empty_geometry_upper=no_plate,ordinary_two_compton_estimate=pair,
                illustrative_sum=tail+no_plate+pair,comparison_uses_synthetic_controls=True)


def kinematic_identity():
    # Coarse-grained ordinary event map already exhausts the measured categories.
    response=np.array([[.91,.05],[.06,.80],[.03,.15]])
    processes=np.array([.94,.06])
    ordinary=response@processes
    # A bookkeeping label distinguishes every process internally but is never read.
    joint=response*processes
    tagged_marginal=joint.sum(axis=1)
    label_and_outcome_distance=np.sum(abs(joint-joint[:,::-1]))/2
    return dict(probability_sum=float(ordinary.sum()),
                visible_total_variation=float(np.linalg.norm(ordinary-tagged_marginal,ord=1)/2),
                hidden_joint_total_variation=float(label_and_outcome_distance))


def feasibility():
    # A conservative illustrative null cap and a preselected alternative; Poisson counts.
    background=2e-5
    alternative=3e-5
    exposures=np.arange(50000,5000001,50000)
    threshold=poisson.isf(.025,background*exposures).astype(int)+1
    powers=poisson.sf(threshold-1,alternative*exposures)
    i=int(np.flatnonzero(powers>=.90)[0])
    return dict(assumed_background_upper=background,assumed_alternative=alternative,
                grid_exposure=int(exposures[i]),counts_threshold=int(threshold[i]),power=float(powers[i]),
                size=float(poisson.sf(threshold[i]-1,background*exposures[i])))


def run():
    operations=(cross_sections,primary_beam,boundary_escape,response_tail,polarization_aperture,
                independent_integrators,geometry_error,independent_background,kinematic_identity,feasibility)
    return {f'v6.{n:02}':f() for n,f in enumerate(operations,2)}


if __name__=='__main__':
    print(json.dumps(run(),indent=2,allow_nan=False))
