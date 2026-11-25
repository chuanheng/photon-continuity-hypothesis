"""Mixed two-scatter paths and incomplete-background bounds for aluminum."""
import json
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.stats import qmc, poisson

from v602_v611.transport import attenuation, estimate
from v592_v601.model import kn_kernel
from v582_v591.model import ELECTRON_REST_KEV as REST

SEED=612621
TABLE=np.loadtxt(Path(__file__).with_name('al_angular_xraylib_4_3_0.csv'),delimiter=',',skiprows=1)
NODES,WEIGHTS=leggauss(48)


def angular_energy(energy, mu, process, atomic, polarization=0., cos2_sin2=0.):
    q=energy/12.39841984*np.sqrt(np.maximum(0.,(1-mu)/2))
    if process == 'C':
        ratio=1/(1+energy/REST*(1-mu))
        weight=kn_kernel(energy,mu)+ratio**2*polarization*cos2_sin2
        if atomic:
            weight*=np.interp(q,TABLE[:,0],TABLE[:,1])
    else:
        ratio=1.
        weight=(1+mu**2+polarization*cos2_sin2)*np.interp(q,TABLE[:,0],TABLE[:,2])**2
    return weight,energy*np.broadcast_to(ratio,np.shape(weight))


def rate(path='CC',*,atomic=True,energy=60.,offset=0.,efficiency=False,seed=SEED,power=15):
    zfrac,lfrac,u,azi,mufrac,rotation=qmc.Sobol(6,scramble=True,seed=seed).random_base2(power).T
    thickness,radius=.10,.50
    cap=1-np.cos(np.deg2rad(3.))
    exit_mu=1-cap*u
    phi=2*np.pi*azi
    opening=np.sqrt(1-exit_mu**2)
    b=opening*np.cos(phi)
    k=REST*(1/(energy-2)-1/energy)
    first,second=path
    if path=='CR':
        upper=np.full_like(u,1-k)
    else:
        a=1+exit_mu if path=='CC' else exit_mu
        c=2-k if path=='CC' else 1-k
        norm_sq=a*a+b*b
        upper=(a*c-b*np.sqrt(norm_sq-c*c))/norm_sq
    mu=-1+(upper+1)*mufrac
    transverse=np.sqrt(1-mu**2)
    mu2=exit_mu*mu+b*transverse
    first_weight,e1=angular_energy(energy,mu,first,atomic)
    ratio=e1/energy
    degree=(1-mu**2)/(ratio+1/ratio-(1-mu**2))
    spin_projection=1-mu2**2-2*(opening*np.sin(phi))**2
    second_weight,e2=angular_energy(e1,mu2,second,atomic,degree,spin_projection)
    normal1=angular_energy(energy,NODES,first,atomic)[0]@WEIGHTS
    normal2=angular_energy(e1[:,None],NODES,second,atomic)[0]@WEIGHTS
    x0=offset*np.cos(2*np.pi*rotation)
    y0=offset*np.sin(2*np.pi*rotation)
    z=zfrac*thickness
    boundary_depth=np.where(mu>0,thickness-z,z)
    side=(-x0+np.sqrt(radius**2-y0**2))/transverse
    chord=np.minimum(boundary_depth/abs(mu),side)
    path_length=chord*lfrac
    z2=z+path_length*mu
    x2=x0+path_length*transverse
    outgoing=(thickness-z2)/exit_mu
    exit_x=x2+outgoing*opening*np.cos(phi)
    exit_y=y0+outgoing*opening*np.sin(phi)
    survival=np.exp(-attenuation(energy)*z-attenuation(e1)*path_length-attenuation(e2)*outgoing)
    columns={'C':2,'R':3}
    collision=thickness*chord*attenuation(energy,columns[first])*attenuation(e1,columns[second])
    weight=(cap*(upper+1)*first_weight*second_weight/normal1/normal2)*collision*survival
    weight*=exit_x**2+exit_y**2<=radius**2
    if efficiency:
        weight*=np.clip(.70+.014*(e2-45),.0,1.)
    return float(weight.mean())


def atomic_change():
    free=rate(atomic=False)
    bound=rate()
    return dict(free_rate=free,atomic_angular_rate=bound,relative_change=bound/free-1,
                first_batch_relative_difference=free/estimate()-1)


def mixed_paths():
    values={path:rate(path) for path in ('CC','CR','RC')}
    return dict(rates=values,combined=sum(values.values()),
                mixed_fraction=(values['CR']+values['RC'])/sum(values.values()))


def source_offset():
    centers=[rate(offset=d) for d in (0.,.25,.45)]
    return dict(offset_cm=[0.,.25,.45],rates=centers,outer_to_center=centers[-1]/centers[0])


def omitted_bound():
    thickness,radius=.10,.50
    max_chord=np.hypot(2*radius,thickness)
    energy_after_two=1/(1/60+4/REST)
    nodes=np.r_[energy_after_two,np.arange(41.,60.01,.25),60.]
    maximal_mu=float(np.max(attenuation(nodes)))
    first=-np.expm1(-attenuation(60.)*thickness)
    any_next=-np.expm1(-maximal_mu*max_chord)
    bound=first*any_next**2
    return dict(all_first_interaction_probability=first,max_chord_cm=max_chord,
                at_least_three_interactions_bound=float(bound),bound_over_modeled_two=float(bound/rate()))


def energy_scan():
    vals=[rate(energy=e) for e in (50.,55.,60.,65.)]
    return dict(incident_keV=[50.,55.,60.,65.],rates=vals,max_to_min=max(vals)/min(vals))


def repeat_integration():
    samples=np.array([[rate(path,power=15,seed=SEED+i) for path in ('CC','CR','RC')] for i in range(4)])
    means=samples.mean(axis=0)
    rel=samples.std(axis=0,ddof=1)/np.sqrt(len(samples))/means
    return dict(path_order=['CC','CR','RC'],mean=means.tolist(),relative_integration_se=rel.tolist(),
                ratio_of_mixed_orders=float(means[1]/means[2]))


def energy_efficiency():
    raw=np.array([rate(path) for path in ('CC','CR','RC')])
    detected=np.array([rate(path,efficiency=True) for path in ('CC','CR','RC')])
    return dict(raw=raw.tolist(),detector_folded=detected.tolist(),weighted_efficiency=float(detected.sum()/raw.sum()))


def exposure_budget():
    alternatives=np.array([3e-5,3e-5,3e-5])
    background=np.array([1e-5,2e-5,2.8e-5])
    exposure=2700000
    thresholds=poisson.isf(.025,background*exposure).astype(int)+1
    powers=poisson.sf(thresholds-1,alternatives*exposure)
    return dict(exposure=exposure,background_caps=background.tolist(),powers=powers.tolist())


def indistinguishable_histories():
    # Two different hidden routes and mixtures yield the same two-bin output.
    mixtures=np.array([[.5,.5],[.25,.75]])
    transition=np.array([[[.9,.3],[.1,.7]],[[.9,.5],[.1,.5]]])
    outputs=np.einsum('ijk,ik->ij',transition,mixtures)
    return dict(outputs=outputs.tolist(),visible_gap=float(np.max(abs(outputs[0]-outputs[1]))),
                independently_measured_route_gap=float(abs(mixtures[0,0]-mixtures[1,0])))


def readiness():
    modeled=sum(rate(path) for path in ('CC','CR','RC'))
    hypothetical_increment=1e-5
    upper=omitted_bound()['at_least_three_interactions_bound']
    return dict(known_selected_two_interaction_rate=modeled,
                illustrative_candidate_increment=hypothetical_increment,
                three_interaction_bound=upper,unresolved_budget_ratio=upper/hypothetical_increment)


def run():
    cases=(atomic_change,mixed_paths,source_offset,omitted_bound,energy_scan,repeat_integration,
           energy_efficiency,exposure_budget,indistinguishable_histories,readiness)
    return {f'v6.{n:02d}':operation() for n,operation in enumerate(cases,12)}


if __name__=='__main__':
    print(json.dumps(run(),indent=2,allow_nan=False))
