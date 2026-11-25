"""Band response for 锗表面非活性层."""
import json
from v752_v761.response import compute

def run():
    values = compute(5)
    return dict(zip(['v8.02', 'v8.03', 'v8.04', 'v8.05', 'v8.06', 'v8.07', 'v8.08', 'v8.09', 'v8.10', 'v8.11'], values))

if __name__=="__main__":
    print(json.dumps(run(), indent=2))
