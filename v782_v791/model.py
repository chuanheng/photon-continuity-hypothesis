"""Band response for 带孔铜片."""
import json
from v752_v761.response import compute

def run():
    values = compute(3)
    return dict(zip(['v7.82', 'v7.83', 'v7.84', 'v7.85', 'v7.86', 'v7.87', 'v7.88', 'v7.89', 'v7.90', 'v7.91'], values))

if __name__=="__main__":
    print(json.dumps(run(), indent=2))
