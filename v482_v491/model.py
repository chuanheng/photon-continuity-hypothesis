"""Ordinary optical memory controls with observable data and refits."""
import json

import numpy as np
from scipy.optimize import linprog


SEED = 482491


def flagged_bell():
    eta, visibility = .43,.58
    bell = np.array([1,0,0,1])/np.sqrt(2)
    projector = np.outer(bell,bell)
    success = eta*(visibility*projector+(1-visibility)*np.eye(4)/4)
    rho = np.zeros((2,3,2,3))
    rho[:,:2,:,:2] = success.reshape(2,2,2,2)
    rho[:,2,:,2] = (1-eta)*np.eye(2)/2
    pt = rho.swapaxes(0,2).reshape(6,6)
    eig = np.linalg.eigvalsh(pt)
    # Ordinary entanglement-breaking bound on herald-conditioned reference overlap.
    witness = float(bell@success@bell-eta/2)
    return dict(eta=eta,success_fidelity=float(bell@success@bell/eta),
                unnormalized_witness=witness,negativity=float(-eig[eig<0].sum()),
                trace_error=float(abs(np.trace(rho.reshape(6,6))-1)),
                allowed_false_herald_mass_for_arbitrary_bell=witness*2)


def multipair_threshold():
    efficiency = .8
    def coincidence(n):
        k = np.arange(n+1)
        return (1-(1-efficiency)**k)*(1-(1-efficiency)**(n-k))
    pair_far = np.array([.25,.5,.25])
    pair_near = np.array([.5,0,.5])
    four_far = np.array([1,4,6,4,1])/16
    four_near = np.array([.375,0,.25,0,.375])
    pair_rate, four_rate = .22,.024
    far = pair_rate*(pair_far@coincidence(2))+four_rate*(four_far@coincidence(4))
    near = pair_rate*(pair_near@coincidence(2))+four_rate*(four_near@coincidence(4))
    refit_pair_rate = far/(pair_far@coincidence(2))
    refit_overlap = 1-near/far
    four_detected_same_port = four_rate*(four_near[0]+four_near[-1])*efficiency**4
    fitted = np.array([refit_pair_rate*(pair_far@coincidence(2)),far*(1-refit_overlap)])
    return dict(coincidence_far=far,coincidence_near=near,refit_single_pair_rate=refit_pair_rate,
                refit_overlap=refit_overlap,threshold_refit_error=float(np.max(abs(fitted-[far,near]))),
                near_four_same_port_probability=four_detected_same_port)


def compressed_modes():
    rng = np.random.default_rng(SEED)
    # Orthogonal output modes with calibrated transmission amplitudes, including loss ports.
    amplitudes = np.array([.92,.79,.41,.12])
    unitary, _ = np.linalg.qr(rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)))
    k = unitary@np.diag(amplitudes)
    density = k@k.conj().T/4
    eig = np.linalg.eigvalsh(density)
    rank = 2
    optimum = float(eig[-rank:].sum())
    sampled = []
    for _ in range(128):
        basis,_ = np.linalg.qr(rng.normal(size=(4,rank))+1j*rng.normal(size=(4,rank)))
        sampled.append(float(np.trace(basis.conj().T@density@basis).real))
    # Continuous receiver with two resolved, matched output modes.
    matched = unitary[:,:rank]
    passive_error = k.conj().T@k+np.diag(1-amplitudes**2)-np.eye(4)
    return dict(seed=SEED,receiver_subspaces=len(sampled),rank=rank,optimum_detection=optimum,
                all_mode_detection=float(eig.sum()),best_random_detection=max(sampled),
                matched_detection=float(np.trace(matched.conj().T@density@matched).real),
                isometry_error=float(np.max(abs(passive_error))))


def echo_refit():
    theta, sigma = 1.3,.46
    def ou(t):
        return sigma**2*(theta*t-theta**2*(1-np.exp(-t/theta)))
    times = np.array([1,2])
    ramsey = ou(times)
    white, static = np.linalg.solve(np.column_stack((times,times**2)),ramsey)
    echo_ou = 4*ou(1)-ou(2)
    echo_white_static = white*2
    switches = np.array([0,.5,1.5,2])
    jumps = np.array([1,-2,2,-1])
    echo_two_ou = -sum(jumps[i]*jumps[j]*ou(switches[j]-switches[i])
                       for i in range(len(switches)) for j in range(i+1,len(switches)))
    # A numerical covariance integral independently checks the OU echo expression.
    n=600
    midpoint=(np.arange(n)+.5)*2/n
    sign=np.where((midpoint<.5)|(midpoint>1.5),1,-1)
    cov=sigma**2*np.exp(-abs(midpoint[:,None]-midpoint)/theta)
    integral=.5*(2/n)**2*(sign@cov@sign)
    return dict(grid=n,static=static,white=white,
                ramsey_error=float(np.max(abs(white*times+static*times**2-ramsey))),
                single_echo_gap=float(abs(np.exp(-echo_ou)-np.exp(-echo_white_static))),
                two_pulse_echo_gap=float(abs(np.exp(-echo_two_ou)-np.exp(-echo_white_static))),
                echo_integral_error=float(abs(integral-echo_two_ou)))


def correlated_reference():
    rng=np.random.default_rng(SEED+1)
    n=60000
    common=rng.normal(scale=.13,size=n)
    independent=rng.normal(scale=.2,size=(n,2))
    gain=np.array([.82,-.62])
    # A pulse rotates only reference polarity while material wait time stays fixed.
    same=common[:,None]*gain+independent
    flipped=same.copy()
    flipped[:,1]-=2*common*gain[1]
    observed=float(np.mean(same[:,0]*same[:,1]))
    reverse=float(np.mean(flipped[:,0]*flipped[:,1]))
    expected=float(np.prod(gain)*.13**2)
    monitored=same-common[:,None]*gain
    return dict(seed=SEED+1,shots=n,ordinary_expected_cross_moment=expected,
                observed_cross_moment=observed,reversed_cross_moment=reverse,
                monitor_subtracted_cross_moment=float(np.mean(np.prod(monitored,axis=1))),
                simulation_error=max(abs(observed-expected),abs(reverse+expected)))


def thermal_bunching():
    eta, environment = .62,.38
    background=(1-eta)*environment
    count=np.arange(64)
    thermal=background**count/(1+background)**(count+1)
    poisson=np.empty(len(count))
    poisson[0]=np.exp(-background)
    for n in count[1:]:
        poisson[n]=poisson[n-1]*background/n
    def moments(p):
        mean=float(count@p)
        return mean,float((count*(count-1))@p/mean**2)
    tmean,tg=moments(thermal)
    pmean,pg=moments(poisson)
    # An electronics-only geometric false-count register yields the same marginal.
    ordinary_register=(1/(1+background))*(background/(1+background))**count
    return dict(support=len(count),noise_mean=tmean,mean_refit_error=abs(tmean-pmean),
                thermal_g2=tg,poisson_g2=pg,
                optical_electronic_marginal_error=float(np.max(abs(ordinary_register-thermal))),
                two_detector_factorial_moment_50_50=background**2/2)


def excitation_ladder():
    g, gamma = .24,.04
    omega=np.linspace(-.8,.8,401)
    lorentz = lambda centers: (gamma**2/((omega[:,None]-centers)**2+gamma**2)).mean(axis=1)
    one=np.array([-g,g])
    linear=np.array([-2*g,0,2*g])
    jc=np.sqrt(2)*one
    # Equal state-dependent linewidths are a scoped comparison, not selection rules.
    observed=lorentz(jc)
    second_block=np.array([[0,g*np.sqrt(2)],[g*np.sqrt(2),0]])
    ordinary=lorentz(np.linalg.eigvalsh(second_block))
    return dict(spectral_samples=len(omega),one_excitation_gap=2*g,
                closest_line_change=float(np.min(abs(jc[:,None]-linear))),
                max_equal_lineweight_response_gap=float(np.max(abs(observed-lorentz(linear)))),
                ordinary_nonlinear_refit_error=float(np.max(abs(observed-ordinary))))


def jittered_delay():
    # Wrapped nearest-neighbor diffusion gives a stochastic jitter kernel.
    from scipy.linalg import expm
    bins=32
    shift=np.roll(np.eye(bins),1,axis=0)
    generator=(shift+shift.T)/2-np.eye(bins)
    duration=3.24
    matrix=expm(duration*generator)
    kernel=matrix[:,0]
    measured=np.roll(matrix,7,axis=0)
    analytic=np.sort(np.exp(duration*(np.cos(2*np.pi*np.arange(bins)/bins)-1)))[::-1]
    numeric=np.linalg.svd(measured,compute_uv=False)
    two_stage=expm(1.2*generator)@expm((duration-1.2)*generator)
    return dict(bins=bins,map_svd_error=float(np.max(abs(analytic-numeric))),
                observable_modes_at_floor=int(np.count_nonzero(numeric>.1)),
                optimum_bin_success=float(np.max(kernel)),
                split_jitter_refit_error=float(np.max(abs(measured-np.roll(two_stage,7,axis=0)))),
                eye_column_sum_error=float(np.max(abs(measured.sum(axis=0)-1))))


def reciprocity():
    # A circulator is a lossless ordinary nonreciprocal three-port network.
    s=np.roll(np.eye(3),1,axis=0)
    block=s[:2,:2]
    symmetric=(block+block.T)/2
    residual=float(np.linalg.norm(block-symmetric))
    # A reciprocal swap with asymmetric preparations/readout fits power contrasts
    # below unit contrast; with both directions calibrated it cannot fit.
    swap=np.array([[0.,1.],[1.,0.]])
    calibrated_observed=np.diag([.7,.83])@swap@np.diag([.8,.42])
    return dict(ports=3,full_unitarity_error=float(np.max(abs(s.T@s-np.eye(3)))),
                circulator_forward_power=block[1,0]**2,circulator_reverse_power=block[0,1]**2,
                best_reciprocal_frobenius_residual=residual,
                reciprocal_uncalibrated_power_gap=float(abs(calibrated_observed[0,1]**2-calibrated_observed[1,0]**2)))


def retained_process():
    # Vertices are full probability tables of passive common-cause polarization preparations.
    vertices=np.array([[.1,.4,.18],[.2,.6,.25],[.7,.7,.37],[.8,.3,.42]])
    train=np.array([.47,.52])
    measured_held=.65
    A=np.vstack((np.ones(len(vertices)),vertices[:,:2].T))
    def upper(table):
        matrix=np.vstack((np.ones(len(table)),table[:,:2].T))
        result=linprog(-table[:,2],A_eq=matrix,b_eq=np.r_[1,train],bounds=(0,None),method="highs")
        if not result.success:
            raise RuntimeError(result.message)
        return result
    fitted=upper(vertices)
    enlarged=np.vstack((vertices,np.r_[train,measured_held]))
    enlarged_fit=upper(enlarged)
    dual=fitted.eqlin.marginals
    return dict(vertices=len(vertices),held_observation=measured_held,restricted_prediction_max=-fitted.fun,
                primal_error=float(np.max(abs(A@fitted.x-np.r_[1,train]))),
                dual_slack_min=float(np.min(A.T@(-dual)-vertices[:,2])),
                dual_gap=float(abs(-fitted.fun+dual@np.r_[1,train])),
                extended_refit_error=float(abs(measured_held+enlarged_fit.fun)))


def run():
    models = (flagged_bell,multipair_threshold,compressed_modes,echo_refit,correlated_reference,
              thermal_bunching,excitation_ladder,jittered_delay,reciprocity,retained_process)
    return {f"v4.{version}":model() for version,model in enumerate(models,82)}


if __name__ == "__main__":
    print(json.dumps(run(),indent=2,allow_nan=False))
