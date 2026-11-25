"""Paired descriptive comparisons on the eight previously selected plot markers."""
import json
import numpy as np
from v672_v681.model import digitize, read

# Upper series only. Each row follows the x coordinates in figure_inputs.json.
# Central ordinates read along the solid and dashed lines; dashed gaps interpolated.
TRACE = {'fig2': ([470,453,435,416], [391,382,371,360]),
         'fig3': ([474,455,427,408], [405,393,377,365])}

def observations():
    rows = []
    for key, fig in digitize().items():
        (y0, a), (y1, b) = read('figure_inputs.json')[key]['y_grid']
        slope = (b-a)/(y1-y0)
        for point, solid, dashed in zip(fig['points'], *TRACE[key]):
            # Log residual weighted by half the plotted error span in log space.
            width = np.log(point['upper_plotted_error_endpoint']/point['lower_plotted_error_endpoint'])/2
            curves = [np.log(10)*(a+slope*(y-y0)) for y in (solid,dashed)]
            rows.append([np.log(point['cross_section']), width, *curves, abs(slope)*np.log(10)])
    return np.array(rows).T

def run():
    y,w,solid,dashed,k = observations()
    def loss(r, width=w):
        return float(np.sum((r/width)**2))
    def offset(r, width=w):
        return float(np.average(r,weights=1/width**2))
    res = [y-solid,y-dashed]
    def scores(slice_):
        return [loss(r[slice_],w[slice_]) for r in res]
    offsets = [offset(r) for r in res]
    bounded = np.clip(offsets,np.log(.91),np.log(1.09))
    # Worst-case independent +/-3 pixel shifts of curve ordinates, data held fixed.
    intervals = [[loss(np.maximum(np.abs(r)-3*k,0)),loss(np.abs(r)+3*k)] for r in res]
    diff = ((res[0]/w)**2-(res[1]/w)**2)
    delta = dashed-solid
    centered = delta-offset(delta)
    r = res[0]-offset(res[0])
    weight = np.sum(centered*r/w**2)/np.sum((centered/w)**2)
    return dict(zip([f'v6.{i}' for i in range(82,92)],[
        np.exp(solid).tolist(),np.exp(dashed).tolist(),scores(slice(0,4)),scores(slice(4,8)),
        [{'scale':float(np.exp(a)),'score':loss(r-a)} for a,r in zip(offsets,res)],
        [{'scale':float(np.exp(a)),'score':loss(r-a)} for a,r in zip(bounded,res)],
        [loss(r[4:]-offset(r[:4],w[:4]),w[4:]) for r in res],intervals,
        (diff.sum()-diff).tolist(),{'log_interpolation':float(weight),'profile_score':loss(r-weight*centered)}
    ]))

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
