"""Published acquisition constraints and selected experimental points from Fizika B."""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.stats import norm
ROOT=Path(__file__).parent
def read(name):return json.loads((ROOT/name).read_text())

def support():
    out=[]
    for e in (55.791,54.612):
        cutoff=e-8
        for width in (.1415,.1402):
            out.append(dict(incident_keV=e,bin_width_keV=width,ideal_upper_keV=cutoff,
                            full_bins_between_Kalpha_marker_and_edge=(9.876-8)/width,
                            rounded_bin_uncertainty_keV=width/2))
    return out

def exposure():
    t=np.array([366.,893.,682.,819.]);weights=t/t.sum()
    # For unknown block response multiplier in [0.9, 1.1], exact max difference
    # of exposure weighting and equal group weighting is .1*||w-u||_1.
    return dict(total_hours=t.sum(),weights=weights.tolist(),kish_groups=1/(weights@weights),
                equal_weight_max_abs_bias=.1*sum(abs(weights-.25)),achieving_multipliers=(1+.1*np.sign(weights-.25)).tolist())

def mirror():
    out=[]
    for f in (0.,.15,.45,.5):
        M=np.array([[1-f,f],[f,1-f]])
        out.append(dict(mixing=f,output=(M@np.array([.8,.2])).tolist(),sum_mode=1.,
                        difference_mode=1-2*f,inverse_gain=None if f==.5 else 1/(1-2*f)))
    return out

def digitize():
    meta=read('figure_inputs.json');result={}
    for key in ('fig2','fig3'):
        f=meta[key]
        (x0,e0),(x1,e1)=f['x_grid'];(y0,a),(y1,b)=f['y_grid']
        def ordinate(y):return 10**(a+(b-a)*(y-y0)/(y1-y0))
        pts=[]
        for x,y,top,bottom in f['points']:
            pts.append(dict(energy_keV=e0+(x-x0)*(e1-e0)/(x1-x0),cross_section=ordinate(y),
                lower_plotted_error_endpoint=ordinate(bottom),upper_plotted_error_endpoint=ordinate(top)))
        result[key]=dict(points=pts,three_pixel_relative_up=ordinate(y0-3)/ordinate(y0)-1)
    return result

def normalization():
    f=digitize()['fig2']['points'];y=np.array([p['cross_section'] for p in f]);y=y/y[0]
    # Illustrative fully common log-scale offset; the paper quotes an approximate
    # geometrical uncertainty, not a probability distribution or its covariance.
    a=.09
    combined=np.sqrt((a*y.sum())**2)
    independent=a*np.linalg.norm(y)
    return dict(weighted_relative_common=combined/y.sum(),weighted_relative_independent=independent/y.sum(),
                max_ratio_shift_common=0.,independent_scale_ratio=(1+a)/(1-a),
                common_cov_rank=np.linalg.matrix_rank(np.outer(y,y)).item())

def source_lines():
    target=54.612;other=54.079
    diff=target-other
    out=[]
    for sigma in (.1,.25,.5):
        gate=.25
        retained=norm.cdf(gate/sigma)-norm.cdf(-gate/sigma)
        spill=norm.cdf((diff+gate)/sigma)-norm.cdf((diff-gate)/sigma)
        rho=np.exp(-diff**2/(4*sigma**2))
        out.append(dict(sigma_keV=sigma,own_acceptance=retained,other_acceptance=spill,
                        template_overlap=rho,gram_condition=(1+rho)/(1-rho)))
    return out

def solid_angle():
    d,r=9.91,7.98
    theta=np.arctan(r/d);c=np.cos(theta)
    j=quad(lambda a:np.cos(a)**3*np.sin(a),0,theta)[0]
    return dict(half_angle_deg=np.rad2deg(theta),bare_solid_angle_sr=2*np.pi*(1-c),
                unit_transmission_integral=j,analytic=(1-c**4)/4,
                ratio_to_unweighted=j/(1-c))

def missing_joint():
    # Two event populations yield exactly the same published 1-D counts and
    # timing marginal, but opposite prompt-energy dependence.
    a=np.array([[12,8],[3,17]]);b=np.array([[4,16],[11,9]])
    return dict(energy_sums=a.sum(1).tolist(),time_sums=a.sum(0).tolist(),
                energy_marginal_max_diff=int(max(abs(a.sum(1)-b.sum(1)))),
                time_marginal_max_diff=int(max(abs(a.sum(0)-b.sum(0)))),
                first_bin_prompt_fractions=[a[0,0]/a[0].sum(),b[0,0]/b[0].sum()])
def run():
    from .profile import profile
    return dict(zip([f'v6.{i}' for i in range(72,82)],[support(),exposure(),mirror(),normalization(),
        read('edge.json'),source_lines(),digitize(),solid_angle(),missing_joint(),profile(digitize())]))
if __name__=='__main__':print(json.dumps(run(),indent=2))
