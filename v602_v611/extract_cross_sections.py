"""Regenerate the aluminum cross-section snapshot with xraylib 4.3.0."""
import sys

import xraylib

print('energy_keV,total_cm2_g,compton_cm2_g,rayleigh_cm2_g,photoelectric_cm2_g', file=sys.stdout)
for step in range(121):
    energy = 35 + step/4
    values = [function(13,energy) for function in (
        xraylib.CS_Total,xraylib.CS_Compt,xraylib.CS_Rayl,xraylib.CS_Photo)]
    print(','.join(f'{number:.12g}' for number in [energy,*values]))
