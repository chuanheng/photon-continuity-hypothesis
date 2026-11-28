"""Passive analysis of a two-boson symmetric state; calibrated output modes."""
import json
import numpy as np
from v1162_v1171.model import state


def amplitudes(vector):
    a,b,c = vector
    return np.array([[a,b/np.sqrt(2)],[b/np.sqrt(2),c]])


def count_probabilities(vector, angle, phase):
    cs,sn = np.cos(angle),np.sin(angle)*np.exp(1j*phase)
    u = np.array([[cs,sn],[-sn.conjugate(),cs]])
    out = u@amplitudes(vector)@u.T
    return abs(np.array([out[0,0],np.sqrt(2)*out[0,1],out[1,1]]))**2


def effects(angle, phase):
    cs, sn = np.cos(angle), np.sin(angle)*np.exp(1j*phase)
    row = np.array([cs**2, np.sqrt(2)*cs*sn, sn**2])
    return np.outer(row.conj(),row)


def dual_frame(angles, phases):
    matrices = [effects(a,p) for a in angles for p in phases]
    return np.stack([m.T.reshape(-1) for m in matrices])


def run():
    target = np.array([1.,1.,0.])/np.sqrt(2)
    singular = np.linalg.svd(amplitudes(target),compute_uv=False)
    plus,minus = [state(u,.4) for u in (8.,-8.)]
    counts = [count_probabilities(v,np.pi/4,0) for v in (plus,minus)]
    phases = 2*np.pi*np.arange(8)/8
    counts_by_phase = [count_probabilities(plus,np.pi/4,p)[0] for p in phases]
    harmonic = np.mean(np.array(counts_by_phase)*np.exp(-2j*phases))
    # Mis-setting by pi flips the sign on the odd-occupation amplitude.
    angle = .33
    shifted = [count_probabilities(plus,angle,np.pi-p) for p in phases]
    minus_table = [count_probabilities(minus,angle,p) for p in phases]
    flat = dual_frame([np.pi/4], phases)
    # Any matrix reconstructed by linear inversion is validated on an unseen angle.
    frame = dual_frame([0,.3,.65,1.05,np.pi/2], phases)
    rho = np.outer(plus,plus.conjugate())
    # Generate measurement data by Fock amplitudes independently of the Born design.
    observations = [count_probabilities(plus,a,p)[0] for a in [0,.3,.65,1.05,np.pi/2] for p in phases]
    recovered = np.linalg.lstsq(frame,observations,rcond=None)[0].reshape(3,3)
    holdout = abs(np.trace(effects(.51,.72)@recovered)-count_probabilities(plus,.51,.72)[0])
    # Threshold detectors count any nonempty port. Uniform loss is independent.
    double, split, other = counts[0]
    eta = .76
    click = double*(1-(1-eta)**2)+split*eta
    both = split*eta**2
    inferred = (click-both/eta)/(eta*(2-eta))
    # Dark-click OR map on four ideal binary patterns.
    d = .025
    detector = np.array([[1-d,0],[d,1]])
    ideal_patterns = np.array([0.,other,double,split])
    noisy = np.kron(detector,detector)@ideal_patterns
    # Phase jitter attenuates harmonic m by exp(-m² sigma²/2).
    from numpy.polynomial.hermite import hermgauss
    nodes,weights = hermgauss(24)
    sigma = .35
    smeared = [sum(w*count_probabilities(plus,np.pi/4,p+np.sqrt(2)*sigma*x)[0]
                   for w,x in zip(weights,nodes))/np.sqrt(np.pi) for p in phases]
    attenuation = abs(np.mean(smeared*np.exp(-2j*phases))/harmonic)
    # A trusted calibration state's complex first harmonic fixes the reflection
    # ambiguity. Pure imaginary coherence alone is invariant under pi-phi.
    reference = np.array([1.,1.,0.])/np.sqrt(2)
    ref = [count_probabilities(reference,angle,p)[0] for p in phases]
    mirror = [count_probabilities(reference,angle,np.pi-p)[0] for p in phases]
    return {'balanced_rank':int(np.linalg.matrix_rank(flat)),
            'tomography':[int(np.linalg.matrix_rank(frame)),float(holdout),float(np.max(abs(recovered-rho)))],
            'threshold_loss':[float(click),float(both),float(inferred)],
            'dark_clicks':[float(noisy[-1]),float(ideal_patterns[-1]),float(np.linalg.cond(np.kron(detector,detector)))],
            'jitter':float(attenuation),'reference':float(np.max(abs(np.array(ref)-mirror))),
            'orbit': {'double_max':float(singular[0]**2),'split_max':float(sum(singular)**2/2)},
            'balanced':[c.tolist() for c in counts],
            'phase_refit':float(np.max(abs(np.array(shifted)-minus_table))),
            'second_harmonic':[float(harmonic.real),float(harmonic.imag),
                               float(abs(4*harmonic-plus[0].conjugate()*plus[2]))]}


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
