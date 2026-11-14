"""v1.09: three partially distinguishable photons in a Fourier tritter.
Standard quantum-optics toy model; does NOT test persistent photon identity.
Python standard library only.
"""
from itertools import permutations, combinations_with_replacement
from math import pi, factorial, sqrt, log
import cmath

PERMS = list(permutations(range(3)))
OCCS = list(combinations_with_replacement(range(3), 3))
U = [[cmath.exp(2j*pi*j*k/3)/sqrt(3) for k in range(3)] for j in range(3)]

def gram(r, phase):
    """G_01=G_12=r, G_20=r*exp(i phase); 0<=r<=0.5 ensures PSD."""
    z = r*cmath.exp(1j*phase)
    return [[1,r,z.conjugate()],[r,1,r],[z,r,1]]

def probabilities(r, phase):
    if not (0 <= r <= .5):
        raise ValueError("r must be in [0,0.5]")
    G = gram(r, phase)
    result = []
    for out in OCCS:
        counts = [out.count(k) for k in range(3)]
        divisor = factorial(counts[0])*factorial(counts[1])*factorial(counts[2])
        total = 0j
        for s in PERMS:
            a = 1+0j
            for i in range(3):
                a *= U[out[i]][s[i]]
            for t in PERMS:
                b = 1+0j
                internal = 1+0j
                for i in range(3):
                    b *= U[out[i]][t[i]]
                    internal *= G[s[i]][t[i]]
                total += a*b.conjugate()*internal
        if abs(total.imag)>1e-10 or total.real < -1e-10:
            raise ArithmeticError("nonphysical probability")
        result.append(max(0.0,total.real/divisor))
    if abs(sum(result)-1)>1e-10:
        raise ArithmeticError("not normalized")
    return result

def coarse_distribution(p):
    """Counts by occupation partition: (3),(2+1),(1+1+1)."""
    bunched = sum(v for o,v in zip(OCCS,p) if len(set(o))==1)
    split = sum(v for o,v in zip(OCCS,p) if len(set(o))==2)
    return [bunched,split,1-bunched-split]

def kl(a,b):
    return sum(x*log(x/y) for x,y in zip(a,b) if x>0)

def max_abs_delta(a,b):
    return max(abs(x-y) for x,y in zip(a,b))

def jacobian(r, phase, h=1e-5):
    pr=probabilities(r+h,phase)
    mr=probabilities(r-h,phase)
    pp=probabilities(r,phase+h)
    mp=probabilities(r,phase-h)
    return [((a-b)/(2*h),(c-d)/(2*h)) for a,b,c,d in zip(pr,mr,pp,mp)]

def fisher_multinomial(r,phase,coarse=False):
    p=probabilities(r,phase)
    j=jacobian(r,phase)
    if coarse:
        p=coarse_distribution(p)
        j=[(sum(x for o,(x,_) in zip(OCCS,j) if len(set(o))==k),
            sum(y for o,(_,y) in zip(OCCS,j) if len(set(o))==k))
            for k in [1,2,3]]
    a=sum(x*x/t for t,(x,y) in zip(p,j))
    b=sum(x*y/t for t,(x,y) in zip(p,j))
    c=sum(y*y/t for t,(x,y) in zip(p,j))
    return (a,b,c,a*c-b*b)

def main():
    r,phase=.3,pi/3
    plus=probabilities(r,phase)
    minus=probabilities(r,-phase)
    print("FULL OUTPUT PROBABILITIES")
    for o,p in zip(OCCS,plus):
        print(tuple(o.count(k) for k in range(3)),f"{p:.8f}")
    print("sum",sum(plus))
    print("full KL",kl(plus,minus))
    print("full TV",sum(abs(x-y) for x,y in zip(plus,minus))/2)
    print("max delta",max_abs_delta(plus,minus))
    print("coarse+",coarse_distribution(plus))
    print("coarse-",coarse_distribution(minus))
    print("coarse KL",kl(coarse_distribution(plus),coarse_distribution(minus)))
    print("per-event Fisher (r,phi)",fisher_multinomial(r,phase))
    print("r=0 phase-invariance",max_abs_delta(probabilities(0,0),probabilities(0,phase)))

if __name__=="__main__":
    main()
