"""v1.10: Standard quantum-optics Fourier tritter with unitary error and detector loss.
Synthetic calculations; not a persistent-photon identity experiment. Python stdlib only.
"""
import cmath, math
from itertools import permutations, combinations_with_replacement, product
from collections import defaultdict
PERMS=tuple(permutations(range(3)))
OCCS=tuple(combinations_with_replacement(range(3),3))
F=tuple(tuple(cmath.exp(2j*math.pi*j*k/3)/math.sqrt(3) for k in range(3)) for j in range(3))
def unitary(epsilon=0):
    c,s=math.cos(epsilon),math.sin(epsilon)
    return (tuple(c*F[0][k]+s*F[1][k] for k in range(3)),
            tuple(-s*F[0][k]+c*F[1][k] for k in range(3)),F[2])
def gram(r,phi):
    if not 0<=r<=.5:raise ValueError('r outside PSD-safe interval')
    z=r*cmath.exp(1j*phi)
    return ((1,r,z.conjugate()),(r,1,r),(z,r,1))
def output_probabilities(r,phi,epsilon=0):
    u,g=unitary(epsilon),gram(r,phi); p={}
    for out in OCCS:
        a={s:math.prod(u[out[i]][s[i]] for i in range(3)) for s in PERMS}
        norm=math.prod(math.factorial(out.count(k)) for k in range(3))
        v=sum(a[s]*a[t].conjugate()*math.prod(g[s[i]][t[i]] for i in range(3))
              for s in PERMS for t in PERMS)/norm
        if abs(v.imag)>1e-10 or v.real < -1e-10:raise ArithmeticError('invalid probability')
        p[tuple(out.count(k) for k in range(3))]=max(0.,v.real)
    if abs(sum(p.values())-1)>1e-10:raise ArithmeticError('normalization')
    return p
def detected_probabilities(p,eta=(1.,1.,1.)):
    if len(eta)!=3 or any(not 0<=e<=1 for e in eta):raise ValueError('eta')
    d=defaultdict(float)
    for occ,pr in p.items():
        for det in product(*(range(n+1) for n in occ)):
            w=pr
            for n,k,e in zip(occ,det,eta):
                w*=math.comb(n,k)*e**k*(1-e)**(n-k)
            d[det]+=w
    if abs(sum(d.values())-1)>1e-10:raise ArithmeticError('loss normalization')
    return dict(d)
def coarse(p):
    d=defaultdict(float)
    for k,v in p.items():d[tuple(sorted(k,reverse=True))]+=v
    return dict(d)
def tv(p,q):return .5*sum(abs(p.get(k,0)-q.get(k,0)) for k in p.keys()|q.keys())
def kl(p,q):
    if any(q.get(k,0)<=0 for k,v in p.items() if v>0):return float('inf')
    return sum(v*math.log(v/q[k]) for k,v in p.items() if v>0)
def fit_grid(observed,r,grid,epsilon=0,eta=(1,1,1)):
    return min(((phi,kl(observed,detected_probabilities(output_probabilities(r,phi,epsilon),eta)))
               for phi in grid),key=lambda pair:pair[1])
def main():
    r,phi=.3,math.pi/3; eta=(.86,.82,.9)
    for eps,loss in [(0,(1,1,1)),(.08,(1,1,1)),(0,eta),(.08,eta)]:
        p=detected_probabilities(output_probabilities(r,phi,eps),loss)
        q=detected_probabilities(output_probabilities(r,-phi,eps),loss)
        print('epsilon',eps,'eta',loss,'TV',tv(p,q),'KL',kl(p,q),
              'coarse TV',tv(coarse(p),coarse(q)),'coarse KL',kl(coarse(p),coarse(q)))
    observed=detected_probabilities(output_probabilities(r,phi,.08),eta)
    grid=[-math.pi+i*2*math.pi/720 for i in range(721)]
    for r_ref in [.27,.29,.3,.31,.33]:
        print('r_ref',r_ref,'phase_fit',fit_grid(observed,r_ref,grid,.08,eta))
    print('wrong optical matrix',fit_grid(observed,r,grid,0,eta))
    print('mean detected photons',sum(sum(k)*v for k,v in observed.items()))
if __name__=='__main__':main()
