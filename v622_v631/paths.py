"""Forced-collision transport on straight chords, with Stokes propagation."""
import itertools
import json
import numpy as np
from scipy.stats import qmc
from v612_v621.model import angular_energy, NODES, WEIGHTS, REST
from v602_v611.transport import attenuation

ENERGY = np.linspace(35,60,501)
NORMAL = {p: angular_energy(ENERGY[:,None],NODES,p,True)[0]@WEIGHTS for p in 'CR'}

def dot(a,b):
    return np.einsum('ij,ij->i',a,b)

def chord(point,direction,h,r):
    dz = direction[:,2]
    face = np.divide(np.where(dz>0,h-point[:,2],-point[:,2]),dz,
                     out=np.full_like(dz,np.inf),where=dz!=0)
    transverse = dot(direction[:,:2],direction[:,:2])
    proj = dot(point[:,:2],direction[:,:2])
    disc = proj**2+transverse*(r*r-dot(point[:,:2],point[:,:2]))
    side = np.divide(-proj+np.sqrt(np.maximum(0.,disc)),transverse,
                     out=np.full_like(dz,np.inf),where=transverse>0)
    return np.maximum(0.,np.minimum(face,side))

def score(path, samples, h=.1,r=.5,angle=3.):
    n=len(samples)
    point=np.zeros((n,3))
    direction=np.tile([0.,0.,1.],(n,1))
    basis=np.tile([1.,0.,0.],(n,1))
    energy=np.full(n,60.)
    weight=np.ones(n)
    q,u=np.zeros(n),np.zeros(n)
    for i,process in enumerate(path):
        leg=chord(point,direction,h,r)
        length=samples[:,3*i]*leg
        weight*=leg*attenuation(energy,2 if process=='C' else 3)*np.exp(-attenuation(energy)*length)
        point+=length[:,None]*direction
        width=1-np.cos(np.deg2rad(angle)) if i==len(path)-1 else 2.
        z=1-width*samples[:,3*i+1]
        phi=2*np.pi*samples[:,3*i+2]
        opening=np.sqrt((1-z)*(1+z))
        outgoing=np.column_stack((opening*np.cos(phi),opening*np.sin(phi),z))
        mu=np.clip(dot(direction,outgoing),-1,1)
        normal=np.cross(direction,outgoing)
        norm=np.linalg.norm(normal,axis=1)
        normal=np.divide(normal,norm[:,None],out=basis.copy(),where=norm[:,None]>0)
        c=dot(normal,basis)
        s=dot(normal,np.cross(direction,basis))
        rotated_q=q*(c*c-s*s)+u*2*c*s
        rotated_u=u*(c*c-s*s)-q*2*c*s
        sin2=1-mu*mu
        ratio=1/(1+energy/REST*(1-mu)) if process=='C' else np.ones(n)
        intensity=ratio+1/ratio-sin2+sin2*rotated_q
        raw,next_energy=angular_energy(energy,mu,process,True,rotated_q,sin2)
        weight*=width*raw/np.interp(energy,ENERGY,NORMAL[process])
        q=(sin2+(1+mu*mu)*rotated_q)/np.maximum(intensity,1e-300)
        u=2*mu*rotated_u/np.maximum(intensity,1e-300)
        direction,basis,energy=outgoing,normal,next_energy
    to_face=(h-point[:,2])/direction[:,2]
    end=point+to_face[:,None]*direction
    downstream=dot(end[:,:2],end[:,:2])<=r*r
    weight*=downstream*np.exp(-attenuation(energy)*to_face)
    return weight,energy

def run():
    result={}
    for order in (2,3):
        paths=[''.join(p) for p in itertools.product('CR',repeat=order)]
        repeats=[]
        for seed in range(622,630):
            samples=qmc.Sobol(3*order,scramble=True,seed=seed).random_base2(15)
            estimates=[]
            for path in paths:
                weight,energy=score(path,samples)
                estimates.append(weight[energy<=58].sum()/len(samples))
            repeats.append(estimates)
        values=np.array(repeats)
        total=values.sum(axis=1)
        result[order]=dict(paths=dict(zip(paths,values.mean(axis=0))),total=total.mean(),
                           se=total.std(ddof=1)/np.sqrt(len(total)),replicates=total.tolist())
    return result

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
