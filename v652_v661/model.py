"""Analyze reproducible transport records and calibrated reference channels."""
import json
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, linprog
from scipy.stats import beta, binom, ks_2samp, norm

ROOT = Path(__file__).parent


def read(name):
    return json.loads((ROOT/name).read_text())


def tag_channels():
    replay = read('tag.json')
    previous = json.loads((ROOT.parent/'v632_v641/trace_622628.json').read_text())
    by_id = {r['event']: r for r in previous['events'] if r['parent'] == 0}
    assert {r['event'] for r in replay['selected']} == set(by_id)
    rows = []
    for threshold in (2., 4., 6.):
        channels = [0, 0, 0]
        for event in replay['selected']:
            losses = [s['before']-s['after'] for s in by_id[event['event']]['steps']]
            channels[0] += event['foil_deposit_keV'] >= threshold
            channels[1] += max(losses) >= threshold
            channels[2] += sum(x >= threshold for x in losses) >= 2
        rows.append(dict(threshold_keV=threshold, foil_sum=channels[0],
                         one_resolved_site=channels[1], two_resolved_sites=channels[2]))
    missing = [60-r['exit_keV']-r['foil_deposit_keV'] for r in replay['selected']]
    return dict(selected=len(missing), threshold_scan=rows,
                max_abs_unaccounted_keV=max(map(abs,missing)))


def accidental_tags():
    # One Poisson accidental process per timing gate, independently of a true tag.
    accidental = -np.expm1(-0.08)
    p, efficiency, f = .4, .8, .02
    ordinary_tag = accidental+(1-accidental)*efficiency
    other_tag = accidental+(1-accidental)*f
    observed = p*ordinary_tag+(1-p)*other_tag
    recovered = (observed-other_tag)/(ordinary_tag-other_tag)
    wrong = (observed-f)/(efficiency-f)
    rng = np.random.default_rng(65301)
    n = 200000
    ordinary = rng.random(n)<p
    detected = rng.random(n)<np.where(ordinary,efficiency,f)
    sampled = np.mean(detected | (rng.poisson(.08,n)>0))
    return dict(gate_hazard=.08, observed=observed, accidentals=accidental,
                corrected=recovered, ignored_accidentals=wrong, simulated=sampled,
                mc_se=np.sqrt(observed*(1-observed)/n))


def profile(total, tag, eps, contamination):
    # q=u+v where u and v are tagged ordinary and candidate rates.
    # LP variables (s,u,v); contamination bounds multiply total-s.
    lo, hi = eps
    a, b = contamination
    A = [[lo,-1,0],[-hi,1,0],[-a,0,-1],[b,0,1]]
    rhs = [0.,0.,-a*total,b*total]
    vertices = []
    for sign in (1,-1):
        fit = linprog([sign,0,0], A_ub=A,b_ub=rhs,A_eq=[[0,1,1]],b_eq=[tag],
                      bounds=[(0,total),(0,None),(0,None)],method='highs')
        if not fit.success:
            raise ValueError(fit.message)
        vertices.append(fit.x.tolist())
    return dict(delta_interval=[total-vertices[1][0],total-vertices[0][0]], witnesses=vertices)


def calibration_design():
    # Independent Bernoulli reference events; same angle and energy selection.
    maxima = []
    for n in range(1,200):
        k = int(binom.isf(.025,n,.36))+1
        power = binom.sf(k-1,n,.90)
        if power >= .9:
            return dict(n=n,k=k,size=binom.sf(k-1,n,.36),power=power,
                        best_smaller=max(maxima),power_at_070=binom.sf(k-1,n,.70))
        maxima.append(power)


def threshold_control():
    # Per stratum maximum of an external iid continuous blank calibration.
    n = int(np.ceil(np.log(.05/3)/np.log(.99)))
    return dict(events_per_stratum=n,union_failure=3*.99**n,
                smaller_union_bound=3*.99**(n-1),
                gaussian_threshold_in_sigma=norm.ppf(.99),
                drifted_tail=norm.sf(norm.ppf(.99)-.4))


def spectroscopy():
    # A calibrated Gaussian energy filter multiplies a Gaussian incident spectrum.
    source, det = .36,.25
    narrow,wide = .04,1.
    def transmitted(v,w):
        return v*w/(v+w)
    measured = [transmitted(source,w)+det for w in (narrow,wide)]
    diff = measured[1]-measured[0]
    fit=brentq(lambda v:transmitted(v,wide)-transmitted(v,narrow)-diff,0.,10.)
    alternative=.16
    offsets=[y-transmitted(alternative,w) for y,w in zip(measured,(narrow,wide))]
    return dict(measured_variances=measured,source_variance=fit,
                common_detector_variance=measured[0]-transmitted(fit,narrow),
                alternative_source_variance=alternative,alternative_detector_variances=offsets)


def transport_comparison():
    nominal,alternate,low,thin=[read(n+'.json') for n in ('nominal','alternative','lowcut','thin')]
    def summarize(r):
        samples=np.asarray(r['single_losses'])
        return dict(count=len(samples),max_loss_keV=float(np.max(samples[:,1])),
                    single_above_2keV=int(np.sum(samples[:,1]>=2)))
    a,b=nominal['single_losses'],alternate['single_losses']
    x=ks_2samp(np.array(a)[:,1],np.array(b)[:,1],method='exact')
    spectra=dict(polarized=summarize(nominal),penelope=summarize(alternate),
                 empirical_KS=x.statistic,unadjusted_p=x.pvalue)
    births=[]
    geometry=[]
    for r in (nominal,low):
        n=r['incident']; k=r['events_with_secondary_gamma']
        births.append(dict(cut_mm=r['cut_mm'],gamma_tracks=r['secondary_gamma_births'],
                           birth_events=k,incident=n,one_sided_975_upper=beta.ppf(.975,k+1,n-k),
                           selected_secondary=sum(e['parent']!=0 for e in r['selected'])))
    from v622_v631.detector import simulate
    for r in (thin,nominal):
        h=r['thickness_mm']/10
        outputs=[simulate(h,.5,3.,s,13).sum(axis=0)[0] for s in range(66010,66014)]
        n=r['incident'];k=sum(e['parent']==0 for e in r['selected'])
        low_ci=beta.ppf(.0125,k,n-k+1) if k else 0.
        hi_ci=beta.ppf(.9875,k+1,n-k)
        geometry.append(dict(thickness_mm=r['thickness_mm'],events=k,incident=n,
                             two_strata_interval=[low_ci,hi_ci],restricted=np.mean(outputs),
                             integration_se=np.std(outputs,ddof=1)/2))
    return spectra,births,geometry


def label_test():
    # Any binary tag is a mixture of the two conditional ordinary tag laws.
    conditional=np.array([[.9,.1],[.25,.75]])
    mixture=np.array([.4,.6])
    base=mixture@conditional
    # Composite affine ordinary response across two control settings.
    a=np.array([.9,.15]);b=np.array([.25,.8])
    outside=np.array([base[0],.44])
    t=np.clip(np.dot(outside-b,a-b)/np.dot(a-b,a-b),0.,1.)
    foot=b+t*(a-b)
    return dict(single_setting=base.tolist(),ordinary_mixture=mixture.tolist(),
                two_settings=outside.tolist(),nearest_mix=t,
                distance=np.linalg.norm(outside-foot),distance_with_free_second=0.)


def run():
    spectra,births,geometry=transport_comparison()
    return dict(zip(['v6.'+str(i) for i in range(52,62)],
                    [tag_channels(),accidental_tags(),
                     {k:profile(5.,1.8,limits,(0.,.25)) for k,limits in
                      [('calibrated',(.75,.95)),('widened',(.36,.95))]},
                     calibration_design(),threshold_control(),spectroscopy(),
                     spectra,births,geometry,label_test()]))


if __name__=='__main__':
    print(json.dumps(run(),indent=2,allow_nan=False))
