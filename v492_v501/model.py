"""Tests of operational criteria for an identifiable carrier."""
from itertools import permutations
import json

import numpy as np

SEED = 492501


def phase_reference():
    states = [np.kron([1,s],[1,1])/2 for s in (1,-1)]
    charges = np.array([0,1,1,2])
    preserve = charges[:,None]==charges
    # Average a uniform common phase, or independently randomize the two pulses.
    common = [np.outer(state,state)*preserve for state in states]
    independent = [np.diag(np.diag(state)) for state in common]
    trace_dist = lambda left,right: np.sum(abs(np.linalg.eigvalsh(left-right)))/2
    detector = np.array([0,1,1,0])/np.sqrt(2)
    marginals = [np.trace(state.reshape(2,2,2,2),axis1=1,axis2=3) for state in common]
    rng=np.random.default_rng(SEED)
    phase_noise=rng.normal(scale=.4,size=65536)
    predicted=.5*np.exp(-.4**2/2)
    prob_delta=.5*np.mean(np.cos(phase_noise))
    return dict(seed=SEED,shots=len(phase_noise),
                single_mode_distinguishability=float(trace_dist(*marginals)),
                independent_distance=float(trace_dist(*independent)),
                common_distance=float(trace_dist(*common)),
                beam_splitter_probability_gap=float(detector@(common[0]-common[1])@detector),
                relative_jitter_gap=float(prob_delta),gaussian_mc_error=float(abs(prob_delta-predicted)))


def thermal_reset():
    beta, gap, p = 2.2, .9, .81
    q=1/(1+np.exp(beta*gap))
    labels=np.array([0.,gap])
    rho_in=np.diag([1-p,p])
    bath=np.diag([1-q,q])
    swap=np.eye(4)[[0,2,1,3],:]
    initial=np.kron(rho_in,bath)
    final=swap@initial@swap.T
    system=np.trace(final.reshape(2,2,2,2),axis1=1,axis2=3)
    environment=np.trace(final.reshape(2,2,2,2),axis1=0,axis2=2)
    heat=float(labels@np.diag(environment-bath))
    removed=float(labels@np.diag(rho_in-system))
    entropy=lambda r: -r*np.log(r)-(1-r)*np.log(1-r)
    relative=p*np.log(p/q)+(1-p)*np.log((1-p)/(1-q))
    return dict(reset_error=q,heat=heat,system_energy_removed=removed,
                entropy_decrease=float(entropy(p)-entropy(q)),
                landauer_excess=float(beta*heat-entropy(p)+entropy(q)),
                ledger_error=abs(heat-removed),
                identity_error=float(abs(beta*heat-entropy(p)+entropy(q)-relative)))


def triad_bunching():
    r=.38
    perms=list(permutations(range(3)))
    out=[]
    max_error=0.
    for phase in (0.,np.pi):
        gram=np.array([[1,r,r*np.exp(-1j*phase)],[r,1,r],[r*np.exp(1j*phase),r,1]])
        vectors=np.linalg.cholesky(gram).conj()
        component=np.zeros(27,dtype=complex)
        for i,j,k in perms:
            component+=np.kron(np.kron(vectors[i],vectors[j]),vectors[k])
        numerical=float(np.vdot(component,component).real/(6*27))
        permanent=sum(np.prod(gram[np.arange(3),perm]) for perm in perms)
        analytic=(1+3*r*r+2*r**3*np.cos(phase))/27
        max_error=max(max_error,abs(numerical-analytic),abs(permanent/27-analytic))
        out.append(numerical)
    return dict(pair_overlap_squared=r*r,all_same_port_probabilities=out,
                triad_gap=abs(out[0]-out[1]),max_tensor_formula_error=float(max_error))


def coupled_internal_mode():
    # Two internal optical modes and two material modes; number-conserving exchange.
    from scipy.linalg import expm
    g, split, dwell = .44,.36,1.7
    identity=np.eye(2)
    coupling=np.kron(np.array([[0,1],[1,0]]),identity)*g
    mixing=np.zeros((4,4))
    mixing[2:,2:]=split*np.array([[0,1],[1,0]])
    transfer=expm(-1j*coupling*np.pi/(2*g))
    unitary=transfer@expm(-1j*dwell*mixing)@transfer
    excitation=unitary@np.array([1,0,0,0])
    ordinary=np.array([-np.cos(split*dwell),1j*np.sin(split*dwell)])
    pair=np.kron(excitation[:2],excitation[:2]).reshape(2,2)
    probabilities=np.array([abs(pair[0,0])**2,abs(pair[0,1])**2+abs(pair[1,0])**2,abs(pair[1,1])**2])
    p=float(abs(ordinary[1])**2)
    pair_error=float(np.max(abs(probabilities-[(1-p)**2,2*p*(1-p),p*p])))
    return dict(internal_modes=2,two_boson_count_fit_error=pair_error,cross_mode_probability=float(abs(excitation[1])**2),
                normal_mode_fit_error=float(np.max(abs(excitation[:2]-ordinary))),
                residual_material_population=float(np.linalg.norm(excitation[2:])**2),
                joint_unitarity_error=float(np.max(abs(unitary.conj().T@unitary-np.eye(4)))))


def boosted_dwell():
    # Natural units c=1. Wave travels along +x. Interactions take place at the same
    # material coordinate, so their separation is timelike in both frames.
    beta=np.linspace(-.84,.84,101)
    gamma=1/np.sqrt(1-beta**2)
    dwell, frequency=1.6,2.3
    dt=gamma*dwell
    dx=-gamma*beta*dwell
    doppler=gamma*(1-beta)*frequency
    phase=doppler*(dt-dx)
    rest=frequency*dwell
    naive=doppler*dt
    return dict(boost_count=len(beta),minimum_interval_squared=float(np.min(dt**2-dx**2)),
                invariant_phase_error=float(np.max(abs(phase-rest))),
                naive_max_phase_error=float(np.max(abs(naive-rest))),
                proper_time_error=float(np.max(abs(np.sqrt(dt**2-dx**2)-dwell))))


def finite_clock():
    # Number shift compensates a one-quantum operation on the system.
    levels=12
    shift=np.diag(np.ones(levels-1),1)
    phase=np.linspace(0,2*np.pi,65)
    theta=np.pi/(levels+1)
    optimum=np.sin(theta*np.arange(1,levels+1))*np.sqrt(2/(levels+1))
    radius=max(np.linalg.eigvalsh((np.exp(-1j*f)*shift+np.exp(1j*f)*shift.T)/2)[-1] for f in phase)
    check=float(optimum@shift@optimum)
    flat=np.ones(levels)/np.sqrt(levels)
    return dict(levels=levels,quadrature_phases=len(phase),tight_visibility=float(np.cos(theta)),
                tightness_error=float(max(abs(radius-np.cos(theta)),abs(check-np.cos(theta)))),
                flat_visibility=float(flat@shift@flat))


def reverse_loss():
    # Petz recovery of a full rank reference through single-rail pure loss.
    eta=.59
    kraus=[np.diag([1,np.sqrt(eta)]),np.array([[0,np.sqrt(1-eta)],[0,0]])]
    def loss(x):
        return sum(k@x@k.T for k in kraus)
    sigma=np.diag([.6,.4])
    output=loss(sigma)
    sqrt_sigma=np.diag(np.sqrt(np.diag(sigma)))
    inverse_output=np.diag(1/np.sqrt(np.diag(output)))
    recovery=[sqrt_sigma@k.T@inverse_output for k in kraus]
    def roundtrip(x):
        return sum(r@loss(x)@r.T for r in recovery)
    pair=[np.diag([1.,0.]),np.diag([0.,1.])]
    difference=roundtrip(pair[0])-roundtrip(pair[1])
    return dict(eta=eta,reference_error=float(np.max(abs(roundtrip(sigma)-sigma))),
                recovery_tp_error=float(np.max(abs(sum(r.T@r for r in recovery)-np.eye(2)))),
                post_loss_trace_distance=eta,
                post_recovery_trace_distance=float(np.sum(abs(np.linalg.eigvalsh(difference)))/2))


def common_controller():
    # Independent preparations X,Y. Readout Q is a noisy shared parity monitor.
    fidelity=.9
    table=np.array([[(fidelity if (i^j)==q else 1-fidelity)/4
                     for q in range(2)] for i in range(2) for j in range(2)]).reshape(2,2,2)
    joint=table.sum(axis=2)
    xq=table.sum(axis=1,keepdims=True)
    yq=table.sum(axis=0,keepdims=True)
    q=table.sum(axis=(0,1),keepdims=True)
    mutual=lambda probability,product: float(np.sum(probability*np.log2(probability/product)))
    conditional=mutual(table,xq*yq/q)
    entropy=-fidelity*np.log2(fidelity)-(1-fidelity)*np.log2(1-fidelity)
    return dict(branch_mutual_information=mutual(joint,joint.sum(axis=0)*joint.sum(axis=1)[:,None]),
                conditional_mutual_information=conditional,parity_accuracy=fidelity,
                entropy_formula_error=abs(conditional-(1-entropy)))


def band_completion():
    n,time_support,band_bins=32,8,5
    row=np.arange(n)[:,None]
    col=np.arange(time_support)
    fourier=np.exp(-2j*np.pi*row*col/n)/np.sqrt(n)
    measured=np.r_[0:3,30:32]
    observed=fourier[measured]
    _,_,right=np.linalg.svd(observed,full_matrices=True)
    hidden=right[-1].conj()
    candidate=fourier@hidden
    out_of_band=np.delete(candidate,measured)
    return dict(grid=n,time_support=time_support,measured_bins=band_bins,null_dimension=int(time_support-np.linalg.matrix_rank(observed)),
                in_band_refit_error=float(np.linalg.norm(candidate[measured])),
                omitted_band_energy=float(np.linalg.norm(out_of_band)**2),
                full_energy_error=float(abs(np.linalg.norm(candidate)**2-1)))


def sourced_scalar():
    # Outgoing three-dimensional Helmholtz Green function, natural units.
    m=.78
    omega=np.array([.55,1.1])
    radius=np.linspace(1,5,81)
    k=np.sqrt(omega**2-m*m+0j)
    scalar=np.exp(1j*k[:,None]*radius)/(4*np.pi*radius)
    # A conventional lossless gapped wave equation for a scalar readout has the
    # same propagator; neither propagator tells us what made the source.
    transfer=np.empty_like(scalar)
    transfer[0]=np.exp(-np.sqrt(m*m-omega[0]**2)*radius)/(4*np.pi*radius)
    transfer[1]=(np.cos(k[1].real*radius)+1j*np.sin(k[1].real*radius))/(4*np.pi*radius)
    invariant=lambda e,b: 2*(b*b-e*e)
    return dict(radii=len(radius),frequency_count=len(omega),plane_wave_source=invariant(1,1),
                standing_antinode_source=invariant(2,0),ordinary_gapped_refit_error=float(np.max(abs(scalar-transfer))),
                far_near_scaled_ratio=float(abs(scalar[0,-1]*radius[-1]/(scalar[0,0]*radius[0]))))


def run():
    models=(phase_reference,thermal_reset,triad_bunching,coupled_internal_mode,boosted_dwell,finite_clock,
            reverse_loss,common_controller,band_completion,sourced_scalar)
    versions=[f"v4.{i}" for i in range(92,100)]+["v5.00","v5.01"]
    return {version:model() for version,model in zip(versions,models)}


if __name__=="__main__":
    print(json.dumps(run(),indent=2,allow_nan=False))
