"""Conservative all-order upper bounds for primary photons in frozen Al model."""
import json
import numpy as np
from v612_v621.model import TABLE as ANG, REST
from v602_v611.transport import TABLE, attenuation

def envelope(low, high, cells=256):
    # Positive lower Riemann sum for the azimuth-averaged angular normalization.
    # In each cosine cell bound over the entire incident energy interval.
    edges = np.linspace(-1, 1, cells+1)
    normal = np.zeros(2)
    for left, right in zip(edges[:-1], edges[1:]):
        q0 = low/12.39841984*np.sqrt((1-right)/2)
        q1 = high/12.39841984*np.sqrt((1-left)/2)
        interior = ANG[(ANG[:,0]>q0) & (ANG[:,0]<q1)]
        mu_sq = max(0., left, -right)**2
        recoil_min = 1/(1+high/REST*(1-left))
        for j, factor in enumerate((recoil_min**2, 1.)):
            col = j+1
            extremum = min(*np.interp([q0,q1], ANG[:,0], ANG[:,col]),
                           interior[:,col].min(initial=np.inf))
            normal[j] += (right-left)*(1+mu_sq)*factor*extremum**col
    return 2*np.array([ANG[:,1].max(), ANG[:,2].max()**2])/normal

def calculate(floor=35., aperture=3.):
    energies = TABLE[(TABLE[:,0]>=floor)&(TABLE[:,0]<=60.),0]
    assert energies[0] == floor and energies[-1] == 60
    diam = np.hypot(.1,1.)
    opening = 2*np.sin(np.deg2rad(aperture)/2)**2
    scatter = attenuation(energies,2)+attenuation(energies,3)
    # Integrate collision density up to maximum chord. The integral decreases
    # with total attenuation, giving an upper bound within each energy cell.
    cont, terminal = [], []
    for i,(lo,hi) in enumerate(zip(energies[:-1],energies[1:])):
        pair = energies[i:i+2]
        loss = attenuation(pair).min()
        effective_length = -np.expm1(-loss*diam)/loss
        cont.append(effective_length*max(scatter[i:i+2]))
        directional = np.minimum(1.,opening*envelope(lo,hi))
        terminal.append(effective_length*sum(
            attenuation(pair,j+2).max()*directional[j] for j in range(2)))
    b,t = max(cont),max(terminal)
    first = -np.expm1(-attenuation(60.)*.1)*(attenuation(60.,2)+attenuation(60.,3))/attenuation(60.)
    def tail(n):
        return first*b**(n-2)*t/(1-b)
    return dict(floor_keV=floor,aperture_deg=aperture,first_scatter=first,
                continuation=b,terminal=t,selected_order_ge3=tail(3),
                selected_order_ge4=tail(4),selected_order_ge8=tail(8),
                below_floor_entry_ge4=first*b**3 if floor==35. else None)

if __name__ == '__main__':
    print(json.dumps(calculate(),indent=2))
