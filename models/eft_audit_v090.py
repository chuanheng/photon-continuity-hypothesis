"""v0.90: neutral complex scalar EFT contact-vertex audit.
Minkowski (+---), natural units. Standard field theory, not persistent photons.
The dimension-six operator is c/Lambda**2 |S|**2 F_mu_nu F^mu_nu.
"""
import numpy as np
import sympy as sp
METRIC=np.diag([1.,-1.,-1.,-1.])
def dot(a,b):
    a=np.asarray(a,float);b=np.asarray(b,float)
    if a.shape!=(4,) or b.shape!=(4,):raise ValueError('four-vectors required')
    return float(a@METRIC@b)
def vertex(k1,k2):
    k1=np.asarray(k1,float);k2=np.asarray(k2,float)
    if k1.shape!=(4,) or k2.shape!=(4,):raise ValueError('four-vectors required')
    return dot(k1,k2)*METRIC-np.outer(k2,k1)
def ward_residuals(k1,k2):
    v=vertex(k1,k2)
    return METRIC@np.asarray(k1,float)@v, v@(METRIC@np.asarray(k2,float))
def amplitude(k1,k2,eps1,eps2,c=1.,cutoff=10.):
    if cutoff<=0:raise ValueError('cutoff must be positive')
    return float((4*c/cutoff**2)*np.asarray(eps1,float)@METRIC@vertex(k1,k2)@METRIC@np.asarray(eps2,float))
def unpolarized_tensor_norm(k1,k2):
    v=vertex(k1,k2)
    return float(np.einsum('ab,ac,bd,cd->',v,METRIC,METRIC,v))
def tensor_norm_identity(k1,k2):
    return 2*dot(k1,k2)**2+dot(k1,k1)*dot(k2,k2)
def null_momenta(angle,energy=1.):
    if energy<=0:raise ValueError('positive energy')
    return np.array([energy,0.,0.,energy]),np.array([energy,energy*np.sin(angle),0.,energy*np.cos(angle)])
def physical_polarizations(angle):
    return (np.array([0.,1.,0.,0.]),np.array([0.,0.,1.,0.])),(np.array([0.,np.cos(angle),0.,-np.sin(angle)]),np.array([0.,0.,1.,0.]))
def boost_z(rapidity):
    c,s=np.cosh(rapidity),np.sinh(rapidity)
    return np.array([[c,0.,0.,s],[0.,1.,0.,0.],[0.,0.,1.,0.],[s,0.,0.,c]])
def gauge_shift_invariance(k1,k2,e1,e2,a=.7,b=-.2):
    v=amplitude(k1,k2,e1,e2)
    return amplitude(k1,k2,np.asarray(e1)+a*np.asarray(k1),np.asarray(e2)+b*np.asarray(k2))-v
def operator_dimensions():
    return {'dim_S':1,'dim_A':1,'dim_derivative':1,'dim_F':2,
      'dim_abs_S_squared':2,'dim_F_squared':4,'operator_dim':6,'coupling_dim':-2}
def global_charge_invariance(S,phase):
    z=complex(S)
    return float(abs(abs(z*np.exp(1j*phase))**2-abs(z)**2))
def noether_current_plane_wave(amp,energy):
    return float(2*energy*abs(amp)**2)
def kinetic_coefficient(c,modulus2,cutoff):
    if cutoff<=0 or modulus2<0:raise ValueError('invalid fields')
    return 1.-4*c*modulus2/cutoff**2
def eom_const_background_dispersion(k0,kvec,c=1.,modulus2=.2,cutoff=10.):
    Z=kinetic_coefficient(c,modulus2,cutoff)
    if Z<=0:raise ValueError('unhealthy kinetic term')
    return float(Z*(k0*k0-np.dot(kvec,kvec)))
def wilson_parameter(c,cutoff):
    if cutoff<=0:raise ValueError('positive cutoff')
    return c/cutoff**2
def fisher_c_cutoff(c,cutoff):
    if cutoff<=0:raise ValueError('positive cutoff')
    grad=np.array([1/cutoff**2,-2*c/cutoff**3])
    return np.outer(grad,grad)
def sympy_ward_identity():
    k=sp.symbols('k0:4',real=True);p=sp.symbols('p0:4',real=True)
    metric=sp.diag(1,-1,-1,-1)
    kv,pv=sp.Matrix(k),sp.Matrix(p)
    a=(kv.T*metric*pv)[0]
    t=a*metric-pv*kv.T
    return {'left':[sp.simplify(x) for x in kv.T*metric*t],
            'right':[sp.simplify(x) for x in t*metric*pv],
            'dimension':6}
def summary():
    rows=[]
    for angle in [0.,np.pi/6,np.pi/3,np.pi/2,2*np.pi/3,np.pi]:
        k1,k2=null_momenta(angle,2.)
        e1,e2=physical_polarizations(angle)
        values=[amplitude(k1,k2,a,b) for a in e1 for b in e2]
        rows.append({'angle_rad':float(angle),'k1_dot_k2':dot(k1,k2),
            'tensor_contraction':unpolarized_tensor_norm(k1,k2),
            'sum_physical_pol_amplitudes_squared':float(sum(x*x for x in values)),
            'sum_expected':float((4/100)**2*2*dot(k1,k2)**2)})
    k1,k2=null_momenta(np.pi/3,2.)
    e1,e2=physical_polarizations(np.pi/3)
    B=boost_z(.35)
    before=amplitude(k1,k2,e1[0],e2[0])
    after=amplitude(B@k1,B@k2,B@e1[0],B@e2[0])
    w=sympy_ward_identity()
    return {'version':'v0.90','operator':'(|S|^2 F_mu_nu F^mu_nu)/Lambda^2',
        'operator_dimensions':operator_dimensions(),
        'symbolic_ward':{k:([str(x) for x in v] if isinstance(v,list) else v) for k,v in w.items()},
        'angle_examples':rows,'boost_amplitude_error':float(after-before),
        'wilson_degeneracy_example':{'c1':1.,'Lambda1':10.,'c2':4.,'Lambda2':20.,'shared_wilson_g':wilson_parameter(1,10)},
        'constant_background':{'Z_example':kinetic_coefficient(1.,.2,10.),
           'on_shell_dispersion_factor':eom_const_background_dispersion(2.,[0,0,2])},
        'classification':'Conventional gauge-invariant scalar-photon EFT term; global S-charge is not historical photon identity.',
        'novel_identity_prediction':False}
if __name__=='__main__':
    import json
    print(json.dumps(summary(),indent=2))
