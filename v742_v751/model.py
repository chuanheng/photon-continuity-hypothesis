"""Windowed direction ratios under positive spectral reweighting."""
import json
import numpy as np
from scipy.optimize import brentq
from scipy.special import logsumexp
from v692_v701.model import AXES, MARKS
from v722_v731.model import mu

def spectrum(key, energy):
    x0,x1,e0,e1,y0,y1=AXES[key[:2]]
    x,y,*_=np.array(MARKS[key]).T
    nodes=e0+(x-x0)*(e1-e0)/(x1-x0)
    if min(energy)<min(nodes) or max(energy)>max(nodes):
        raise ValueError("outside marker support")
    values=10**(-2*(y-y0)/(y1-y0))*(100 if key.endswith('D2') else 1)
    return np.interp(energy,nodes,values)

def evaluate(n=2001):
    e=np.linspace(34.5,36.5,n)
    keys=list(MARKS)
    spectra=np.array([spectrum(k,e) for k in keys])
    signs=np.array([1,-1,-1,1])
    quad=np.ones(n);quad[[0,-1]]=.5
    def contrast(weights):
        return float(signs@logsumexp(np.log(spectra*quad)+weights,axis=1))
    base=contrast(np.zeros(n))
    x=e-35.5
    means=(spectra*quad)@x/(spectra@quad)
    slope=float(signs@means)
    step=.0001
    # Undo only the numerator material factor in Eq. (1), proportional to mu0+mu(E).
    corr=np.array([[mu(float(k.split('/')[0]))+mu(t) for t in e] for k in keys])
    directions=spectra[[1,3]]/spectra[[0,2]]
    hi,lo=directions
    return {
        'v7.42':{'published_groups':4,'monitor_cells_for_one_peak_per_line_arm_group':16},
        'v7.43':{'unweighted_log_cross':base,'constant_weight_log_cross':contrast(np.log(7.))},
        'v7.44':{'pivot_point_ratio':float(lo[n//2]/hi[n//2]),'integrated_ratio':float(np.exp(base))},
        'v7.45':{'arm_centroids_keV':(35.5+means).tolist(),'log_cross_derivative_keV':slope},
        'v7.46':{'finite_difference':(contrast(step*x)-contrast(-step*x))/(2*step),'analytic':slope},
        'v7.47':{'tilts_per_keV':[-1.,0.,1.],'cross_ratios':[float(np.exp(contrast(b*x))) for b in (-1.,0.,1.)]},
        'v7.48':{'original':base,'inverse_material_weight':contrast(-np.log(corr))},
        'v7.49':{'linewise_direction_ratio_ranges':[[float(min(z)),float(max(z))] for z in directions]},
        'v7.50':{'grid_cross_bounds':[float(min(lo)/max(hi)),float(max(lo)/min(hi))]},
        'v7.51':{'flattening_tilt_per_keV':float(brentq(lambda b: contrast(b*x),1,30)),
                 'weight_ratio_across_band':float(np.exp(2*brentq(lambda b: contrast(b*x),1,30)))}
    }
def run():
    return evaluate()
if __name__=='__main__':
    print(json.dumps(run(),indent=2))
