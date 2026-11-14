"""v0.92 Wigner-Weisskopf approximation and finite-mode Hermitian benchmark.
Gamma is the excited-population decay rate. This is established quantum optics,
not a mechanism for persistent individual photon identities.
"""
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import expm_multiply

def atomic_amplitude(t,gamma=1.,lamb_shift=0.):
    t=np.asarray(t,float)
    if gamma<=0 or np.any(t<0):raise ValueError('gamma and t')
    return np.exp((-gamma/2-1j*lamb_shift)*t)

def excited_population(t,gamma=1.):
    return abs(atomic_amplitude(t,gamma))**2

def detection_density(t,gamma=1.):
    return gamma*excited_population(t,gamma)

def emission_probability_by(t,gamma=1.):
    if gamma<=0 or np.any(np.asarray(t)<0):raise ValueError('gamma and t')
    return -np.expm1(-gamma*np.asarray(t,float))

def time_mode(t,gamma=1.,omega0=0.):
    if gamma<=0:raise ValueError('gamma')
    t=np.asarray(t,float)
    return np.where(t>=0,np.sqrt(gamma)*np.exp((-gamma/2-1j*omega0)*np.maximum(t,0)),0j)

def spectrum(detuning,gamma=1.):
    if gamma<=0:raise ValueError('gamma')
    d=np.asarray(detuning,float)
    return gamma/(2*np.pi)/(d*d+(gamma/2)**2)

def spectral_amplitude(detuning,gamma=1.):
    if gamma<=0:raise ValueError('gamma')
    return np.sqrt(gamma/(2*np.pi))/(gamma/2-1j*np.asarray(detuning,float))

def pulse_overlap(gamma1,gamma2,frequency_difference=0.,onset_difference=0.):
    g1,g2=float(gamma1),float(gamma2)
    if g1<=0 or g2<=0:raise ValueError('gamma')
    d=float(onset_difference);dw=float(frequency_difference)
    a=(g1+g2)/2+1j*dw
    return complex(np.sqrt(g1*g2)*np.exp((g2/2+1j*dw)*d-a*max(0.,d))/a)

def overlap_probability(gamma1,gamma2,frequency_difference=0.,onset_difference=0.):
    return float(abs(pulse_overlap(gamma1,gamma2,frequency_difference,onset_difference))**2)

def finite_reservoir(gamma=1.,bandwidth=12.,modes=401):
    if gamma<=0 or bandwidth<=0 or not isinstance(modes,int) or modes<3 or modes%2==0:
        raise ValueError('gamma, bandwidth, odd modes')
    det=np.linspace(-bandwidth,bandwidth,modes)
    spacing=det[1]-det[0]
    g=np.full(modes,np.sqrt(gamma*spacing/(2*np.pi)))
    ids=np.arange(1,modes+1)
    rows=np.r_[np.arange(modes+1),np.zeros(modes,int),ids]
    cols=np.r_[np.arange(modes+1),ids,np.zeros(modes,int)]
    data=np.r_[0.,det,g,g]
    h=csr_matrix((data,(rows,cols)),shape=(modes+1,modes+1),dtype=complex)
    return h,det,g

def finite_evolution(times,gamma=1.,bandwidth=12.,modes=401):
    t=np.asarray(times,float)
    if t.ndim!=1 or len(t)<2 or t[0]!=0 or np.any(np.diff(t)<=0) or not np.allclose(np.diff(t),t[1]-t[0]):
        raise ValueError('uniform increasing times beginning at zero required')
    h,det,g=finite_reservoir(gamma,bandwidth,modes)
    v=np.zeros(modes+1,complex);v[0]=1.
    psi=expm_multiply(-1j*h,v,start=0.,stop=float(t[-1]),num=len(t),endpoint=True,traceA=0.)
    return {'times':t,'atomic_amplitude':psi[:,0],
        'atomic_population':abs(psi[:,0])**2,
        'field_population':np.sum(abs(psi[:,1:])**2,axis=1),
        'mode_amplitudes_at_end':psi[-1,1:],
        'mode_detunings':det,'couplings':g,
        'total_norm':np.sum(abs(psi)**2,axis=1)}

def finite_early_curvature(gamma=1.,bandwidth=12.,modes=401):
    return float(sum(finite_reservoir(gamma,bandwidth,modes)[2]**2))

def compact_summary():
    t=np.linspace(0,8,81);out=finite_evolution(t)
    indices=[0,5,10,20,40,80]
    return {'version':'v0.92','gamma':1.,'bandwidth':12.,'modes':401,
      'frequency_grid_spacing':float(out['mode_detunings'][1]-out['mode_detunings'][0]),
      'early_curvature':finite_early_curvature(),
      'max_norm_error':float(np.max(abs(out['total_norm']-1))),
      'max_markov_population_abs_error_from_t_0_5':float(np.max(abs(out['atomic_population'][t>=.5]-excited_population(t[t>=.5])))),
      'time_rows':[{'time':float(t[i]),
          'finite_atomic_population':float(out['atomic_population'][i]),
          'finite_field_population':float(out['field_population'][i]),
          'markov_atomic_population':float(excited_population(t[i]))} for i in indices],
      'lorentzian_fwhm':1.,
      'temporal_mean_emission_time':1.,
      'overlap_dw_gamma':overlap_probability(1,1,1),
      'overlap_identical':overlap_probability(1,1),
      'different_width_overlap':overlap_probability(1,2),
      'early_time_markov_slope':-1.,
      'early_time_closed_unitary_slope':0.,
      'interpretation':'Standard emitter-field unitary dynamics; no historical photon identity label observed.'}

if __name__=='__main__':
    import json
    print(json.dumps(compact_summary(),indent=2))
