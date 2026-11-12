"""Binned conditional event-shape likelihood; not a QED amplitude."""
import math
def normalized_bins(weights):
    if not weights or any(not math.isfinite(v) or v<0 for v in weights): raise ValueError('invalid weights')
    s=sum(weights)
    if not math.isfinite(s) or s<=0: raise ValueError('invalid total')
    return tuple(v/s for v in weights)
def observed_bins(truth_weights,response):
    truth=normalized_bins(truth_weights); n=len(truth)
    if not response or any(len(row)!=n for row in response): raise ValueError('shape')
    if any(not math.isfinite(v) or v<0 for row in response for v in row): raise ValueError('response')
    for j in range(n):
        if not math.isclose(sum(row[j] for row in response),1,rel_tol=1e-12,abs_tol=1e-12): raise ValueError('column sum')
    return normalized_bins([sum(row[j]*truth[j] for j in range(n)) for row in response])
def log_likelihood_ratio(counts,h0,h1):
    if not counts or len(counts)!=len(h0) or len(counts)!=len(h1): raise ValueError('shape')
    if any(not isinstance(c,int) or isinstance(c,bool) or c<0 for c in counts): raise ValueError('counts')
    p0,p1=normalized_bins(h0),normalized_bins(h1); total=0.
    for c,a,b in zip(counts,p0,p1):
        if c==0: continue
        if a==0 and b==0: raise ValueError('impossible both')
        if a==0: return math.inf
        if b==0: return -math.inf
        total+=c*math.log(b/a)
    return total
def kl_divergence(h1,h0):
    p1,p0=normalized_bins(h1),normalized_bins(h0)
    if len(p1)!=len(p0): raise ValueError('shape')
    return sum(a*math.log(a/b) if a and b else (math.inf if a else 0.) for a,b in zip(p1,p0))
