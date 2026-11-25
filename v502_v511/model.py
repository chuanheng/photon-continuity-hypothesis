"""Source geometry, conversion and readout controls for a scalar hypothesis."""
import json

import numpy as np
from scipy.integrate import quad
from scipy.stats import poisson

from . import controls

SEED = 502511


def two_beam_source():
    omega = np.array([1.1,.83])
    mass=.9
    theta = np.r_[np.linspace(0,np.pi,301),np.arccos(1-mass**2/(2*np.prod(omega)))]
    k1 = np.array([0.,0.,1.])
    k2 = np.column_stack((np.sin(theta),np.zeros(len(theta)),np.cos(theta)))
    e1 = np.array([0.,1.,0.])
    e2s = np.broadcast_to(e1,k2.shape)
    e2p = np.column_stack((np.cos(theta),np.zeros(len(theta)),-np.sin(theta)))
    b1 = np.cross(k1,e1)
    source_s = 4*(np.cross(k2,e2s)@b1-e2s@e1)
    source_p = 4*(np.cross(k2,e2p)@b1-e2p@e1)
    invariant_mass = omega.sum()**2-np.linalg.norm(omega[0]*k1+omega[1]*k2,axis=1)**2
    analytic = 2*np.prod(omega)*(1-np.cos(theta))
    # An ordinary angle-dependent coherent difference channel implements this one source scan.
    difference_channel = 4*(k2@k1-1)
    return dict(angle_samples=len(theta),target_mass=mass,phase_matched_angle=float(theta[-1]),
                kinematic_error=float(np.max(abs(invariant_mass-analytic))),
                mass_shell_error=float(abs(invariant_mass[-1]-mass**2)),
                collinear_source=float(source_s[0]),orthogonal_max_source=float(np.max(abs(source_p))),
                counterpropagating_source=float(source_s[-2]),
                ordinary_angular_refit_error=float(np.max(abs(source_s-difference_channel))))


def finite_converter():
    length=6.
    q=2*np.pi/length
    kernel=lambda z: np.exp(1j*q*z)
    # Split into separately oriented coherent domains.
    def integral(left,right):
        return (quad(lambda z: kernel(z).real,left,right,epsabs=1e-12)[0]
                +1j*quad(lambda z: kernel(z).imag,left,right,epsabs=1e-12)[0])
    uniform=integral(0,length)
    switched=integral(0,length/2)-integral(length/2,length)
    analytic=length*np.exp(1j*q*length/2)*np.sinc(q*length/(2*np.pi))
    return dict(length=length,mismatch=q,uniform_normalized_power=float(abs(uniform/length)**2),
                switched_normalized_power=float(abs(switched/length)**2),
                uniform_quadrature_error=float(abs(uniform-analytic)),
                switched_quadrature_error=float(abs(abs(switched)/length-2/np.pi)))


def clipped_readout():
    limit=44
    means=np.arange(1.,111,)
    count=np.arange(limit)
    prob=poisson.pmf(count[None,:],means[:,None])
    tail=poisson.sf(limit-1,means)
    # Score for P(K=k), k<M, is k/mu-1. For the tail its probability
    # derivative is P(Poisson(mu)=M-1).
    fisher=np.sum(prob*(count[None,:]/means[:,None]-1)**2,axis=1)+prob[:,-1]**2/tail
    ideal_ratio=means*fisher
    def mean_clipped(mu):
        return float(count@poisson.pmf(count,mu)+limit*poisson.sf(limit-1,mu))
    h=1e-4
    derivative=(mean_clipped(52+h)-mean_clipped(52-h))/(2*h)
    exact=poisson.cdf(limit-1,52)
    # A coherent optical leakage field and a hypothetical one with the same
    # complex amplitude have identical count likelihood, clipped or unclipped.
    rng=np.random.default_rng(SEED)
    theta=rng.uniform(-np.pi,np.pi,64)
    lo=np.sqrt(52.)
    target=.03*np.exp(.65j)
    ordinary=.03*(np.cos(.65)+1j*np.sin(.65))
    def rates(field):
        return abs(lo+field*np.exp(1j*theta))**2
    return dict(seed=SEED,phase_settings=len(theta),ceiling=limit,scan_means=len(means),
                fisher_ratio_mu_20=float(ideal_ratio[19]),fisher_ratio_mu_80=float(ideal_ratio[79]),
                clipped_mean_slope_mu_52=float(exact),derivative_check_error=float(abs(derivative-exact)),
                leakage_refit_error=float(np.max(abs(rates(target)-rates(ordinary)))))


def run():
    return {
        "v5.02": two_beam_source(),
        "v5.03": finite_converter(),
        "v5.04": clipped_readout(),
        "v5.05": controls.propagation_planes(),
        "v5.06": controls.chopping_parity(),
        "v5.07": controls.reset_logs(),
        "v5.08": controls.zero_event_limit(),
        "v5.09": controls.lifetime_mixture(),
        "v5.10": controls.memory_dimension(),
        "v5.11": controls.preregistered_disk(),
    }


if __name__=="__main__":
    print(json.dumps(run(),indent=2,allow_nan=False))
