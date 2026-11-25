"""Conditional design using deterministic background envelopes and Poisson counts."""
import json
from pathlib import Path
import numpy as np
from scipy.stats import poisson,norm
from scipy.optimize import brentq
from v622_v631.bounds import calculate

def design():
    bounds=calculate()
    root=Path(__file__).parent
    data=json.loads((root/'detector.json').read_text())[0]
    # Synthetic joint family: each incident photon sees one of two specified
    # response laws, and every interaction order shares that mixing fraction.
    lo,hi=data['total'][1:3]
    omitted=bounds['selected_order_ge4']+.5*bounds['below_floor_entry_ge4']
    n=2700000
    cap=hi+omitted
    crit=int(poisson.isf(.025,n*cap))+1
    target=brentq(lambda p:poisson.sf(crit-1,n*p)-.9,cap,1.)
    # Two-setting counts: foil mean = ordinary beam leakage + excess; blank
    # mean measures the same leakage with the independently known transmission.
    transmission=np.exp(-.277810274566*2.70*.1)
    leakage=norm.cdf(-4.)
    return dict(partial_response_mixture=[lo,hi],tail_allowance=omitted,
                conditional_total_cap=cap,exposure=n,critical_count=crit,
                power90_total_rate=target,increment_over_cap=target-cap,
                true_window_order4_bound=bounds['selected_order_ge4'],
                blank_expected_counts=n*leakage,foil_leakage_rate=transmission*leakage,
                blank_transfer_se=transmission*np.sqrt(leakage*(1-leakage)/n))
if __name__=='__main__':
    print(json.dumps(design(),indent=2))
