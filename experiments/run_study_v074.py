"""Reproduce v0.74 summary from the GitHub repository root."""
import json
from pathlib import Path
from models.gauge_redundancy_v074 import summary

if __name__ == "__main__":
    result = {
        "version": "v0.74",
        "model": "three-qubit Z2 lattice gauge example",
        "warning": "finite-dimensional toy model, not photon QED",
        **summary(),
    }
    output = Path("results/gauge_redundancy_v074_recomputed.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
