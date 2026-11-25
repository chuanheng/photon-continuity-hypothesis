"""Finite-aperture and thickness checks for conventional forward energy loss."""
import json

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq
from scipy.special import expn
from scipy.stats import norm

from v582_v591.model import compton, ELECTRON_REST_KEV


def kn_kernel(energy, cosine):
    ratio = 1/(1+energy/ELECTRON_REST_KEV*(1-cosine))
    angular = 1-cosine**2
    return ratio**2*(ratio+1/ratio-angular)


def double_probability(cone_degrees, order, polarized=True):
    # Conditional directional kernels: two guaranteed collisions, no target or escape weighting.
    x,w = leggauss(order)
    angle = np.deg2rad(cone_degrees)
    cap = 1-np.cos(angle)
    u = 1-cap*(1-x[:,None,None])/2
    phi = 2*np.pi*np.arange(2*order)[None,:,None]/(2*order)
    transverse = np.sqrt(1-u**2)
    c = 2-ELECTRON_REST_KEV*(1/58-1/60)
    a,b = 1+u,transverse*np.cos(phi)
    # For these small cones and threshold, the loss condition holds from -1 to this root.
    norm_sq = a*a+b*b
    upper = (a*c-b*np.sqrt(norm_sq-c*c))/norm_sq
    mu = -1+(upper+1)*(1+x[None,None,:])/2
    second_cosine = u*mu+b*np.sqrt(1-mu**2)
    first_energy = 60/(1+60/ELECTRON_REST_KEV*(1-mu))
    first_sigma = float(kn_kernel(60,x)@w)
    second_sigma = kn_kernel(first_energy[...,None],x)@w
    second_weight = kn_kernel(first_energy,second_cosine)
    if polarized:
        ratio_first = first_energy/60
        polarization = (1-mu**2)/(ratio_first+1/ratio_first-(1-mu**2))
        exit_y = transverse*np.sin(phi)
        ratio_second = 1/(1+first_energy/ELECTRON_REST_KEV*(1-second_cosine))
        second_weight += ratio_second**2*polarization*(1-second_cosine**2-2*exit_y**2)
    weighted = (kn_kernel(60,mu)/first_sigma)*(second_weight/second_sigma)*(upper+1)/2
    return float(cap/2*np.sum(w*(weighted@w).mean(axis=1)))


def quadrature():
    baseline=double_probability(3,32)
    refined=double_probability(3,64)
    unpolarized=double_probability(3,32,polarized=False)
    return dict(cone_deg=3,loss_threshold_kev=2, conditional_probability=baseline,
                refinement_difference=abs(refined-baseline), polarization_reset_probability=unpolarized)


def aperture_scaling():
    cones=[1.5,3.,6.]
    probabilities=[double_probability(angle,24) for angle in cones]
    area=1-np.cos(np.deg2rad(cones))
    densities=np.array(probabilities)/area
    return dict(cones_deg=cones, conditional_probabilities=probabilities, cone_area_normalized=densities.tolist(),
                half_aperture_ratio=probabilities[0]/probabilities[1])


def grazing():
    # Toy escape geometry: at a uniform path depth bound t, isotropic |mu| and cap D.
    tau=np.array([.001,.01,.1])
    chord_cap=.2
    infinite_second=1-expn(2,tau)
    finite_second=np.minimum(infinite_second,-np.expm1(-chord_cap))
    first=-np.expm1(-tau)
    upper=first*finite_second
    return dict(first_normal_optical_depth=tau.tolist(), second_path_cap_optical_depth=chord_cap,
                second_upper=finite_second.tolist(),two_stage_upper=upper.tolist(),
                infinite_bound_over_naive_square=(first*infinite_second/tau**2).tolist())


def low_tail():
    single_loss=60-compton(60,np.deg2rad(3))
    gaussian=norm.sf((2-single_loss)/.35)
    tail_fraction=.0004
    conditional_tail=.30
    mixture=(1-tail_fraction)*gaussian+tail_fraction*conditional_tail
    return dict(gaussian_upper=float(gaussian),tail_mixture_upper=float(mixture),
                inflation=float(mixture/gaussian),independent_tail_upper=tail_fraction)


def intermediate_deflection():
    cone=np.deg2rad(3)
    target=ELECTRON_REST_KEV*(1/58-1/60)
    lower=brentq(lambda t: (1-np.cos(t))+(1-np.cos(t+cone))-target,0.,np.pi/2)
    first_compton=compton(60,lower)
    extremal=compton(first_compton,lower+cone)
    return dict(minimum_first_angle_deg=float(np.rad2deg(lower)), qualifying_loss_at_bound=float(60-extremal),
                straight_return_symmetric_angle_deg=float(np.rad2deg(np.arccos(1-target/2))))


def thickness_series():
    t=np.array([.5,1.,2.])
    response_linear=.006*t
    response_pair=.006*t**2
    return dict(relative_thickness=t.tolist(),linear=response_linear.tolist(),pair=response_pair.tolist(),
                central_point_gap=float(abs(response_linear[1]-response_pair[1])),
                heldout_max_gap=float(np.max(abs(response_linear-response_pair))),
                ordinary_linear_nuisance_refit=float(np.max(abs(response_linear-.006*t))))


def displacement():
    # Internal straight segment with axial separation dz and first deflection 60 degrees.
    internal_mm=np.array([.02,.07,.15])
    theta=np.pi/3
    shifts=internal_mm*np.tan(theta)
    resolution_mm=.04
    return dict(internal_axial_spacing_mm=internal_mm.tolist(), ideal_shift_mm=shifts.tolist(),
                resolvable_at_fixed_tolerance=(shifts>resolution_mm).tolist(),
                near_surface_exact_limit_mm=float(0*np.tan(theta)))


def recoil_records():
    initial=np.array([0.,0.,60.])
    direction=np.array([np.sin(np.pi/3),0.,np.cos(np.pi/3)])
    mid=compton(60,np.pi/3)*direction
    final=np.array([0.,0.,compton(np.linalg.norm(mid),np.pi/3)])
    recoil=np.vstack((initial-mid,mid-final))
    kinetic=np.hypot(ELECTRON_REST_KEV,np.linalg.norm(recoil,axis=1))-ELECTRON_REST_KEV
    return dict(recoils_kev_c=recoil.tolist(),kinetic_energies_kev=kinetic.tolist(),
                sum_energy_error=float(abs(kinetic.sum()-np.linalg.norm(initial)+np.linalg.norm(final))),
                net_transverse_recoil=float(np.linalg.norm(recoil.sum(axis=0)[:2])),
                individual_transverse_recoil=float(abs(recoil[0,0])))


def repeated_collision_limits():
    n=np.arange(1,5)
    # For exactly n scatters each no larger than pi, an all-backscatter sequence
    # attains the bound for even n with a forward final direction.
    bound=60-1/(1/60+2*n/ELECTRON_REST_KEV)
    direction=(-1.)**n
    return dict(collision_counts=n.tolist(),kinematic_any_direction_max_losses_kev=bound.tolist(),
                all_backscatter_exit_direction_z=direction.tolist(),
                minimum_collisions_for_20kev_loss=int(n[np.flatnonzero(bound>=20)[0]]))


def combined_design():
    thick=np.array([.5,1.,2.,2.,2.])
    angle_acceptance=np.array([1.,1.,1.,.25,.25])
    # Template pairs: smooth solid-angle background and a collimated component.
    background=thick**2*angle_acceptance
    candidate=thick.copy()
    correlated_recoil=np.array([0.,0.,0.,0.,1.])
    design=np.column_stack((background,candidate,correlated_recoil))
    data=design@np.array([.002,.006,.004])
    fit=np.linalg.lstsq(design,data,rcond=None)[0]
    false_null=np.column_stack((background,correlated_recoil))
    ordinary_limited=data-false_null@np.linalg.lstsq(false_null,data,rcond=None)[0]
    return dict(single_cell_rank=int(np.linalg.matrix_rank(design[[1]])),joint_rank=int(np.linalg.matrix_rank(design)),
                fitted_weights=fit.tolist(),ordinary_without_linear_floor=float(np.linalg.norm(ordinary_limited)),
                ordinary_with_linear_refit_error=float(np.linalg.norm(design@fit-data)))


def run():
    operations=(quadrature,aperture_scaling,grazing,low_tail,intermediate_deflection,thickness_series,
                displacement,recoil_records,repeated_collision_limits,combined_design)
    return {f'v{n//100+5}.{n%100:02d}':experiment() for n,experiment in enumerate(operations,92)}


if __name__=='__main__':
    print(json.dumps(run(),indent=2,allow_nan=False))
