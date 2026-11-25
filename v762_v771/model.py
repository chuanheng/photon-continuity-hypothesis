"""Band response for 全覆盖铜片."""
import json
from v752_v761.response import compute

def run():
    values = compute(1)
    return dict(zip(['v7.62', 'v7.63', 'v7.64', 'v7.65', 'v7.66', 'v7.67', 'v7.68', 'v7.69', 'v7.70', 'v7.71'], values))

if __name__=="__main__":
    print(json.dumps(run(), indent=2))
