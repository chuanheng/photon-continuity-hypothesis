"""v1.08: analytic identifiability demonstration; NOT an apparatus simulation."""
import math

def fisher(theta, q, n=1000, m=0):
    """X~Binomial(n,theta*q), Y~Binomial(m,q); theta,q in (0,1)."""
    p = theta * q
    factor = n / (p * (1 - p))
    a = factor * q*q
    b = factor * theta*q
    c = factor * theta*theta + m/(q*(1-q))
    det = a*c - b*b
    eigen_min = (a+c-math.sqrt((a-c)**2+4*b*b))/2
    return a,b,c,det,eigen_min

def pseudo_true_theta(theta,q_main,q_reference):
    return theta*q_main/q_reference

def gram_permanent(r,phase):
    """Equicorrelation magnitudes r<1/2 ensure Gram positive definite."""
    return 1 + 3*r*r + 2*r**3*math.cos(phase)

def main():
    theta,q,n=.7,.8,1000
    for m in [0,100,1000,10000]:
        a,b,c,d,e=fisher(theta,q,n,m)
        sd = math.sqrt(c/d) if m else float('inf')
        print(f"m={m}, det={d:.6f}, eigmin={e:.6f}, CRLB_SD={sd:.6f}")
    for shift in [-.05,0,.05]:
        estimate=pseudo_true_theta(theta,q,q+shift)
        print(f"reference_shift={shift:+.3f}, theta_asymptotic={estimate:.6f}, bias={estimate-theta:+.6f}")
    for phase in [0,math.pi/2,math.pi]:
        print(f"phase={phase:.6f}, Gram_permanent={gram_permanent(.3,phase):.6f}")

if __name__ == '__main__':
    main()
