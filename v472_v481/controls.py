"""Operational controls for polarization, calibration, and optical storage."""
import numpy as np
from scipy.optimize import linprog

SEED = 472482


def resolved_jones():
    """Resolve a coherently populated ordinary mode rather than trace it."""
    c = .37*np.exp(.49j)
    isometry = np.array([[1,0],[0,c],[0,0],[0,np.sqrt(1-abs(c)**2)]])
    rng = np.random.default_rng(SEED)
    states = rng.normal(size=(64,2)) + 1j*rng.normal(size=(64,2))
    states /= np.linalg.norm(states,axis=1,keepdims=True)
    reduced_error, restored_error = 0., 0.
    for state in states:
        rho = np.outer(state,state.conj())
        joint = (isometry@state).reshape(2,2)
        expected = rho*np.array([[1,c.conjugate()],[c,1]])
        reduced_error = max(reduced_error,np.max(abs(joint.T@joint.conj()-expected)))
        for sign in (1,-1):
            conditional = (joint[0]+sign*joint[1])/np.sqrt(2)
            a = c+sign*np.sqrt(1-abs(c)**2)
            # Probability-weighted inversion would amplify; use a passive filter.
            recovered = np.diag([min(1,abs(a)),min(1,abs(a))/a])@conditional
            restored_error = max(restored_error,np.max(abs(np.outer(recovered,recovered.conj())-min(1,abs(a))**2*rho/2)))
    return dict(seed=SEED,inputs=len(states),reduced_error=float(reduced_error),
                filtered_inversion_error=float(restored_error), unfiltered_visibility=abs(c))


def polarization_transfer():
    # Unital CPTP isotropic preparation, detector contraction and depolarizing gate.
    gate_a, gate_b = .70,.90
    prep_a, read_a, read_b = .9,.8,.8
    prep_b = prep_a*read_a*gate_a/(read_b*gate_b)
    axes = np.vstack((np.eye(3),-np.eye(3)))
    single = (1+gate_a*prep_a*read_a*axes@axes.T)/2
    alternative = (1+gate_b*prep_b*read_b*axes@axes.T)/2
    # A matched-depth ratio cancels fixed SPAM when axes and idle are held fixed.
    two = (1+gate_a**2*prep_a*read_a*axes@axes.T)/2
    two_b = (1+gate_b**2*prep_b*read_b*axes@axes.T)/2
    ratio = (2*two[0,0]-1)/(2*single[0,0]-1)
    drift_read_b = read_b*gate_a/gate_b
    drift_fit = (1+gate_b**2*prep_b*drift_read_b*axes@axes.T)/2
    return dict(single_setting_pairs=single.size,single_depth_refit=float(np.max(abs(single-alternative))),
                depth_two_gap=float(np.max(abs(two-two_b))),depth_ratio=ratio,
                readout_drift_refit=float(np.max(abs(two-drift_fit))),drifting_readout=drift_read_b)


def multiport_reset():
    # If z = T x, the exact minimum ||T||_2 over unrestricted complex T is ||z||/||x||.
    x = np.array([.6,.8j])
    z = np.array([.078,.083j,.071])
    epsilon = .12
    best = np.outer(z,x.conj())/np.vdot(x,x)
    norm = float(np.linalg.norm(z)/np.linalg.norm(x))
    best_bounded = best*min(1,epsilon/norm)
    # Per-port limits can each hold even when the simultaneously calibrated budget fails.
    return dict(ports=len(z), max_port=float(np.max(abs(z))),calibrated_norm=epsilon,
                least_exact_refit_norm=norm,bounded_residual=float(np.linalg.norm(z-best_bounded@x)),
                exact_refit_error=float(np.linalg.norm(z-best@x)),
                ordinary_passive_slack=1-norm)


def flagged_history():
    # Dual-rail pure loss with equal transmissivity gives the qubit erasure channel.
    eta = .37
    identity = np.eye(2)
    kraus = np.zeros((3,3,2))
    kraus[0,:2,:] = np.sqrt(eta)*identity
    kraus[1:,2,:] = np.sqrt(1-eta)*identity
    def channel(rho):
        return sum(k@rho@k.T for k in kraus)
    rho0,rho1 = [channel(np.outer(x,x)) for x in identity]
    distinguish = np.sum(abs(np.linalg.eigvalsh(rho0-rho1)))/2
    # Eigenvalues of the joint reference-output state are eta, (1-eta)/2 twice.
    entropy = lambda p: -sum(x*np.log2(x) for x in p if x>0)
    coherent = entropy([eta/2,eta/2,1-eta])-entropy([eta,(1-eta)/2,(1-eta)/2])
    return dict(eta=eta,coherent_information=float(coherent),quantum_capacity=max(0,2*eta-1),
                history_trace_distance=float(distinguish),classical_capacity=eta,
                tp_error=float(np.max(abs(sum(k.T@k for k in kraus)-identity))))


def transported_contrast():
    # Device B reports counts in four randomized blocks. Missing shots have unknown outcomes.
    rng = np.random.default_rng(SEED+1)
    n = 500
    observed = rng.binomial(n,[.76,.72,.79,.75])
    positive = rng.binomial(observed,[.62,.61,.65,.66])
    low, high = positive/n,(positive+n-observed)/n
    weights = np.array([.1,.3,.4,.2])
    drift, prediction = .04,.75
    intervals = list(zip(np.maximum(low-drift,0),np.minimum(high+drift,1)))
    ends = []
    for direction in (1,-1):
        fit = linprog(direction*weights,bounds=intervals,method="highs")
        if not fit.success:
            raise RuntimeError(fit.message)
        ends.append(float(weights@fit.x))
    analytic = [float(weights@np.array(intervals)[:,i]) for i in (0,1)]
    return dict(seed=SEED+1,shots=4*n,observed=observed.tolist(),positive=positive.tolist(),
                complete_case=float(weights@(positive/observed)),prediction=prediction,
                identified_interval=ends,lp_error=float(np.max(abs(np.array(ends)-analytic))),
                exact_refit_error=abs(ends[0]+np.clip((prediction-ends[0])/(ends[1]-ends[0]),0,1)*(ends[1]-ends[0])-prediction))


def remote_lorentz():
    # Two damped oscillator tails plus a calibrated static offset (arbitrary frequency units).
    omega = np.linspace(.2,1.,301)
    poles = np.array([5.,8.])
    damping = np.array([.045,.08])
    response = 1/(poles**2-omega[:,None]**2-1j*omega[:,None]*damping)
    columns = np.column_stack((np.ones(len(omega)),response))
    target = columns@np.array([.011,.74,1.41])
    real_fit = linprog([0,1,1],A_ub=np.r_[columns.real,-columns.real],
                      b_ub=np.r_[target.real+1e-4,-target.real+1e-4],
                      bounds=[(0,.04),(0,None),(0,None)],method="highs")
    if not real_fit.success:
        raise RuntimeError(real_fit.message)
    ordinary = columns@real_fit.x
    absorption_ratio_bound = float(np.max(omega[:,None]*damping/(poles**2-omega[:,None]**2)))
    return dict(samples=len(omega),real_refit_error=float(np.max(abs(target.real-ordinary.real))),
                ordinary_max_imaginary=float(np.max(ordinary.imag)),
                analytic_ratio_bound=absorption_ratio_bound,
                target_imaginary_peak=float(np.max(target.imag)),
                exact_ordinary_strengths=[.011,.74,1.41])


def coherent_reemission():
    # Path r bypasses storage. Modes a (optical), b (material) exchange excitation.
    angle = np.pi/2
    swap = np.array([[1,0,0],[0,np.cos(angle),-1j*np.sin(angle)],[0,-1j*np.sin(angle),np.cos(angle)]])
    incoming = np.array([1,1,0])/np.sqrt(2)
    stored = swap@incoming
    phases = np.linspace(-np.pi,np.pi,129)
    retrieved = np.array([swap@np.diag([1,1,np.exp(1j*p)])@stored for p in phases])
    analyzer = np.array([1,1,0])/np.sqrt(2)
    fringe = abs(retrieved@analyzer)**2
    return dict(samples=len(phases),stored_arm_optical_population=abs(stored[1])**2,
                output_pop_variation=float(np.ptp(abs(retrieved[:,:2])**2,axis=0).max()),
                reference_fringe_span=float(np.ptp(fringe)),
                analytic_fringe_error=float(np.max(abs(fringe-(1-np.cos(phases))/2))),
                excitation_ledger_error=float(np.max(abs(np.sum(abs(retrieved)**2,axis=1)-1))))


def joint_quadrature():
    # One ordinary complex amplitude shared across calibration projections and signal.
    target = np.array([.095,.075])
    detector = np.array([.012,.013])
    # Measured loss accounting gives upper bound on ordinary coherent leakage power.
    energy_limit = .008
    # Closest point of the readout box to the origin is componentwise shrinkage.
    lowest = np.maximum(abs(target)-detector,0)
    needed = float(lowest@lowest)
    # Each marginal is feasible within the same power ball.
    return dict(quadratures=len(target),target=target.tolist(),readout_error=detector.tolist(),
                minimum_shared_power=needed,calibrated_power_bound=energy_limit,
                max_marginal_required_power=float(max(lowest**2)),
                critical_missing_power=max(0,needed-energy_limit))
