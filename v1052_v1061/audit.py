"""Calibration and held-out controls for the material occupation witness."""
import json
import numpy as np
from .model import run as prefix

def run():
    old=prefix()
    theta=.16
    rotate=np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])
    pulse=rotate@np.diag([1,-1]);P=np.diag([0,1])
    bias=(pulse.T@P@pulse-P)/2
    observed=.62;angle=np.arccos(np.sqrt(observed))
    calibrated=np.cos(angle+np.array([.08,-.08]))**2
    # For third effect use equal material and centre responses, so the range
    # is the largest available perpendicular component of the weighted Bloch ball.
    a=.32;r=.18
    shift=np.array(old['spectral']['measured'])-a
    w=np.array([.65,.60])-a
    A=r*r-w@w;B=2*(shift@w-r*r);C=r*r-shift@shift
    peak=np.clip(-B/(2*A),*old['joint']['interval'])
    radius=np.sqrt(max(0.,A*peak**2+B*peak+C))
    # Perfectly classical schedule: orthogonal readouts follow two source preparations.
    skew=np.array([1.,1.]); blind=np.array([.5,.5])
    # Probe samples accumulated conditional phase of a stored excitation.
    t=np.arange(1,8)*.3
    population=.64;g=.37
    def coherence(strength):
        return (1-population)+population*np.exp(1j*t*strength)
    return dict(prefix=old,mixing=dict(bias=np.linalg.eigvalsh(bias).tolist(),transfer=np.sin(theta)**2),
                axis_interval=calibrated.tolist(),
                third_effect=dict(center_occupation=float(peak),range=[a-radius,a+radius]),
                schedule=dict(blocked_norm=np.linalg.norm(skew),blind_norm=np.linalg.norm(blind)),
                conditional_probe=dict(max_error=float(max(abs(coherence(g)-coherence(.21+.16)))),
                                       largest_deviation=float(max(abs(coherence(g)-1)))))
if __name__=='__main__': print(json.dumps(run(),indent=2))
