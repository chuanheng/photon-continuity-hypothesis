"""Tetrahedral quantum inputs: all-trial probabilities for a semiquantum game."""
import json
import numpy as np
from scipy.optimize import brentq

I=np.eye(2)
P=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]])
T=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])/np.sqrt(3)
B=(6*np.eye(4)-1)/8
S=np.array([0,1,-1,0])/np.sqrt(2)
SINGLET=np.outer(S,S)
W=np.eye(4)/2-SINGLET

def probes(vectors):
    return (I+np.einsum('ij,jkl->ikl',vectors,P))/2

def table(rho,left=T,right=T):
    # Contraction with two local Phi+ projectors, grouped as probes vs resource.
    return np.array([[np.trace(rho@np.kron(a.T,b.T)).real/4
                      for b in probes(right)] for a in probes(left)])

def score(table_):
    return float(np.sum(B*table_))

def confusion(e):
    return (1-e)*np.eye(4)+e*np.ones((4,4))/4

def accidentals(d):
    # A click of either kind is a success, independent dark bits at each end.
    p=table(SINGLET)
    return (1-d)**2*p+2*d*(1-d)*.25+d*d

def run():
    rng=np.random.default_rng(972981)
    raw=table(SINGLET)
    reconstruction=sum(B[i,j]*np.kron(a.T,b.T) for i,a in enumerate(probes(T)) for j,b in enumerate(probes(T)))
    products=[]
    for u,v in rng.normal(size=(128,2,3)):
        u=u/np.linalg.norm(u);v=v/np.linalg.norm(v)
        projected=np.outer((1+T@u)/2,(1+T@v)/2)
        products.append(abs(score(projected)-(1+u@v)/4))
    flag=np.where(np.eye(4),1.,.25)
    theta=np.deg2rad(70)
    R=np.array([[np.cos(theta),-np.sin(theta),0],[np.sin(theta),np.cos(theta),0],[0,0,1]])
    K=confusion(.18)
    changed=K@raw@K.T
    corrected=np.linalg.solve(K.T,np.linalg.solve(K.T,B).T).T
    eps=.03
    # Draw settings independently of trial history. Importance sampling over pairs.
    weights=abs(B)/abs(B).sum()
    second_uniform=float((B**2*raw*16).sum())
    second_weighted=float((B**2*raw/weights).sum())
    return dict(tetra=dict(score=score(raw),operator_error=float(np.linalg.norm(reconstruction-W))),
                product_error=max(products),uniform_loss=score(.093*raw),
                postselection=dict(raw=score(np.full((4,4),.0625)),conditional=score(.0625/flag)),
                noisy_probe=dict(score=score(table(SINGLET,.8*T,.7*T)),threshold=1/(3*.8*.7)),
                rotation=dict(score=score(table(SINGLET,T,T@R.T)),trace=float(np.trace(R))),
                confusion=dict(uncorrected=score(changed),corrected=float(np.sum(corrected*changed)),
                               amplification=float(np.linalg.norm(np.linalg.inv(K),2)**2)),
                dark_threshold=brentq(lambda d:score(accidentals(d)),0,.5),
                label_sideband=-eps/8,
                pair_sampling=dict(uniform_var=second_uniform-score(raw)**2,weighted_var=second_weighted-score(raw)**2,
                                   absolute_weight=float(abs(B).sum())))

if __name__=='__main__': print(json.dumps(run(),indent=2))
