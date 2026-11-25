"""Band response for 斜射角积分."""
import json
from v752_v761.response import compute

def run():
    values = compute(4)
    return dict(zip(['v7.92', 'v7.93', 'v7.94', 'v7.95', 'v7.96', 'v7.97', 'v7.98', 'v7.99', 'v8.00', 'v8.01'], values))

if __name__=="__main__":
    print(json.dumps(run(), indent=2))
