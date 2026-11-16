"""Run from repo root: python -m experiments.run_v077"""
import json
from pathlib import Path
from models.absorption_memory_v077 import summary
if __name__ == "__main__":
    results={"version":"v0.77","status":"finite-dimensional toy model, not QED","results":summary()}
    output=Path("results/absorption_memory_v077_recomputed.json")
    output.parent.mkdir(exist_ok=True,parents=True)
    output.write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(results,indent=2,ensure_ascii=False))
