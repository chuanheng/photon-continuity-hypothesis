"""Gauge, polarization and cavity tests at a partial research checkpoint."""
import json

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import linprog

SEED = 462471


def gauge_probe():
    rng = np.random.default_rng(SEED)
    metric = np.diag([1, -1, -1, -1])
    field_errors, conserved_errors, bare_changes = [], [], []
    for direction in rng.normal(size=(64,3)):
        unit = direction/np.linalg.norm(direction)
        k = np.r_[1,unit]
        tangent = np.cross(unit,[0,0,1])
        polarization = np.r_[0,tangent/np.linalg.norm(tangent)]
        displaced = polarization + .7*k
        # A Fourier component of F, up to the common factor i.
        field = lambda eps: np.outer(k,eps)-np.outer(eps,k)
        field_errors.append(np.max(abs(field(displaced)-field(polarization))))
        # j·k=0 for j proportional to the transverse polarization.
        conserved_errors.append(abs(polarization@metric@(displaced-polarization)))
        t = np.array([1,0,0,0])
        bare_changes.append(t@metric@(displaced-polarization))
    return {"seed":SEED,"trials":64,"field_max_gauge_error":float(max(field_errors)),
            "conserved_current_max_gauge_error":float(max(conserved_errors)),
            "bare_timelike_current_min_change":float(min(bare_changes))}


def rotation_fit():
    # Homogeneous pseudoscalar derivative. The helicity splitting is real
    # on the chosen eikonal domain k > |g dot(a)|.
    k = np.linspace(.75,1.4,11)
    change_rate, duration = .004, 10.0
    splitting = np.sqrt(k*k+change_rate*k)-np.sqrt(k*k-change_rate*k)
    rotation = duration*splitting/2
    eikonal = duration*change_rate/2
    design = np.column_stack((np.ones_like(k),k**-2))
    residuals = []
    for cap in (.008,.05):
        contra = np.column_stack((np.vstack((design,-design)),-np.ones(2*len(k))))
        lp = linprog([0,0,1],A_ub=contra,b_ub=np.r_[rotation,-rotation],
                     bounds=[(-cap,cap),(-.08,.08),(0,None)],method="highs")
        if not lp.success:
            raise RuntimeError(lp.message)
        residuals.append(float(max(abs(design@lp.x[:2]-rotation))))
    # Faraday-only endpoint bound for a perfectly constant angle with a capped offset.
    r = k[[0,-1]]**-2
    lower = max(0,eikonal-.008)*(r[0]-r[1])/sum(r)
    detuning_error = float(max(abs(rotation-eikonal)))
    return {"frequencies":len(k),"eikonal_angle_rad":eikonal,
            "eikonal_max_error_rad":detuning_error,
            "calibrated_max_residual_rad":residuals[0],
            "free_offset_max_residual_rad":residuals[1],
            "certified_calibrated_lower_bound_rad":float(lower-detuning_error)}


def cavity_ledger():
    # Vacuum input, one stored excitation, constant passive Markov decay rates.
    kappa_out, kappa_internal, horizon = .7,.3,8.
    def ode(_, state):
        population = state[0]
        return [-(kappa_out+kappa_internal)*population,kappa_out*population,
                kappa_internal*population]
    sim = solve_ivp(ode,(0,horizon),[1,0,0],rtol=1e-11,atol=1e-13,dense_output=True)
    if not sim.success:
        raise RuntimeError(sim.message)
    time = np.linspace(0,horizon,81)
    actual = sim.sol(time)
    retained = np.exp(-(kappa_out+kappa_internal)*time)
    released = 1-retained
    theory = np.vstack((retained,kappa_out*released,kappa_internal*released))
    return {"time_end":horizon,"grid_points":len(time),
            "final_probabilities_stored_out_internal":actual[:,-1].tolist(),
            "ledger_max_error":float(max(abs(actual.sum(axis=0)-1))),
            "ode_closed_form_error":float(np.max(abs(actual-theory)))}


def run():
    return {"v4.62":gauge_probe(),"v4.63":rotation_fit(),"v4.64":cavity_ledger()}


if __name__ == "__main__":
    print(json.dumps(run(),indent=2,allow_nan=False))
