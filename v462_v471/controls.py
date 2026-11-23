"""Additional standard optical and statistical controls."""
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import linprog
from scipy.stats import binom

SEED = 462472


def rotating_wave():
    def trace(levels, coupling, counter_rotating):
        a = np.diag(np.sqrt(np.arange(1, levels)), 1)
        sigma_plus = np.array([[0,0],[1,0]])
        exchange = np.kron(a,sigma_plus)
        if counter_rotating:
            exchange = exchange + np.kron(a.T,sigma_plus)
        h = np.kron(np.diag(np.arange(levels)), np.eye(2))
        h += np.kron(np.eye(levels),np.diag([0.,1.]))
        h += coupling*(exchange+exchange.T)
        e,v = eigh(h)
        time = np.linspace(0,np.pi/coupling,141)
        states = (np.exp(-1j*time[:,None]*e)*v[2])@v.T
        return np.sum(abs(states[:,1::2])**2,axis=1), time

    errors, cutoff = [], []
    for g in (.02,.3):
        standard, t = trace(10,g,True)
        rwa, _ = trace(10,g,False)
        reduced, _ = trace(8,g,True)
        errors.append(float(max(abs(standard-rwa))))
        cutoff.append(float(max(abs(standard-reduced))))
    return {"rwa_gaps":errors, "cutoff_errors":cutoff,
            "rwa_formula_error":float(max(abs(rwa-np.sin(.3*t)**2)))}


def bell_bounds():
    x = np.array([[0,1],[1,0]])
    y = np.array([[0,-1j],[1j,0]])
    z = np.diag([1,-1])
    c = .6
    threshold = 1/np.sqrt(1+c*c)
    max_error, optimum = 0., []
    for p in (.8,.9,1.):
        density = np.array([[1,0,0,c],[0,0,0,0],[0,0,0,0],[c,0,0,1]])/2
        density = p*density+(1-p)*np.eye(4)/4
        corr = np.array([[np.trace(density@np.kron(a,b)).real for b in (x,y,z)]
                         for a in (x,y,z)])
        singulars = np.linalg.svd(corr,compute_uv=False)
        value = 2*np.linalg.norm(singulars[:2])
        beta = np.arctan(c)
        b1,b2 = np.cos(beta)*z+np.sin(beta)*x, np.cos(beta)*z-np.sin(beta)*x
        chsh = np.kron(z,b1+b2)+np.kron(x,b1-b2)
        max_error = max(max_error,abs(value-np.trace(density@chsh)))
        optimum.append(float(value))
    return {"visibility_threshold":float(threshold),"max_chsh":optimum,
            "explicit_setting_max_error":float(max_error)}


def environment_eraser():
    rng = np.random.default_rng(SEED)
    phases = rng.uniform(-np.pi,np.pi,32)
    rho = np.outer([1,0,0,1],[1,0,0,1])/2
    confusion = .12
    x = np.array([[0,1],[1,0]])
    outcomes = []
    for phi in phases:
        obs = np.array([[0,np.exp(-1j*phi)],[np.exp(1j*phi),0]])
        previous = (np.eye(2)+obs)/2
        outcomes.append([np.trace(rho@np.kron(previous,(np.eye(2)+s*(1-2*confusion)*x)/2)).real
                         for s in (1,-1)])
    joint = np.array(outcomes)
    cond_plus = 2*joint[:,0]
    error = max(abs(cond_plus-(1+.76*np.cos(phases))/2))
    return {"seed":SEED,"phases":len(phases),"conditional_visibility":.76,
            "conditional_error":float(error),"unconditional_error":float(max(abs(joint.sum(axis=1)-.5)))}


def allpass_delay():
    kappa = .74
    detuning = np.linspace(-3,3,12001)
    response = (detuning-1j*kappa)/(detuning+1j*kappa)
    derivatives = np.gradient(np.unwrap(np.angle(response)),detuning,edge_order=2)
    expected = 2*kappa/(detuning**2+kappa**2)
    extra_delay = .4
    composite = response*np.exp(1j*extra_delay*detuning)
    apparent = np.gradient(np.unwrap(np.angle(composite)),detuning,edge_order=2)
    return {"intensity_error":float(max(abs(abs(response)**2-1))),
            "center_group_delay":float(derivatives[len(detuning)//2]),
            "finite_difference_max_error":float(max(abs(derivatives-expected))),
            "untracked_reference_error":float(max(abs(apparent-derivatives-extra_delay)))}


def finite_reference():
    # Each block of total number n has the ordered basis |0,n>, |1,n-1>.
    rows = []
    for levels in (1,2,4,8):
        # A sine-state reference maximizes adjacent-mode overlap at fixed support.
        r = np.sqrt(2/(levels+1))*np.sin(np.pi*np.arange(1,levels+1)/(levels+1))
        blocks = np.column_stack((r[1:],r[:-1]))/np.sqrt(2)
        observed = float(2*np.sum(blocks[:,0]*blocks[:,1]))
        uniform = (levels-1)/levels
        bound = np.cos(np.pi/(levels+1))
        rows.append([levels,observed,uniform,float(bound)])
    return {"columns":["levels","measured","uniform","bound"],"results":rows}


def joint_null():
    # The columns are declared material, coherent bypass, and electronics response.
    ordinary = np.array([[1.,.5,0.],[.2,1.,0.],[0.,0.,1.]])
    target = np.array([.32,.29,.05])
    distances, refits = [], []
    for cap in (.22,.50):
        fit = linprog([0,0,0,1],A_ub=np.vstack((
            np.column_stack((np.vstack((ordinary,-ordinary)),-np.ones(6))),
            [1,1,0,0])),b_ub=np.r_[target,-target,cap],
            bounds=[(0,.35),(0,.35),(0,.10),(0,None)],method="highs")
        if not fit.success:
            raise RuntimeError(fit.message)
        distances.append(float(fit.fun))
        refits.append(fit.x[:3].tolist())
    # A positive linear combination of rows one and two equals w_M+w_C.
    dual = np.linalg.solve(ordinary[:2,:2].T,np.ones(2))
    lower = (dual@target[:2]-.22)/np.sum(abs(dual))
    return {"distance":distances,"fits":refits,"small_cap_dual_bound":float(lower)}


def heldout_design():
    # One-sided count test using simultaneous allocation across calibration and data.
    n,c = 4000,4000
    sub_alpha = .025
    p_cal,p_target = .30,.42
    drift = .015
    radii = np.sqrt(np.log(1/sub_alpha)/(2*np.array([n,c])))
    ref_counts = np.arange(c+1)
    limit = ref_counts/c+drift+sum(radii)
    critical = np.floor(n*limit).astype(int)
    calibration = binom.pmf(ref_counts,c,p_cal)
    rng = np.random.default_rng(SEED+1)
    calibrators = rng.binomial(c,p_cal,20000)
    trials = rng.binomial(n,p_target,20000)
    return {"seed":SEED+1,"per_arm_shots":n,"nominal_size_bound":2*sub_alpha,
            "exact_boundary_size":float(calibration@binom.sf(critical,n,p_cal+drift)),
            "exact_power":float(calibration@binom.sf(critical,n,p_target)),
            "nearby_power_at_0p355":float(calibration@binom.sf(critical,n,.355)),
            "simulated_power":float(np.mean(trials>critical[calibrators]))}


ROUNDS = dict(zip(("v4.65","v4.66","v4.67","v4.68","v4.69","v4.70","v4.71"),
                  (rotating_wave,bell_bounds,environment_eraser,allpass_delay,
                   finite_reference,joint_null,heldout_design),strict=True))
