"""Leading-log independent-emission toy, not full QED or a photon identity model."""
import math

def mean_count(beta, lower, upper):
    if not all(map(math.isfinite,(beta,lower,upper))) or beta<0 or lower<=0 or upper<=lower:
        raise ValueError('require finite beta>=0 and 0<lower<upper')
    return beta*math.log(upper/lower)

def exclusive_zero(beta,lower,upper):
    return math.exp(-mean_count(beta,lower,upper))

def poisson_probability(beta,lower,upper,n):
    if not isinstance(n,int) or isinstance(n,bool) or n<0:
        raise ValueError('n must be a nonnegative integer')
    mu=mean_count(beta,lower,upper)
    if mu==0: return 1.0 if n==0 else 0.0
    return math.exp(-mu+n*math.log(mu)-math.lgamma(n+1))

def expected_radiated_energy(beta,lower,upper):
    mean_count(beta,lower,upper)
    return beta*(upper-lower)

def no_resolved_emission(beta, resolution, hard_scale):
    return exclusive_zero(beta,resolution,hard_scale)
