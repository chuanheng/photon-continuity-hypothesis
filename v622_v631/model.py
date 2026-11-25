"""Recompute the internal model and analyze the separately simulated Geant4 run."""
import json
from pathlib import Path
from scipy.stats import binomtest
from v622_v631.bounds import calculate
from v622_v631.paths import run as paths
from v622_v631.detector import run as detector
from v622_v631.inference import design

def external():
    record=json.loads(Path(__file__).with_name('geant.json').read_text())
    n=record['incident']
    interval=binomtest(record['selected'],n).proportion_ci(.95)
    return dict(**record,per_million=1e6*record['selected']/n,
                exact_95_per_million=[1e6*interval.low,1e6*interval.high])

if __name__=='__main__':
    print(json.dumps(dict(bounds=calculate(),paths=paths(),detector=detector(),
                          design=design(),external=external()),indent=2))
