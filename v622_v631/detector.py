"""True versus recorded counts, including beam leakage for a Gaussian response."""
import itertools
import json
import numpy as np
from scipy.special import ndtr
from scipy.stats import qmc
from v622_v631.paths import score
from v602_v611.transport import attenuation

def simulate(h,r,angle,seed,power=14):
    # Column 0 is the true window; columns 1 and 2 fold all energies.
    uncollided=np.exp(-attenuation(60.)*h)
    sigmas=np.array([.5,1.])
    rows=[[0.,*(uncollided*ndtr(-2/sigmas))]]
    for n in (1,2,3):
        samples=qmc.Sobol(3*n,scramble=True,seed=seed).random_base2(power)
        row=np.zeros(3)
        for path in itertools.product('CR',repeat=n):
            weight,e=score(path,samples,h,r,angle)
            row[0]+=np.mean(weight*(e<=58))
            for col,sigma in enumerate(sigmas,1):
                probability=ndtr((58-e)/sigma)-ndtr((35-e)/sigma)
                row[col]+=np.mean(weight*probability)
        rows.append(row.tolist())
    return np.array(rows)

def run():
    out=[]
    for h,r,angle in ((.1,.5,3.),(.05,.25,1.5),(.2,1.,6.)):
        replicates=np.array([simulate(h,r,angle,s) for s in range(630,634)])
        out.append(dict(thickness_cm=h,radius_cm=r,angle_deg=angle,
                        order_rows=replicates.mean(axis=0).tolist(),
                        total=replicates.sum(axis=1).mean(axis=0).tolist(),
                        integration_se= (replicates.sum(axis=1).std(axis=0,ddof=1)/2).tolist()))
    return out

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
