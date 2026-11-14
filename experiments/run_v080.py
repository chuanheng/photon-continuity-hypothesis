"""Recompute numerical v0.80 results from the GitHub repository root."""
import json
from pathlib import Path
from models.fair_model_competition_v080 import summary

if __name__ == '__main__':
    r=summary()
    output=Path('results/model_competition_v080_recomputed.json')
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(r,indent=2,ensure_ascii=False))
