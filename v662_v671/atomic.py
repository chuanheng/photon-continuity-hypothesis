"""Regenerate frozen atomic coefficients (xraylib 4.3.0)."""
import json
import xraylib as x

def build():
    result={}
    for name,z,rho in [('Al',13,2.70),('Ge',32,5.323)]:
        energies=[9.876,10.98,45.,55.791,59.537,60.]
        result[name]={'density':rho,'fluor_yield_K':x.FluorYield(z,x.K_SHELL),
          'cross_sections':{str(e):[fun(z,e) for fun in (x.CS_Total,x.CS_Compt,x.CS_Photo,x.CS_Rayl)] for e in energies}}
    result['Ge']['profile_au']=[[i/50,x.ComptonProfile(32,i/50)] for i in range(251)]
    return result

if __name__=='__main__':
    print(json.dumps(build(),indent=2))
