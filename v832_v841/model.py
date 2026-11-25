"""Band response for 有限分辨率能窗."""
import json
from v752_v761.response import compute

def run():
    values = compute(8)
    return dict(zip(['v8.32', 'v8.33', 'v8.34', 'v8.35', 'v8.36', 'v8.37', 'v8.38', 'v8.39', 'v8.40', 'v8.41'], values))

if __name__=="__main__":
    print(json.dumps(run(), indent=2))
