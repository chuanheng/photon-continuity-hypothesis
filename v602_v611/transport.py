"""Exactly two Compton interactions in a finite uniform aluminum cylinder."""
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.stats import qmc

from v592_v601.model import kn_kernel
from v582_v591.model import ELECTRON_REST_KEV

TABLE = np.loadtxt(Path(__file__).with_name('al_xraylib_4_3_0.csv'),delimiter=',',skiprows=1)
DENSITY = 2.70
REST = ELECTRON_REST_KEV
Z_NODES, Z_WEIGHTS = leggauss(16)


def attenuation(energy, column=1):
    if np.any((energy < TABLE[0,0]) | (energy > TABLE[-1,0])):
        raise ValueError('Photon energy is outside the frozen cross-section table.')
    return DENSITY*np.interp(energy,TABLE[:,0],TABLE[:,column])


def directions(exit_mu, azimuth, first_uniform, polarized):
    """Return angle density including the Jacobian of the energy-loss cut."""
    opening=np.sqrt(1-exit_mu**2)
    a,b=1+exit_mu,opening*np.cos(azimuth)
    threshold=2-REST*(1/58-1/60)
    norm_sq=a*a+b*b
    upper=(a*threshold-b*np.sqrt(norm_sq-threshold**2))/norm_sq
    first_mu=-1+(upper+1)*first_uniform
    first_sin=np.sqrt(1-first_mu**2)
    cos_second=exit_mu*first_mu+b*first_sin
    first_ratio=1/(1+60/REST*(1-first_mu))
    first_energy=60*first_ratio
    final_ratio=1/(1+first_energy/REST*(1-cos_second))
    final_energy=first_energy*final_ratio
    first_normalization=float(kn_kernel(60,Z_NODES)@Z_WEIGHTS)
    second_normalization=kn_kernel(first_energy[...,None],Z_NODES)@Z_WEIGHTS
    second_kernel=kn_kernel(first_energy,cos_second)
    if polarized:
        degree=first_sin**2/(first_ratio+1/first_ratio-first_sin**2)
        second_kernel+=final_ratio**2*degree*(1-cos_second**2-2*(opening*np.sin(azimuth))**2)
    density=(upper+1)*kn_kernel(60,first_mu)*second_kernel/(first_normalization*second_normalization)
    return first_mu,first_sin,first_energy,final_energy,density


def depth_weight(z_fraction, path_fraction, directions_data, exit_mu, azimuth, thickness, radius):
    mu,transverse,e1,e2,_=directions_data
    depth=z_fraction*thickness
    signed_surface=np.where(mu>0,thickness-depth,depth)
    to_face=np.divide(signed_surface,abs(mu),out=np.full_like(depth+mu,np.inf),where=abs(mu)>0)
    to_side=np.divide(radius,transverse,out=np.full_like(transverse,np.inf),where=transverse>0)
    chord=np.minimum(to_face,to_side)
    intermediate=chord*path_fraction
    second_z=depth+mu*intermediate
    second_x=transverse*intermediate
    outgoing=(thickness-second_z)/exit_mu
    opening=np.sqrt(1-exit_mu**2)
    final_x=second_x+outgoing*opening*np.cos(azimuth)
    final_y=outgoing*opening*np.sin(azimuth)
    forward_face=(final_x**2+final_y**2<=radius**2)
    return (thickness*chord*attenuation(60.,2)*attenuation(e1,2)*forward_face
            *np.exp(-attenuation(60.)*depth-attenuation(e1)*intermediate-attenuation(e2)*outgoing))


def estimate(thickness=.10,radius=.50,cone_deg=3.,power=15,seed=602611,polarized=True):
    points=qmc.Sobol(5,scramble=True,seed=seed).random_base2(power).T
    first_depth,second_path,angle,azimuth,first_angle=points
    cap=1-np.cos(np.deg2rad(cone_deg))
    exit_mu=1-cap*angle
    phi=2*np.pi*azimuth
    direction=directions(exit_mu,phi,first_angle,polarized)
    travel=depth_weight(first_depth,second_path,direction,exit_mu,phi,thickness,radius)
    return float(cap*np.mean(direction[-1]*travel))


def quadrature(thickness=.10,radius=.50,cone_deg=3.,order=24):
    nodes,weights=leggauss(order)
    scaled=(1+nodes)/2
    cap=1-np.cos(np.deg2rad(cone_deg))
    exit_mu=1-cap*scaled[:,None,None]
    azimuth=2*np.pi*np.arange(2*order)[None,:,None]/(2*order)
    direction=directions(exit_mu,azimuth,scaled[None,None,:],True)
    depths=np.zeros_like(direction[-1])
    dw=Z_WEIGHTS/2
    zs=(Z_NODES+1)/2
    for i,z in enumerate(zs):
        for j,path in enumerate(zs):
            depths+=dw[i]*dw[j]*depth_weight(z,path,direction,exit_mu,azimuth,thickness,radius)
    return float(cap*((direction[-1]*depths)@(weights/2)).mean(axis=1)@(weights/2))
