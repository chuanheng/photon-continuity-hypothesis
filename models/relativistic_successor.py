"""Relativistic kinematics for gamma + H(rest) -> gamma' + e + p.
Natural units c=1; energies and masses in eV. No QED amplitudes.
"""
import math
ELECTRON_MASS_EV=510998.95000
PROTON_MASS_EV=938272088.16
IONIZATION_EV=13.5984345997
HYDROGEN_MASS_EV=ELECTRON_MASS_EV+PROTON_MASS_EV-IONIZATION_EV

def _validate(energy,theta):
    if not math.isfinite(energy) or energy<0 or not math.isfinite(theta) or not 0<=theta<=math.pi:
        raise ValueError('invalid energy or angle')

def invariant_ep_sq(incident_ev,successor_ev,theta):
    _validate(incident_ev,theta)
    if not math.isfinite(successor_ev) or successor_ev<0: raise ValueError('invalid successor energy')
    m=HYDROGEN_MASS_EV
    return m*m+2*m*(incident_ev-successor_ev)-2*incident_ev*successor_ev*(1-math.cos(theta))

def threshold_incident_ev():
    m=HYDROGEN_MASS_EV
    pair=ELECTRON_MASS_EV+PROTON_MASS_EV
    return (pair-m)*(pair+m)/(2*m)

def max_successor_ev(incident_ev,theta):
    _validate(incident_ev,theta)
    m=HYDROGEN_MASS_EV
    numerator=2*m*(incident_ev-threshold_incident_ev())
    if numerator<=0: return 0.0
    return numerator/(2*(m+incident_ev*(1-math.cos(theta))))

def allowed(incident_ev,successor_ev,theta):
    _validate(incident_ev,theta)
    if not math.isfinite(successor_ev) or successor_ev<0: raise ValueError('invalid successor energy')
    return incident_ev>=threshold_incident_ev() and successor_ev<=max_successor_ev(incident_ev,theta)

def final_pair_four_vectors(incident_ev,successor_ev,theta,cm_cos=0.0,cm_azimuth=0.0):
    """Electron, proton, outgoing photon 4-vectors (E,px,py,pz)."""
    if not allowed(incident_ev,successor_ev,theta): raise ValueError('forbidden')
    if not all(math.isfinite(v) for v in (cm_cos,cm_azimuth)) or not -1<=cm_cos<=1:
        raise ValueError('invalid CM direction')
    m=HYDROGEN_MASS_EV
    k=(successor_ev,successor_ev*math.sin(theta),0.0,successor_ev*math.cos(theta))
    q0=m+incident_ev-successor_ev
    qvec=(-k[1],0.0,incident_ev-k[3])
    s=q0*q0-sum(v*v for v in qvec)
    me=ELECTRON_MASS_EV; mp=PROTON_MASS_EV
    root=math.sqrt(s)
    ee=(s+me*me-mp*mp)/(2*root)
    ep=(s+mp*mp-me*me)/(2*root)
    pstar=math.sqrt(max(0.0,ee*ee-me*me))
    sint=math.sqrt(max(0.0,1-cm_cos*cm_cos))
    direction=(sint*math.cos(cm_azimuth),sint*math.sin(cm_azimuth),cm_cos)
    beta=tuple(v/q0 for v in qvec)
    b2=sum(v*v for v in beta)
    gamma=q0/root
    def boost(en,vec):
        dot=sum(b*v for b,v in zip(beta,vec))
        factor=((gamma-1)*dot/b2 if b2>0 else 0.0)+gamma*en
        return (gamma*(en+dot),*(v+factor*b for v,b in zip(vec,beta)))
    return boost(ee,tuple(pstar*d for d in direction)),boost(ep,tuple(-pstar*d for d in direction)),k
