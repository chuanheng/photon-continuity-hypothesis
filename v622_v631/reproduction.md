# 复现环境与输入

在项目根目录运行。内部模型使用已入库的两个 xraylib 4.3.0 表。对于外部引擎，安装 geant4-pybind==0.1.3。GEANT4_DATA_DIR 指向解包后包含以下四个子目录的目录。

| 数据子目录 | 官方压缩包 MD5 |
|---|---|
| G4EMLOW8.8 | 328330009df633f7e9b3a9f445745298 |
| G4ENSDFSTATE3.0 | c500728534ce3e9fb2fefa0112eb3a74 |
| G4PARTICLEXS4.2 | b63341cc97a472b04ff607b094493174 |
| PhotonEvaporation6.1.2 | d80ba9bdefcf9e23487a26adfa273304 |

先用真实引擎生成 geant.json，再运行内部积分及二项区间计算。设计计算读取已保存的 detector.json。Notebook 从源码重算上述内部积分并核对输出。

```bash
export OPENBLAS_NUM_THREADS=1
python -m v622_v631.geant 5000000 v622_v631/geant.json --seed 622628
python -m v622_v631.bounds > v622_v631/bounds.json
python -m v622_v631.paths > v622_v631/paths.json
python -m v622_v631.detector > v622_v631/detector.json
python -m v622_v631.inference > v622_v631/inference.json
python -m v622_v631.model > v622_v631/results.json
PYTHONPATH=. python tools/execute_research_notebook.py v622_v631/reproduce.ipynb
```

[Geant4 偏振康普顿物理手册](https://geant4.web.cern.ch/documentation/dev/prm_html/PhysicsReferenceManual/electromagnetic/polarized_incident/livermore_polarizedcompton.html) · [CERN 数据文件](https://geant4-data.web.cern.ch/datasets/)
