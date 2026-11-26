"""Two-to-one random access memory with independently chosen readout."""
from itertools import product
import json
import numpy as np
from scipy.stats import binom

WORDS = np.array(list(product([-1, 1], repeat=2)))
X = np.array([[0.,1.],[1.,0.]])
Z = np.diag([1.,-1.])

def classical(weights):
    scores = []
    for encoding in product([0,1], repeat=4):
        advantage = sum(weights @ abs(WORDS[np.array(encoding)==message].sum(axis=0))
                        for message in [0,1])
        scores.append(.5 + advantage/8)
    return float(max(scores))

def encoded(weights, axes, shift=(0,0)):
    probabilities = []
    directions = []
    for word in WORDS:
        vector = (word * weights) @ axes
        direction = vector/np.linalg.norm(vector)
        directions.append(direction)
        probabilities.append((1 + word*(axes @ direction + shift))/2)
    return float(np.mean(np.array(probabilities) @ weights)), directions, probabilities

def run():
    w = np.array([.5,.5])
    axes = np.eye(2)
    ideal, directions, table = encoded(w,axes)
    biased = np.array([.8,.2])
    tilted = np.array([[1.,0.],[.5,np.sqrt(.75)]])
    cutoff = next(k for k in range(201) if binom.sf(k-1,200,.75)<=.01)
    swap = np.eye(4)[[0,2,1,3]]
    transferred = []
    for word, (x,z) in zip(WORDS,directions):
        rho = (np.eye(2)+x*X+z*Z)/2
        joint = swap @ np.kron(rho,np.diag([1,0])) @ swap.T
        memory = np.trace(joint.reshape(2,2,2,2),axis1=0,axis2=2)
        transferred.append([(1+s*np.trace(memory@op))/2 for s,op in zip(word,[X,Z])])
    accepted = [a == word[0] for word in WORDS for a in [word[0]]]
    return dict(classical=classical(w),qubit=ideal,biased_classical=classical(biased),
                biased_quantum=encoded(biased,axes)[0],tilted=encoded(w,tilted)[0],
                dephase=encoded(w,np.diag([.5,1.]))[0],
                damping=encoded(w,np.diag([.8,.64]),np.array([0.,.36]))[0],
                postselected=float(np.mean(accepted)),acceptance=.5,
                leak_fraction=(ideal-classical(w))/(1-classical(w)),critical=cutoff,
                alpha=float(binom.sf(cutoff-1,200,.75)),power=float(binom.sf(cutoff-1,200,ideal)),
                swap_error=float(np.max(abs(np.array(transferred)-table))))

if __name__ == '__main__':
    print(json.dumps(run(),indent=2))
