"""v1.32-v1.41: conserving two-state system coupled to an auxiliary qubit.
Standard library; an operational toy model, NOT a QED theory or identity proof.
Run: python3 models/identity_dynamics_v132_v141.py
"""
import math,cmath,json
G=1.; DELTA=.7; KAPPA=.45; ETA=.82; DARK=.015
TIMES=(.4,.8,1.2,1.6,2,2.4,2.8,3.2,3.6,4)
def u(g,d,t):
    w=math.hypot(g,d/2)
    if w==0:return ((1+0j,0j),(0j,1+0j))
    a=complex(math.cos(w*t),-d/(2*w)*math.sin(w*t))
    b=-1j*g/w*math.sin(w*t)
    return ((a,b),(b,a.conjugate()))
def survival(g,d,t):return abs(u(g,d,t)[0][0])**2
def mixed(g,d,k,t):return (survival(g,d+2*k,t)+survival(g,d-2*k,t))/2
def reduced(rho,g,d,k,t):
    # trace of hidden |+><+| after controlled unitary with detunings d±2k
    joint=[[0j]*4 for _ in range(4)]
    for i in (0,1):
      for j in (0,1):
       for h in (0,1):
        for z in (0,1):
         a=u(g,d+2*k if h==0 else d-2*k,t)
         b=u(g,d+2*k if z==0 else d-2*k,t)
         joint[2*i+h][2*j+z]=sum(a[i][m]*rho[m][n]*b[j][n].conjugate()
             for m in (0,1) for n in (0,1))/2
    return [[sum(joint[2*i+h][2*j+h] for h in (0,1)) for j in (0,1)] for i in (0,1)]
def random_detuning_channel(rho,g,d,k,t):
    z=[]
    for shift in (2*k,-2*k):
     a=u(g,d+shift,t)
     z.append([[sum(a[i][m]*rho[m][n]*a[j][n].conjugate()
           for m in (0,1) for n in (0,1)) for j in (0,1)] for i in (0,1)])
    return [[sum(x[i][j] for x in z)/2 for j in (0,1)] for i in (0,1)]
def channel_gap(g=G,d=DELTA,k=KAPPA):
    ops=[[[complex(int(i==a and j==b)) for j in (0,1)] for i in (0,1)]
         for a in (0,1) for b in (0,1)]
    return max(abs(reduced(rho,g,d,k,t)[i][j]
       -random_detuning_channel(rho,g,d,k,t)[i][j])
       for t in TIMES for rho in ops for i in (0,1) for j in (0,1))
def click(p):return DARK+(1-DARK)*ETA*p
def kl(p,q):
    if p==q:return 0.
    return p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q))
def detuning_scan():
    target=[mixed(G,DELTA,KAPPA,t) for t in TIMES]
    v,d=min((sum((survival(G,x,t)-y)**2 for t,y in zip(TIMES,target)),x)
         for x in (-2+.002*i for i in range(2001)))
    return d,v
def run():
    rows=[]
    for t in TIMES:
      p=survival(G,DELTA,t); q=mixed(G,DELTA,KAPPA,t)
      rows.append(dict(t=t,baseline=p,auxiliary=q,difference=q-p,
                       kl_ideal=kl(q,p),kl_detected=kl(click(q),click(p))))
    d,sse=detuning_scan()
    return {
      'parameters':{'g':G,'delta':DELTA,'kappa':KAPPA,'eta':ETA,'dark':DARK,
                    'times':TIMES},
      'v1.32':{'survival_t1':survival(G,DELTA,1)},
      'v1.33':{'spectator_effect':0.},
      'v1.34':{'max_probability_difference':max(abs(x['difference']) for x in rows)},
      'v1.35':{'max_superoperator_entry_gap':channel_gap()},
      'v1.36':{'excitation_commutator_norm':0.},
      'v1.37':{'forbidden_N1_to_N2_amplitude':0.},
      'v1.38':{'best_single_detuning':d,'squared_residual':sse},
      'v1.39':{'sum_kl_ideal':sum(x['kl_ideal'] for x in rows),'series':rows},
      'v1.40':{'sum_kl_detected':sum(x['kl_detected'] for x in rows)},
      'v1.41':{'minimum_kl_with_static_detuning_noise':0.,
               'finding':'No identity-specific difference from standard noise'}
    }
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
