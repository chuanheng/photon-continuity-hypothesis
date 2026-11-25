"""Band response for 串联铝铜."""
import json
from v752_v761.response import compute

def run():
    values = compute(2)
    return dict(zip(['v7.72', 'v7.73', 'v7.74', 'v7.75', 'v7.76', 'v7.77', 'v7.78', 'v7.79', 'v7.80', 'v7.81'], values))

if __name__=="__main__":
    print(json.dumps(run(), indent=2))
