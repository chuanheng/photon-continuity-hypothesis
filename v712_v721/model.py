"""Deterministic calibration design calculations, not additional measurements."""
import json
from math import ceil, exp, log, sqrt
from statistics import NormalDist
from v702_v711.model import run as previous

def run():
    prior = previous()
    contrast = prior['v7.02']['log_ratio']
    sigma = prior['v7.06']['independent_log_sd']
    lines = [54.612, 55.791, 59.537, 86.5]
    half_gap = (lines[1]-lines[0])/2
    intercept = (lines[1]+lines[0])/2
    ref = lines[2]
    # A linear ordinary log response vanishing at the external reference.
    slope = contrast/(lines[0]-lines[1])
    gains = [slope*(e-ref) for e in lines]
    # Two high-energy anchors: a quadratic perturbation vanishes at both.
    basis = [(e-ref)*(e-lines[3]) for e in lines]
    curvature = contrast/(basis[0]-basis[1])
    z = NormalDist().inv_cdf(.975)
    target = contrast/(z+NormalDist().inv_cdf(.8))
    ref_counts = ceil(4/.05**2)
    # ABBA science/reference acquisition cancels constant and linear temporal drift.
    times = [-1.5,-.5,.5,1.5]
    abba = [.5,-.5,-.5,.5]
    drift = [sum(w*t**power for w,t in zip(abba,times)) for power in range(3)]
    return {
        'v7.12': {'recoil_windows_keV':[[e-36.5,e-34.5] for e in lines]},
        'v7.13': {'common_efficiency_product':.93*.98,'log_cross_contribution':0.},
        'v7.14': {'slope_per_keV':slope,'ordinary_log_gains':gains},
        'v7.15': {'quadratic_per_keV2':curvature,'ordinary_log_gains':[curvature*x for x in basis]},
        'v7.16': {'center_keV':intercept,'half_gap_keV':half_gap,'required_log_slope_abs':abs(slope)},
        'v7.17': {'equal_reference_counts_per_cell':ref_counts,'reference_log_sd':sqrt(4/ref_counts)},
        'v7.18': {'science_log_sd':sigma,'combined_log_sd':sqrt(sigma**2+.05**2)},
        'v7.19': {'target_total_log_sd':target,'science_exposure_multiplier':sigma**2/(target**2-.05**2)},
        'v7.20': {'abba_drift_moments':drift,'quadratic_drift_to_mimic':contrast/drift[2]},
        'v7.21': {'swap_odd_if_stable':((contrast)-(-contrast))/2,
                   'ordinary_odd_counterexample':[contrast,-contrast], 'odd_null_reference_corrected': ((contrast-.1)-(-contrast+.1))/2}
    }

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
