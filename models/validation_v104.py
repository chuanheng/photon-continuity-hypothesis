"""v1.04 GitHub companion: *restricted* exact-prior SBC, held-out zero-reference
predictive check, and v1.03 hyperproposal ESS sensitivity.
All experiments are synthetic. The exact 34/34 locally tested code is in ZIP.
Full-v1.03 complex-source detector calibration is NOT formally SBC-validated.
"""
import numpy as np
from scipy.special import logsumexp
from scipy.stats import chisquare,binomtest
from models.hyperposterior_v103 import sample_hyper,infer
from models.continuous_calibration_v102 import Setup,simulate

def posterior_optical(k,N=280,c0=.25,contrast=.17,A=.76,points=801):
    if N<1 or not 0<=k<=N or points<20 or not 0<c0-contrast*A<c0<1:
        raise ValueError('physical submodel')
    m=np.linspace(0,1,points)
    p=c0-contrast*A*m
    ll=k*np.log(p)+(N-k)*np.log1p(-p)
    weights=np.exp(ll-logsumexp(ll))
    # Trapezoid-weight the uniform-in-M continuous prior at boundaries.
    weights[[0,-1]]*=.5
    weights/=weights.sum()
    quant=np.interp([.025,.5,.975],np.cumsum(weights),m)
    return m,weights,quant

def exact_submodel_sbc(n=450,draws=49,seed=10401):
    if n<10 or draws<5:raise ValueError('sample sizes')
    rng=np.random.default_rng(seed);ranks=[];covered=[]
    for _ in range(n):
        truth=rng.uniform()
        count=rng.binomial(280,.25-.17*.76*truth)
        grid,w,ci=posterior_optical(int(count))
        post=grid[rng.choice(len(grid),draws,p=w)]
        ranks.append(int(np.sum(post<truth)))
        covered.append(bool(ci[0]<=truth<=ci[2]))
    hist=np.histogram(ranks,bins=np.linspace(-.5,draws+.5,11))[0]
    test=chisquare(hist)
    k=int(sum(covered))
    ci=binomtest(k,n).proportion_ci()
    return {'n':n,'posterior_draws':draws,'ranks':ranks,'rank_histogram':hist.tolist(),
        'chi2':float(test.statistic),'rank_uniformity_p':float(test.pvalue),
        'covered':k,'coverage':k/n,'coverage_ci_exact95':[float(ci.low),float(ci.high)]}

def heldout_predictive(rec,seed=1041,ntrain=70,draws=75,reps=160):
    z=np.asarray(rec['z'])
    if len(z)<ntrain+10 or ntrain<5 or draws<10 or reps<20:raise ValueError('holdout')
    train=z[:ntrain];hold=z[ntrain:]
    h=sample_hyper({'y':rec['y'],'z':train},draws,seed)
    theta=h['theta'];w=h['weights'];rng=np.random.default_rng(seed+1)
    observed=np.array([np.sum(abs(hold-x[2])>3*np.exp(x[1])) for x in theta])
    ii=rng.choice(len(theta),size=reps,p=w)
    simulated=[int(np.sum(abs(rng.normal(theta[j,2],np.exp(theta[j,1]),size=len(hold))-theta[j,2])>
                          3*np.exp(theta[j,1]))) for j in ii]
    stat=float(w@observed)
    return {'n_holdout':len(hold),'observed_stat':stat,
       'prediction_mean':float(np.mean(simulated)),
       'predictive_probability_ge_observed':float(np.mean(np.asarray(simulated)>=stat)),
       'hyper_ess':h['ess']}

def ppc_audit(n=75,seed=10420,fraction=.09,outlier_sd=.85):
    if n<2 or not 0<=fraction<=1:raise ValueError('count/fraction')
    result={}
    for case in ('gaussian','holdout_contaminated'):
        points=[]
        for i in range(n):
            rec=simulate(seed+101*i,Setup())
            if case=='holdout_contaminated':
                rng=np.random.default_rng(seed+900001+101*i)
                z=rec['z'].copy();mask=rng.random(len(z)-70)<fraction
                z[70:]+=mask*rng.normal(0,outlier_sd,size=len(mask));rec['z']=z
            points.append(heldout_predictive(rec,seed+20000+i))
        result[case]={'n':n,'flagged_p_le_0_05':sum(p['predictive_probability_ge_observed']<=.05 for p in points),
           'mean_observed_tail':float(np.mean([p['observed_stat'] for p in points])),
           'mean_predicted_tail':float(np.mean([p['prediction_mean'] for p in points])),
           'rows':points}
    return result

def proposal_audit(n=32,draws=90,seed=10480,scales=(.8,1.4,2.2)):
    from models.hyperposterior_v103 import sample_hyper
    rows=[]
    for i in range(n):
        rec=simulate(seed+31*i,Setup());row={'seed':seed+31*i}
        for scale in scales:
            # v1.03 companion uses sample_hyper(scale=...) and infer; fit's
            # default proposal scale is separate, so ESS is tested directly.
            h=sample_hyper(rec,draws,seed+100000+19*i,scale=scale)
            row[str(scale)]={'ESS':float(h['ess']),'hyper_mean':np.sum(h['weights'][:,None]*h['theta'],axis=0).tolist()}
        rows.append(row)
    return {'n':n,'draws':draws,'scales':list(scales),
       'summary':{str(s):{'median_ESS':float(np.median([r[str(s)]['ESS'] for r in rows])),
                         'min_ESS':float(np.min([r[str(s)]['ESS'] for r in rows]))}
         for s in scales},'rows':rows}
