"""Elementary photon-number statistics; not a photon-continuity model."""
import math

def g2_zero(probabilities):
    """g^(2)(0) = <n(n-1)>/<n>^2 for a photon-number distribution."""
    if not probabilities or any(not math.isfinite(p) or p < 0 for p in probabilities):
        raise ValueError("invalid probabilities")
    if not math.isclose(sum(probabilities), 1.0, rel_tol=0, abs_tol=1e-10):
        raise ValueError("probabilities must sum to one")
    mean = sum(n*p for n,p in enumerate(probabilities))
    if mean == 0:
        raise ValueError("vacuum has undefined normalized g2")
    factorial = sum(n*(n-1)*p for n,p in enumerate(probabilities))
    return factorial/(mean*mean)

def fock_distribution(n):
    if not isinstance(n,int) or n<0:
        raise ValueError("n must be nonnegative integer")
    return [0.0]*n+[1.0]

def cross_covariance(joint):
    """Covariance of two binary detector click variables, for a 2x2 joint table."""
    if len(joint)!=2 or any(len(row)!=2 for row in joint):
        raise ValueError("joint distribution must be 2x2")
    flat=[p for row in joint for p in row]
    if any(not math.isfinite(p) or p<0 for p in flat) or not math.isclose(sum(flat),1,abs_tol=1e-10):
        raise ValueError("invalid joint probabilities")
    p_a=joint[1][0]+joint[1][1]
    p_b=joint[0][1]+joint[1][1]
    return joint[1][1]-p_a*p_b

if __name__=="__main__":
    print("Fock n=1:",g2_zero(fock_distribution(1)))
    print("Fock n=2:",g2_zero(fock_distribution(2)))
    print("Independent binary clicks covariance:",cross_covariance([[.25,.25],[.25,.25]]))
