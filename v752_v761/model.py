"""Band response for 全覆盖铝片."""
import json
from v752_v761.response import compute

def run():
    values = compute(0)
    return dict(zip(['v7.52', 'v7.53', 'v7.54', 'v7.55', 'v7.56', 'v7.57', 'v7.58', 'v7.59', 'v7.60', 'v7.61'], values))

if __name__=="__main__":
    print(json.dumps(run(), indent=2))
