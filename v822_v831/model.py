"""Band response for 近阈值选择."""
import json
from v752_v761.response import compute

def run():
    values = compute(7)
    return dict(zip(['v8.22', 'v8.23', 'v8.24', 'v8.25', 'v8.26', 'v8.27', 'v8.28', 'v8.29', 'v8.30', 'v8.31'], values))

if __name__=="__main__":
    print(json.dumps(run(), indent=2))
