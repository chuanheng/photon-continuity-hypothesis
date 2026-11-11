"""Synthetic spectral identifiability with uncertain background normalization.
All counts and templates are invented; NOT a radiation transport prediction.
"""
import math
BASELINE=(80.,110.,170.,300.,550.,2400.)
TEMPLATE=(.28,.32,.24,.11,.04,.01)

def information(baseline=BASELINE,template=TEMPLATE,fractional_prior=None):
    """Profiled Fisher information for A at zero in mu_i=beta*B_i+A*T_i."""
    if len(baseline)!=len(template) or not baseline:
        raise ValueError("invalid lengths")
    if any(not math.isfinite(b) or b<=0 for b in baseline):
        raise ValueError("baseline must be positive finite")
    if any(not math.isfinite(t) or t<0 for t in template):
        raise ValueError("template must be nonnegative finite")
    if not math.isclose(sum(template),1,abs_tol=1e-10):
        raise ValueError("template must sum to one")
    if fractional_prior is not None and (not math.isfinite(fractional_prior) or fractional_prior<=0):
        raise ValueError("prior sigma must be positive finite")
    iaa=sum(t*t/b for t,b in zip(template,baseline))
    iab=sum(template)
    ibb=sum(baseline)+(0 if fractional_prior is None else 1/fractional_prior**2)
    return max(0.,iaa-iab**2/ibb)

def amplitude_for_local_snr(z,fractional_prior=None):
    """Local Gaussian sensitivity proxy, NOT a discovery threshold."""
    if not math.isfinite(z) or z<=0:
        raise ValueError("z must be positive finite")
    i=information(fractional_prior=fractional_prior)
    return math.inf if i==0 else z/math.sqrt(i)

if __name__=="__main__":
    print("SYNTHETIC STUDY ONLY; no measured spectra or calibrated significance")
    for label,sigma in (("free",None),("10%",.1),("3%",.03),("1%",.01),("0.1%",.001)):
        print(f"{label}: Ieff={information(fractional_prior=sigma):.9f}, A_3proxy={amplitude_for_local_snr(3,sigma):.2f}")
