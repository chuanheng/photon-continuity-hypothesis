"""Energy balance and conventional controls for the metal-foil hypothesis."""
import json

import numpy as np
from scipy.optimize import linprog
from scipy.stats import binom, norm

from v542_v551.model import binom_limit

AL_ENERGY_KEV = np.array([30.,40.,60.,80.])
AL_MU_OVER_RHO = np.array([1.128,.5685,.2778,.2018])
ELECTRON_REST_KEV = 511.


def compton(energy, angle):
    return energy/(1+energy/ELECTRON_REST_KEV*(1-np.cos(angle)))


def ledger():
    # Incident-energy fractions of disjoint channels; these fractions are synthetic.
    partition = np.array([.67,.08,.04,.16,.03,.02])
    direct, forward_scatter, backward, heat, escaping_secondaries, stored = partition
    measured = direct + .4*forward_scatter + backward + heat
    thickness_areal = .27
    return dict(channels=partition.tolist(), closure=float(partition.sum()), measured_ledger=float(measured),
                unmeasured_energy=float(1-measured), nontransmitted_in_cone=float(1-direct-.4*forward_scatter),
                nist_60kev_primary_survival=float(np.exp(-.2778*thickness_areal)),
                nist_60kev_mu_en_over_mu=.1099/.2778)


def aperture():
    apertures_deg=np.array([1.,3.,8.])
    narrow_width=4.
    ordinary_direct=.020
    diffuse_flux=.045
    accepted=diffuse_flux*(-np.expm1(-.5*(apertures_deg/narrow_width)**2))
    tail=ordinary_direct+accepted
    chosen=tail[1]
    return dict(apertures_deg=apertures_deg.tolist(),ordinary_transmission=tail.tolist(),
                single_aperture_flat_refit=float(chosen),
                wider_aperture_gap=float(tail[-1]-chosen))


def film_response(index, reduced_thickness):
    # Normal incidence with vacuum on both sides; positive Im(n) means attenuation.
    r01=(1-index)/(1+index)
    phase=2*np.pi*index*reduced_thickness
    loop=np.exp(2j*phase)
    denom=1-r01**2*loop
    r=r01*(1-loop)/denom
    t=(1-r01**2)*np.exp(1j*phase)/denom
    R,T=abs(r)**2,abs(t)**2
    # Internal forward/backward field amplitudes at the first surface.
    forward=(1+r+(1-r)/index)/2
    backward=(1+r-(1-r)/index)/2
    z=np.linspace(0,reduced_thickness,4097)
    field=forward*np.exp(2j*np.pi*index*z)+backward*np.exp(-2j*np.pi*index*z)
    absorption=2*np.pi*np.imag(index**2)*np.trapezoid(abs(field)**2,z)
    return R,T,absorption


def film():
    index=1.8+.15j
    values=np.array([film_response(index,d) for d in [.17,.2,.23]])
    return dict(reduced_thicknesses=[.17,.2,.23], R_T_A=values.tolist(),
                independently_integrated_closure_error=float(np.max(abs(values.sum(axis=1)-1))),
                transmission_range=float(np.ptp(values[:,1])))


def calorimetry():
    outputs = np.array([42.,48.,54.,60.])
    linked_heat = 60-outputs
    shuffled_heat = linked_heat[::-1]
    return dict(energy_kev=60,mean_photon_energy=float(outputs.mean()),mean_heat=float(linked_heat.mean()),
                correlated_max_closure_error=float(np.max(abs(outputs+linked_heat-60))),
                swapped_same_marginal_max_error=float(np.max(abs(outputs+shuffled_heat-60))),
                linked_covariance=float(np.cov(outputs,linked_heat,ddof=0)[0,1]),
                swapped_covariance=float(np.cov(outputs,shuffled_heat,ddof=0)[0,1]))


def scattering_tail():
    energy=60.
    cone_angle=np.deg2rad(3.)
    max_single_loss=energy-compton(energy,cone_angle)
    first=compton(energy,np.pi/3)
    second=compton(first,np.pi/3)
    # The second scattering reverses the first deflection, not its energy transfer.
    incident=np.array([0.,0.,1.])
    intermediate=np.array([np.sin(np.pi/3),0.,np.cos(np.pi/3)])
    returned=np.array([0.,0.,1.])
    net_recoil=energy*incident-first*intermediate+first*intermediate-second*returned
    cut=2.
    sigma=.35
    tail_at_cone=norm.sf((cut-max_single_loss)/sigma)
    return dict(single_loss_in_3deg_kev=float(max_single_loss), return_direction_error=float(np.linalg.norm(returned-incident)),
                two_scatter_output_kev=float(second),two_scatter_loss_kev=float(energy-second),
                total_recoil_momentum_kev_over_c=net_recoil.tolist(),
                gaussian_single_false_tail_upper=float(tail_at_cone))


def common_material():
    # Standard uncollided prediction; true effective areal scale is synthetic.
    areal=np.array([.08,.27,.72])
    effective=1.04
    depths=areal[:,None]*AL_MU_OVER_RHO
    exact=np.exp(-effective*depths)
    shared_scale=float(np.linalg.lstsq(depths[:2,:3].ravel()[:,None],-np.log(exact[:2,:3]).ravel(),rcond=None)[0][0])
    heterogeneous=exact.copy()
    heterogeneous[-1,-1]*=.97
    return dict(energy_kev=AL_ENERGY_KEV.tolist(),nist_mu_over_rho=AL_MU_OVER_RHO.tolist(),
                recovered_shared_scale=shared_scale,
                homogeneous_heldout_error=float(np.max(abs(exact-np.exp(-shared_scale*depths)))),
                mismatched_heldout_error=float(abs(heterogeneous[-1,-1]-np.exp(-shared_scale*depths[-1,-1]))))


def redistribution():
    # Bounds for a synthetic detector tail and ordinary scattering component.
    # x levels increase held-out intensity by [ .3, .8 ]; both also load a reference window.
    limits=[(.0,.12),(.0,.09)]
    target=np.array([.3,.8])
    monitor=np.array([.6,.4])
    observed=.115
    monitor_max=.048
    opt=linprog(-target,A_ub=[monitor],b_ub=[monitor_max],bounds=limits,method='highs')
    if not opt.success:
        raise RuntimeError(opt.message)
    return dict(ordinary_max=float(target@opt.x),components=opt.x.tolist(),monitor_load=float(monitor@opt.x),
                gap=float(observed-target@opt.x),
                unconstrained_box_gap=float(observed-target@np.array([.12,.09])),
                wider_ordinary_exact_refit_error=float(abs(observed-target@np.array([.15,.0875]))))


def rare_counts():
    calibration_shots=100000
    false_events=18
    upper=binom_limit(false_events,calibration_shots,.025)
    n=np.arange(1,120001)
    thresholds=binom.isf(.025,n,upper).astype(int)+1
    powers=binom.sf(thresholds-1,n,.00075)
    picked=int(np.flatnonzero(powers>=.9)[0])
    return dict(calibration_shots=calibration_shots, background_upper=upper,
                required_shots=int(n[picked]), threshold=int(thresholds[picked]),
                heldout_power=float(powers[picked]), lower_n_max_power=float(max(powers[:picked])),
                worst_case_null_tail=float(binom.sf(thresholds[picked]-1,n[picked],upper)))


def collinear_recoil():
    # c=1, energies and masses in keV. The outgoing light remains collinear.
    mass, delta=511.,6.
    final_energy=mass+delta
    final_momentum=delta
    invariant=mass**2+2*mass*delta
    required_mass=np.sqrt(invariant)
    kinetic_free=np.hypot(mass,final_momentum)-mass
    return dict(rest_mass_kev=mass, requested_loss_kev=delta,
                invariant_mass_squared_increase_kev2=2*mass*delta,
                free_recoil_kinetic_kev=float(kinetic_free),
                target_mass_increase_kev=float(required_mass-mass),
                energy_closure_with_excitation=float(abs(np.hypot(required_mass,final_momentum)-final_energy)))


def joint_gate():
    observed=np.array([.190,.138,.136])
    # Two independent ordinary templates, with nonnegative fitted weights.
    design=np.array([[1.,0.],[.6,.2],[.2,.6]])
    ordinary=np.array([.18,.10])
    reference=design@ordinary
    residual=observed-reference
    # Add one ordinary template with normalized entries and a small amplitude.
    extension=np.array([.25,.25,1.])
    fit=reference+.04*extension
    return dict(observed=observed.tolist(),base_residual=residual.tolist(),
                third_bin_gap_with_calibration_radius=float(abs(residual[-1])-.015),
                expanded_ordinary_refit=float(np.max(abs(fit-observed))))


def run():
    experiments=(ledger,aperture,film,calorimetry,scattering_tail,common_material,
                 redistribution,rare_counts,collinear_recoil,joint_gate)
    return {f'v5.{n}':experiment() for n,experiment in enumerate(experiments,82)}


if __name__=='__main__':
    print(json.dumps(run(),indent=2,allow_nan=False))
