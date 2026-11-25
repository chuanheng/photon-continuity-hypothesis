"""Expected normalized counts and conditional counterexamples. Lengths in cm."""
import json
from math import exp,log
from v722_v731.model import mu
from v702_v711.model import run as previous

def cross(values):
    a,b,c,d=values
    return log(a*d/(b*c))

def average_transmission(k,paths,weights):
    return sum(w*exp(-k*x) for w,x in zip(weights,paths))

def run():
    klo,khi=mu(54.612),mu(55.791)
    dm=klo-khi
    target=previous()['v7.02']['log_ratio']
    paths=(.001,.003)
    # First index is high energy, second detector varies fastest.
    entrance=[exp(-k*x) for k in (khi,klo) for x in paths]
    flux=[150.,210.,110.,190.]
    monitor=[f*t for f,t in zip(flux,entrance)]
    signal=[.2*m for m in monitor]
    mismatch=[exp(-k*x) for k in (khi,klo) for x in (.0,.001)]
    def ratio(k):
        return average_transmission(k,paths,(.8,.2))/average_transmission(k,paths,(.2,.8))
    # Same expected true monitor in four cells, additive background in one.
    polluted=[100.,100.,100.,100.*exp(target)]
    counts=[40.,160.]
    monitor_counts=[100.,200.]
    return dict(zip([f'v7.{i}' for i in range(32,42)],[
        {'per_flux_rates':[s/m for s,m in zip(signal,monitor)]},
        {'raw_entrance_log_cross':cross(entrance),'matched_log_cross':cross([s/m for s,m in zip(signal,monitor)])},
        {'net_log_cross':cross(mismatch),'required_double_path_difference_mm':10*target/dm},
        {'weighted_ratio_low':ratio(klo),'weighted_ratio_high':ratio(khi),'single_arm_log_residual':log(ratio(klo)/ratio(khi))},
        {'one_arm_log_bound':dm*(max(paths)-min(paths)),'two_arm_log_bound':2*dm*(max(paths)-min(paths))},
        {'one_cell_background_fraction':exp(target)-1,'normalized_log_bias':-cross(polluted)},
        {'pooled_ratio':sum(counts)/sum(monitor_counts),'equal_block_mean':sum(c/m for c,m in zip(counts,monitor_counts))/2},
        {'independent_log_variance':1/100+1/1000,'subset_log_variance':1/100-1/1000},
        {'monitor_low':exp(-target),'equal_signal_log_ratio':cross([1.,1.,1.,exp(target)])},
        {'raw_log_cross':cross(signal),'monitor_log_cross':cross(monitor),
         'normalized_log_cross':cross(signal)-cross(monitor),'target_log_cross':target}
    ]))
if __name__=='__main__':
    print(json.dumps(run(),indent=2))
