"""v2.12-v2.21: nonlinear Bloch toy model and ensemble equivalence tests.
Pure mathematics. NOT a photon identity theory. Standard library Python 3.
Run: python -m models.identity_nonlinear_v212_v221
"""
import math,json,random
LAMBDA=.4
def evolve(r,lam=LAMBDA):
    x,y,z=r
    c=1-2*lam*x*x
    return (c*x,c*y,z)
def mix(ensemble):
    return tuple(sum(w*r[i] for w,r in ensemble) for i in range(3))
def length(r):return math.sqrt(sum(x*x for x in r))
def distance(a,b):return length(tuple(x-y for x,y in zip(a,b)))/2
def plus(r):return (1+r[0])/2
def KL(p,q):
    if p==q:return 0.
    return p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))
def ensemble_evolve(states):return mix([(w,evolve(r)) for w,r in states])
def main():
    # Both input ensemble states average to the maximally mixed state I/2.
    A=[(.5,(1.,0.,0.)),(.5,(-1.,0.,0.))]
    B=[(1/3,(1.,0.,0.)),(1/3,(-.5,0.,math.sqrt(3)/2)),
       (1/3,(-.5,0.,-math.sqrt(3)/2))]
    outA,outB=ensemble_evolve(A),ensemble_evolve(B)
    r=mix([(.5,(1.,0.,0.)),(.5,(0.,0.,1.))])
    nonlinear=evolve(r)
    affine=mix([(.5,evolve((1.,0.,0.))),(.5,evolve((0.,0.,1.)))])
    # Positivity is actually guaranteed analytically for 0<=lambda<=1/2,
    # since 0<=1-2 lambda*x*x<=1: x/y contract and z stays fixed.
    rng=random.Random(4102);min_eigenvalue=1.
    for _ in range(5000):
        v=[rng.gauss(0,1) for _ in range(3)]
        magnitude=math.sqrt(sum(x*x for x in v))
        radius=rng.random()**(1/3)
        state=tuple(radius*x/magnitude for x in v)
        min_eigenvalue=min(min_eigenvalue,(1-length(evolve(state)))/2)
    pA,pB=plus(outA),plus(outB)
    eta,dark=.85,.02
    vA=dark+(1-dark)*eta*pA;vB=dark+(1-dark)*eta*pB
    n=1000;rg=random.Random(20261117)
    kA=sum(rg.random()<vA for _ in range(n))
    kB=sum(rg.random()<vB for _ in range(n))
    phat=(kA+kB)/(2*n)
    z=(kA/n-kB/n)/math.sqrt(phat*(1-phat)*2/n)
    return {
     'v2.12':{'candidate_classes':['inert label','standard CPTP','nonlinear toy','contextual preparation'],'identity_specific':False},
     'v2.13':{'affine_law':'E(sum w rho)=sum w E(rho) for fixed linear channels'},
     'v2.14':{'lambda':LAMBDA,'map':'(x,y,z)->((1-2lambda*x*x)x,(1-2lambda*x*x)y,z)'},
     'v2.15':{'sampled_minimum_eigenvalue':min_eigenvalue,'positivity_for_0_to_half':True},
     'v2.16':{'nonlinear_of_mixture':nonlinear,'mixture_of_images':affine,'trace_distance':distance(nonlinear,affine)},
     'v2.17':{'input_A':mix(A),'input_B':mix(B),'output_A':outA,'output_B':outB,'P_plus_A':pA,'P_plus_B':pB,'trace_distance':distance(outA,outB)},
     'v2.18':{'KL_B_to_A':KL(pB,pA),'expected_log_LR_at_1000':1000*KL(pB,pA)},
     'v2.19':{'shared_affine_channel_matches_both':False,'minimax_trace_distance':distance(outA,outB)/2},
     'v2.20':{'eta':eta,'dark':dark,'P_click_A':vA,'P_click_B':vB,'click_KL_B_to_A':KL(vB,vA),'n_each':n,'clicks_A':kA,'clicks_B':kB,'z_statistic':z},
     'v2.21':{'no_signaling_verified':False,'ordinary_preparation_errors_excluded':False,'unique_photon_identity_prediction':False}
    }
if __name__=='__main__':print(json.dumps(main(),ensure_ascii=False,indent=2))
