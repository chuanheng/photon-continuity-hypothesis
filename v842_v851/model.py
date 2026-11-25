"""Band response for 复合符合选择."""
import json
from v752_v761.response import compute

def run():
    values = compute(9)
    return dict(zip(['v8.42', 'v8.43', 'v8.44', 'v8.45', 'v8.46', 'v8.47', 'v8.48', 'v8.49', 'v8.50', 'v8.51'], values))

if __name__=="__main__":
    print(json.dumps(run(), indent=2))
