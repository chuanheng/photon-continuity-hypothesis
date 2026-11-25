"""Freeze the angular xraylib table for aluminum."""
import numpy as np
import xraylib


def values(q):
    if q == 0:
        return 0., 13.
    return xraylib.SF_Compt(13,q), xraylib.FF_Rayl(13,q)


print('q_inverse_angstrom,incoherent_function,elastic_form_factor')
for q in np.r_[0.,np.linspace(.01,5.4,540)]:
    print(','.join(f'{v:.12g}' for v in (q,*values(q))))
