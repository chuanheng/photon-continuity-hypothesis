"""Gain invariants for the common-window germanium measurements."""
import json
import numpy as np
from v692_v701.model import summarize

def run():
    keys = ['55.791/D1','55.791/D2','54.612/D1','54.612/D2']
    def values(band):
        return np.array([summarize(k,band)['mean'] for k in keys])
    y = values((34.5,36.5))
    signs = np.array([1.,-1.,-1.,1.])
    def contrast(z):
        return float(signs@np.log(z))
    c = contrast(y)
    gain = np.array([2.,3.,10.,15.])
    # Separable line and detector log gains span a three-dimensional subspace.
    design = np.array([[1,0,0],[1,0,1],[1,1,0],[1,1,1.]])
    beta = np.linalg.lstsq(design,np.log(y),rcond=None)[0]
    residual = np.log(y)-design@beta
    relative = np.array([summarize(k)['independent'] for k in keys])/y
    paired_amp = relative.reshape(2,2)
    # Independent lines, fixed within-line correlation rho; delta method.
    def pair_sd(rho):
        return float(np.sqrt(np.sum(relative**2)-2*rho*np.sum(np.prod(paired_amp,axis=1))))
    # Tight delta-method bounds over all correlation matrices (polygon inequality).
    upper = float(relative.sum())
    lower = max(0.,2*float(relative.max())-upper)
    extra = np.array([0.,0.,0.,1.])
    full = np.column_stack((design,extra))
    beta_full = np.linalg.solve(full,np.log(y))
    return dict(zip([f'v7.{i:02d}' for i in range(2,12)],[
        {'cross_ratio':float(np.exp(c)),'log_ratio':c},
        {'after_gains':contrast(gain*y),'gain_log_contrast':contrast(gain)},
        {'rank':int(np.linalg.matrix_rank(design)),'contrast_times_design':(signs@design).tolist()},
        {'cell_residuals':residual.tolist(),'max_abs_log_error':float(max(abs(residual)))},
        {'relative_stat_proxies':relative.tolist(),'independent_log_sd':pair_sd(0.)},
        {str(rho):pair_sd(rho) for rho in [-1.,0.,.5,1.]},
        {'min_log_sd':lower,'max_log_sd':upper},
        {'cross_ratio_narrow':float(np.exp(contrast(values((35.,36.)))))},
        {'per_cell_minimax_log_radius':abs(c)/4,'one_cell_multiplier':float(np.exp(c)),
         'symmetric_multiplier':float(np.exp(abs(c)/4))},
        {'ordinary_interaction':float(beta_full[-1]),'reconstructed':np.exp(full@beta_full).tolist(),
         'max_relative_error':float(max(abs(np.exp(full@beta_full)/y-1)))}
    ]))

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
