"""Oscillating polarization and finite cavity loading controls."""
import json

import numpy as np
from scipy.integrate import solve_ivp

SEED = 472481


def modulated_rotation():
    phase = 2*np.pi*np.arange(2048)/2048
    theta = .23*np.cos(phase+.51)
    circular_basis = np.array([[1,1],[-1j,1j]])/np.sqrt(2)
    # Relative circular eigenphases yield a real linear polarization rotation.
    amplitude = np.exp(1j*theta[:,None]*np.array([1,-1]))/np.sqrt(2)
    field = amplitude@circular_basis.T
    rotator = np.column_stack((np.cos(theta),np.sin(theta)))
    common_phase = np.exp(1j*theta[:,None])*np.array([[1.,0.]])
    # Random sample of reference-shifted analyzer angles.
    rng = np.random.default_rng(SEED)
    phi = rng.uniform(-np.pi,np.pi,64)
    analyzers = np.array([np.cos(phi),np.sin(phi)])
    probability = abs(field@analyzers)**2
    ordinary = abs(rotator@analyzers)**2
    common = abs(common_phase@analyzers)**2
    stokes_u = 2*np.real(field[:,0]*field[:,1].conj())
    power_reference = np.abs(np.fft.fft(np.exp(1j*theta)))**2
    powers = np.abs(np.fft.fft(amplitude,axis=0))**2
    return {"seed":SEED,"sample_count":len(phase),"analyzers":len(phi),
            "polarization_summed_spectral_power_error":float(max(abs(powers.sum(axis=1)-power_reference))/len(phase)**2),
            "ordinary_rotator_probability_error":float(np.max(abs(ordinary-probability))),
            "common_phase_probability_error":float(np.max(abs(common-probability))),
            "stokes_u_peak_to_peak":float(np.ptp(stokes_u))}


def pulsed_loading():
    # Time in total-linewidth units. One addressable port, critical coupling.
    external, internal, T = .5,.5,4.
    kappa = external+internal
    kernel_norm_squared = (1-np.exp(-kappa*T))/kappa
    rising = lambda t: np.exp(kappa*t/2)/np.sqrt(kernel_norm_squared)
    square = lambda t: 1/np.sqrt(T)

    def integrate(pulse):
        def rhs(t,state):
            a, _, _ = state
            drive = pulse(t)
            return [-kappa*a/2+np.sqrt(external)*drive,
                    (drive-np.sqrt(external)*a)**2, internal*a*a]
        result = solve_ivp(rhs,(-T,0),[0,0,0],rtol=3e-12,atol=1e-13)
        if not result.success:
            raise RuntimeError(result.message)
        amplitude, escaped, lost = result.y[:,-1]
        return np.array([amplitude**2,escaped,lost])

    matched, flat = integrate(rising),integrate(square)
    return {
        "duration":T,"matched_and_square_ledgers":[matched.tolist(),flat.tolist()],
        "optimal_storage_probability":float(external*kernel_norm_squared),
        "max_ledger_error":float(max(abs(matched.sum()-1),abs(flat.sum()-1))),
        "steady_resonant_reflection_amplitude":1-2*external/kappa,
    }


def run():
    return {"v4.72":modulated_rotation(),"v4.73":pulsed_loading()}


if __name__ == "__main__":
    print(json.dumps(run(),indent=2,allow_nan=False))
