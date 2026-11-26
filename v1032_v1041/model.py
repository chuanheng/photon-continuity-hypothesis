"""Write/read interferometry in the one-excitation material and bypass subspace."""
import json
import numpy as np

def amplitudes(x,y):
    return np.sqrt((1-x)*(1-y)),np.sqrt(x*y)

def prob(x,y,phi,t=1.,gamma=1.):
    a,b=amplitudes(x,y)
    return a*a+t*b*b+2*a*b*np.sqrt(t)*np.real(gamma*np.exp(1j*phi))

def run():
    phases=np.linspace(0,2*np.pi,17)
    x,y=.25,.65
    a,b=amplitudes(x,y)
    low,high=prob(x,y,np.pi),prob(x,y,0)
    root=np.sqrt(max(0,1-4*.2*.8))
    contrast=(high-low)/(high+low)
    # One output port after a calibrated read operation with variable y.
    y2=.3
    p=[prob(x,r,0,0) for r in (y,y2)]
    # Partial which-path marker with overlap g in a balanced interferometer.
    g=.6
    marker0=np.diag([1,0])
    vec=np.array([g,np.sqrt(1-g*g)])
    diff=marker0-np.outer(vec,vec)
    discr=.5*np.sum(abs(np.linalg.eigvalsh(diff)))
    # Sum and difference marker basis, each joint probability has weight 1/2.
    eraser=[float(abs(a+sign*b*np.exp(.4j))**2/2) for sign in (1,-1)]
    # Nearly destructive, nonreciprocal port with B smaller than A.
    slope=-b/(a-b)
    sigma=.8
    # Unknown equal cross-talk on material and bypass drives only a global phase.
    return dict(local_phase=dict(high=high,low=low,visibility=contrast),
                reciprocal=dict(roots=[(1-root)/2,(1+root)/2],minimum=prob(.2,.2,np.pi)),
                swapped=dict(max_error=float(abs(prob(x,y,phases)-prob(y,x,phases)).max()),occupancies=[x,y]),
                blocked_reference=dict(no_material=p,estimated_x=1-p[1]/(1-y2)),
                distinguishability=dict(D=discr,V=g,quadratic_sum=discr**2+g**2),
                eraser=dict(joints=eraser,unconditional=sum(eraser)),
                conditional_phase=dict(slope=slope,true_population=x,selected_probability=low),
                echo=dict(free=float(np.exp(-2*sigma**2)),static_echo=1.,independent_echo=float(np.exp(-sigma**2))),
                crosstalk=dict(peak=abs(a+b)**2,minimum_common=abs((a+b)*np.exp(.83j))**2,
                               relative=prob(x,y,.83)),
                scale_alias=dict(fringe_coefficients=[.6*.9,.9*.6],
                                 inferred_marker=[.54/.93,.54/.87],
                                 physical_phase_jitter=float(np.sqrt(-2*np.log(.9)))))
if __name__=='__main__':print(json.dumps(run(),indent=2))
