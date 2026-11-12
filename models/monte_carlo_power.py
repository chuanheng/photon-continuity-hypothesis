"""Monte Carlo power for fixed binned hypotheses; illustrative, not QED."""
import math,random
def probabilities(weights):
    v=tuple(weights)
    if not v or any(not math.isfinite(x) or x<0 for x in v): raise ValueError('invalid weights')
    s=sum(v)
    if not math.isfinite(s) or s<=0: raise ValueError('invalid total')
    return tuple(x/s for x in v)
def detector_response(truth,response):
    p=probabilities(truth); rows=tuple(tuple(r) for r in response)
    if not rows or any(len(r)!=len(p) for r in rows): raise ValueError('shape')
    if any(not math.isfinite(x) or x<0 for r in rows for x in r): raise ValueError('entry')
    if any(not math.isclose(sum(r[j] for r in rows),1,abs_tol=1e-12) for j in range(len(p))): raise ValueError('column sum; include missed-event bin')
    return probabilities([sum(r[j]*p[j] for j in range(len(p))) for r in rows])
def log_likelihood_ratio(counts,null,alternative):
    a,b=probabilities(null),probabilities(alternative)
    if len(a)!=len(b) or len(counts)!=len(a): raise ValueError('shape')
    if any(type(c) is not int or c<0 for c in counts): raise ValueError('counts')
    total=0.
    for n,x,y in zip(counts,a,b):
        if not n: continue
        if x==0 and y==0: raise ValueError('impossible event')
        if x==0: return math.inf
        if y==0: return -math.inf
        total+=n*math.log(y/x)
    return total
def sample_counts(probability,size,rng):
    p=probabilities(probability)
    if type(size) is not int or size<0: raise ValueError('size')
    counts=[0]*len(p)
    for _ in range(size):
        u=rng.random(); cumulative=0.
        for j,w in enumerate(p):
            cumulative+=w
            if u<cumulative or j==len(p)-1:
                counts[j]+=1;break
    return tuple(counts)
def simulate_power(null,alternative,size,repetitions=2000,alpha=.05,seed=1234):
    p0,p1=probabilities(null),probabilities(alternative)
    if len(p0)!=len(p1): raise ValueError('shape')
    if type(size) is not int or size<1 or type(repetitions) is not int or repetitions<20: raise ValueError('simulation size')
    if not math.isfinite(alpha) or not 0<alpha<1: raise ValueError('alpha')
    rng0=random.Random(seed);rng1=random.Random(seed+1)
    null_scores=sorted(log_likelihood_ratio(sample_counts(p0,size,rng0),p0,p1) for _ in range(repetitions))
    critical=null_scores[min(repetitions-1,math.ceil((1-alpha)*repetitions)-1)]
    fpr=sum(x>critical for x in null_scores)/repetitions
    power=sum(log_likelihood_ratio(sample_counts(p1,size,rng1),p0,p1)>critical for _ in range(repetitions))/repetitions
    return {'size':size,'repetitions':repetitions,'alpha':alpha,'critical':critical,'false_positive_rate':fpr,'power':power}
