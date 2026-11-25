"""Band response for 有限敏感厚度."""
import json
from v752_v761.response import compute

def run():
    values = compute(6)
    return dict(zip(['v8.12', 'v8.13', 'v8.14', 'v8.15', 'v8.16', 'v8.17', 'v8.18', 'v8.19', 'v8.20', 'v8.21'], values))

if __name__=="__main__":
    print(json.dumps(run(), indent=2))
