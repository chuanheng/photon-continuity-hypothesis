"""v1.05 GitHub companion: heldout Gaussian vs Student-t sensor forecasting.
Synthetic zero-phase reference data. Outliers affect TRAIN and HELDOUT.
This does not constitute a robust full quantum-optical latent-state posterior.
"""
import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm,t

def sensor_data(seed,ntrain=100,nhold=80,contamination=0.,extra_sd=.9):
    if ntrain<10 or nhold<5 or not 0<=contamination<=1 or extra_sd<0:
        raise ValueError('physical sampling configuration')
    rng=np.random.default_rng(seed);n=ntrain+nhold
    x=rng.normal(.015,.15,n)
    flags=rng.random(n)<contamination
    x+=flags*rng.normal(0,extra_sd,n)
    return x[:ntrain],x[ntrain:],flags[:ntrain],flags[ntrain:]

def fit_predict(train,hold):
    train=np.asarray(train,float);hold=np.asarray(hold,float)
    if len(train)<10 or len(hold)<5:raise ValueError('sample sizes')
    center=float(train.mean());sd=max(float(train.std()),1e-5)
    fun=lambda v:-np.sum(t.logpdf(train,4,loc=v[0],scale=np.exp(v[1])))
    opt=minimize(fun,[np.median(train),np.log(sd)],method='L-BFGS-B',
        bounds=[(-5,5),(-8,3)])
    if not opt.success:raise RuntimeError('Student-t fit did not converge')
    ng=float(np.mean(norm.logpdf(hold,loc=center,scale=sd)))
    st=float(np.mean(t.logpdf(hold,4,loc=opt.x[0],scale=np.exp(opt.x[1]))))
    return {'normal_log_score':ng,'student_log_score':st,
        'student_minus_normal':st-ng,'normal_scale':sd,'student_scale':float(np.exp(opt.x[1]))}

def audit(n=180,seed=105500):
    answer={}
    for contamination in (0.,.08):
        records=[]
        for i in range(n):
            train,hold,flags_tr,flags_h=sensor_data(seed+431*i,contamination=contamination)
            fit=fit_predict(train,hold)
            records.append({**fit,'train_outliers':int(flags_tr.sum()),
                'holdout_outliers':int(flags_h.sum())})
        delta=np.array([z['student_minus_normal'] for z in records])
        answer[str(contamination)]={'n':n,
            'mean_student_minus_normal':float(delta.mean()),
            'median_student_minus_normal':float(np.median(delta)),
            'student_wins':int(np.sum(delta>0)),
            'records':records}
    return answer
