"""Restricted planar photon transport and conditional recoil readout examples."""
from math import cos, exp, log, radians
import json
from scipy.special import ndtr
from scipy.optimize import brentq
from v702_v711.model import run as prior

def mu(e):
    """Ge linear attenuation per cm; log-log interpolation of NIST table."""
    grid = [(30,13.85),(40,6.207),(50,3.335),(60,2.023)]
    for (x,a),(y,b) in zip(grid,grid[1:]):
        if x <= e <= y:
            return 5.323*a*exp(log(b/a)*log(e/x)/log(y/x))
    raise ValueError("energy outside tabulated interval")

def run():
    lo,hi = 54.612,55.791
    c = prior()['v7.02']['log_ratio']
    dm = mu(lo)-mu(hi)
    d = c/dm
    theta = radians(38.84)
    # For an E' photon returning through both front layers, the summed path
    # does not change when the detectors exchange roles at normal incidence.
    paths = [.001,.003]
    def ray(e,i):
        return exp(-mu(e)*paths[i]-mu(35.5)*sum(paths))
    ray_ratio = ray(lo,0)*ray(hi,1)/(ray(lo,1)*ray(hi,0))
    # Hypothetical recoil charge collection fraction q, not X-ray attenuation.
    e1,e2 = lo-35.5,hi-35.5
    def gate(q,e):
        return ndtr((q*e-8)/.5)
    def response(q):
        return log(gate(q,e2)/gate(q,e1))
    q = brentq(lambda q:response(q)-c,.38,.55)
    return dict(zip([f'v7.{i}' for i in range(22,32)],[
        {'active_mm':13,'published_area_mm2':200},
        {'mu_low_cm_inverse':mu(lo),'mu_high_cm_inverse':mu(hi),'difference':dm},
        {'illustrative_depth_difference_um':20,'ray_cross_ratio':ray_ratio},
        {'required_normal_path_difference_mm':10*d,'thin_10um_abs_log_ratio':dm*.001},
        {'secant':1/cos(theta),'required_thickness_difference_mm_common_angle':10*d*cos(theta)},
        {'transmission_extra_path_lo':exp(-mu(lo)*d),'transmission_extra_path_hi':exp(-mu(hi)*d)},
        {'scattered_mu_span_cm_inverse':mu(34.5)-mu(36.5),'log_span_for_total_40um':.004*(mu(34.5)-mu(36.5))},
        {'recoil_keV':[e1,e2],'full_collection_trigger':[float(gate(1,e1)),float(gate(1,e2))]},
        {'toy_charge_fraction':q,'trigger_probabilities':[float(gate(q,e1)),float(gate(q,e2))],
         'sum_deficits_keV':[(1-q)*e1,(1-q)*e2]},
        {'max_loss_fraction_for_half_keV_gate':[.5/e1,.5/e2],'toy_deficit_min_keV':(1-q)*e1}
    ]))
if __name__=='__main__':
    print(json.dumps(run(),indent=2))
