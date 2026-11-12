"""Weak-probe Rabi absorption spectrum with Voigt broadening; hbar=1."""
import math
import numpy as np

def rabi_levels(cutoff=8, omega=1., omega0=1., coupling=.2):
    if isinstance(cutoff,bool) or not isinstance(cutoff,int) or cutoff<2: raise ValueError('cutoff >=2')
    if not np.all(np.isfinite([omega,omega0,coupling])): raise ValueError('nonfinite parameter')
    a=np.diag(np.sqrt(np.arange(1,cutoff,dtype=float)),1)
    x=a+a.T
    n=np.diag(np.arange(cutoff,dtype=float))
    z=np.diag([-1.,1.]);sx=np.array([[0.,1.],[1.,0.]])
    h=omega*np.kron(np.eye(2),n)+omega0/2*np.kron(z,np.eye(cutoff))+coupling*np.kron(sx,x)
    energies,states=np.linalg.eigh(h)
    strengths=np.abs(states.conj().T@np.kron(np.eye(2),x)@states)**2
    return energies,strengths

def thermal_populations(energies,temperature):
    e=np.asarray(energies,dtype=float)
    if e.ndim!=1 or not len(e) or not np.all(np.isfinite(e)) or not math.isfinite(temperature) or temperature<0:
        raise ValueError('invalid energies or temperature')
    if temperature==0:
        p=np.zeros(len(e));p[np.argmin(e)]=1.;return p
    w=np.exp(-(e-e.min())/temperature)
    return w/w.sum()

def transitions(energies,strengths,populations,min_weight=0.):
    e=np.asarray(energies,dtype=float);s=np.asarray(strengths,dtype=float);p=np.asarray(populations,dtype=float)
    if e.ndim!=1 or s.shape!=(len(e),len(e)) or p.shape!=(len(e),) or not all(np.all(np.isfinite(v)) for v in (e,s,p)):
        raise ValueError('invalid shapes or nonfinite values')
    if np.any(s < -1e-12) or np.any(p<0) or not np.isclose(p.sum(),1.) or not np.isfinite(min_weight) or min_weight<0:
        raise ValueError('invalid weights')
    return [(float(e[j]-e[i]),float(p[i]*s[j,i])) for i in range(len(e)) for j in range(len(e))
            if e[j]>e[i] and p[i]*s[j,i]>min_weight]

def lorentzian(x,center,gamma):
    if not math.isfinite(gamma) or gamma<=0: raise ValueError('gamma must be positive')
    return gamma/(math.pi*((np.asarray(x)-center)**2+gamma**2))

def voigt_gauss_quadrature(x,center,gamma,sigma,order=48):
    if not math.isfinite(sigma) or sigma<0: raise ValueError('invalid sigma')
    if sigma==0: return lorentzian(x,center,gamma)
    if not isinstance(order,int) or order<8: raise ValueError('order >=8')
    nodes,weights=np.polynomial.hermite.hermgauss(order)
    v=lorentzian(np.asarray(x)[...,None],center+math.sqrt(2)*sigma*nodes,gamma)
    return np.sum(v*weights,axis=-1)/math.sqrt(math.pi)

def observed_spectrum(frequencies,lines,gamma=.04,sigma=.03,order=48):
    f=np.asarray(frequencies,dtype=float)
    if f.ndim!=1 or not np.all(np.isfinite(f)): raise ValueError('invalid grid')
    result=np.zeros_like(f)
    for center,weight in lines:
        if not math.isfinite(center) or not math.isfinite(weight) or weight<0: raise ValueError('invalid line')
        result+=weight*voigt_gauss_quadrature(f,center,gamma,sigma,order)
    return result
