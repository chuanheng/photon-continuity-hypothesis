"""Common-window comparison on figure 2 and 3 of Pašić & Ilakovac (1995)."""
import json
import numpy as np

# x, center, upper and lower error cap in the PDF embedded rasters.
MARKS = {
    '55.791/D1': [(387,369,356,383),(460,384,371,397),(532,416,400,440),(596,395,379,417)],
    '55.791/D2': [(380,644,626,667),(459,633,618,653),(562,622,610,635),(659,608,596,624)],
    '54.612/D1': [(335,424,400,460),(465,432,406,478),(546,414,392,446),(629,391,376,412)],
    '54.612/D2': [(331,687,668,719),(440,656,642,675),(539,667,650,691),(618,689,662,740)]
}
# Local fiducials close to the interval. Columns are x at two labeled energy
# ticks, their energies, y at 1e-30 and 1e-32. Allow inverse display scale for D2.
AXES = {'55':(406,536,34,36,356,605),'54':(305,483,34,36,392,667)}
# Upper-series curve ordinates sampled on either side and inside the window.
CURVES = {'55':[(387,435,371),(460,416,360),(532,397,347),(596,379,336)],
          '54':[(335,455,393),(465,427,377),(546,408,365),(629,388,352)]}
BAND = (34.5,36.5)

def weights(energy, window):
    lo,hi = window
    if not energy[0] <= lo < hi <= energy[-1]:
        raise ValueError("interpolation interval outside marker support")
    knots = np.r_[lo,energy[(energy>lo)&(energy<hi)],hi]
    basis = np.eye(len(energy))
    return np.array([np.trapezoid(np.interp(knots,energy,col),knots)/(hi-lo) for col in basis])

def summarize(key, window=BAND):
    tag = key[:2]
    x0,x1,e0,e1,y0,y1 = AXES[tag]
    def energy(x): return e0+(x-x0)*(e1-e0)/(x1-x0)
    # All ordinates expressed in units of 1e-30 m²/(keV sr).
    def ordinate(y): return 10**(-2*(y-y0)/(y1-y0))
    x,y,top,bottom = np.array(MARKS[key]).T
    correction = 100 if key.endswith('D2') else 1
    coeff = weights(energy(x),window)
    linear = correction*ordinate(y)
    mean = coeff@linear
    # Half error-bar span is a symmetric sensitivity proxy on the linear axis.
    errors = correction*(ordinate(top)-ordinate(bottom))/2
    cx,solid,dashed = np.array(CURVES[tag]).T
    wc = weights(energy(cx),window)
    theory = np.array([wc@ordinate(solid),wc@ordinate(dashed)])
    return dict(mean=float(mean),theory=theory.tolist(),
                weights=coeff.tolist(),independent=float(np.linalg.norm(coeff*errors)),
                fully_correlated=float(coeff@errors),display_scale=correction,
                geometric_mean=float(np.exp(coeff@np.log(linear))),
                absolute_difference=np.abs(theory-mean).tolist())

def run():
    all_rows = {k:summarize(k) for k in MARKS}
    def field(name):return {k:r[name] for k,r in all_rows.items()}
    narrow = {k:summarize(k,(35.,36.))['absolute_difference'] for k in MARKS}
    return dict(zip(['v6.92','v6.93','v6.94','v6.95','v6.96','v6.97','v6.98','v6.99','v7.00','v7.01'],[
        field('display_scale'),field('weights'),field('mean'),field('theory'),
        field('absolute_difference'),field('geometric_mean'),field('independent'),
        field('fully_correlated'),narrow,
        {k:all_rows[k+'/D2']['mean']/all_rows[k+'/D1']['mean'] for k in ['55.791','54.612']}
    ]))

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
