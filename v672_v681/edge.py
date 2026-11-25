"""Regenerate narrow-beam Ge transmission across the K edge using xraylib."""
import json
import xraylib as x
import numpy as np
from scipy.integrate import quad
from scipy.stats import norm
def run():
    edge=x.EdgeEnergy(32,x.K_SHELL)
    def t(e):
        return np.exp(-.01*5.323*x.CS_Total(32,e))
    rows=[]
    for sigma in (.01,.05,.15):
        lo,hi=10.98-8*sigma,10.98+8*sigma
        val=quad(lambda e:t(e)*norm.pdf(e,10.98,sigma),lo,hi,points=[edge] if lo<edge<hi else [],
                 epsabs=1e-10,limit=200)[0]
        rows.append(dict(sigma_keV=sigma,weight_above_edge=norm.sf((edge-10.98)/sigma),transmission=val))
    return dict(edge_keV=edge,nominal=t(10.98),below=t(edge-.001),above=t(edge+.001),rows=rows)
if __name__=='__main__':
    print(json.dumps(run(),indent=2))
