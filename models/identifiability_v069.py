import numpy as np
from scipy.optimize import minimize_scalar

def visibility(x,strength,law='exp'):
    x=np.asarray(x,float)
    if np.any(x<0) or strength<0: raise ValueError('nonnegative required')
    if law=='exp': return np.exp(-strength*x)
    if law=='gaussian': return np.exp(-strength*x*x)
    raise ValueError('unknown law')

def coincidence(x,strength,law='exp'):
    return (1-visibility(x,strength,law))/2

def kl(p,q):
    p=np.asarray(p,float);q=np.asarray(q,float)
    with np.errstate(divide='ignore',invalid='ignore'):
        return np.where(p>0,p*np.log(p/np.clip(q,1e-300,1)),0)+np.where(p<1,(1-p)*np.log((1-p)/np.clip(1-q,1e-300,1)),0)

def fit(x,lam,shots):
    p=coincidence(x,lam)
    f=lambda k:float(2*shots*np.sum(kl(p,coincidence(x,k,'gaussian'))))
    r=minimize_scalar(f,bounds=(1e-8,10),method='bounded')
    return float(r.x),float(r.fun)
