# v1.12–v1.21 十轮连续研究索引（2026-11-16）

本批次**连续完成十个研究问题**，共享标准量子光学的 Fourier tritter 三光子基线和固定合成参数；全部结果为数学/计算实验，**不是实际光学实验，不支持宣称已验证光子永久身份**。

| 版本 | 中文报告 | 研究主题 |
|---|---|---|
| v1.12 | [查看](./v112_finite_sample_phase_zh.md) | 80 次有限样本相位 MLE / 覆盖率 |
| v1.13 | [查看](./v113_joint_hom_mle_zh.md) | 35 次 HOM 联合 MLE |
| v1.14 | [查看](./v114_reference_mismatch_zh.md) | 模式重叠错设的总体偏差 |
| v1.15 | [查看](./v115_nuisance_inflation_zh.md) | 未知仪器参数的 Fisher 代价 |
| v1.16 | [查看](./v116_budget_sensitivity_zh.md) | 三组基线的预算分配 |
| v1.17 | [查看](./v117_detector_readout_zh.md) | 四种读出类型的信息损失 |
| v1.18 | [查看](./v118_low_overlap_phase_zh.md) | 低重叠极限与相位退化 |
| v1.19 | [查看](./v119_hom_drift_joint_zh.md) | 参考漂移的联合伪真实值 |
| v1.20 | [查看](./v120_phase_sign_budget_zh.md) | 相位符号区分的样本尺度 |
| v1.21 | [查看](./v121_falsifiability_gate_zh.md) | 永久身份可证伪性门槛 |

## 方法与复现

- 模型来源：[v1.10](../models/three_photon_v110.py)、[v1.11](../models/three_photon_v111.py)；本批次使用同一理论模型增加 Monte Carlo 和不同读出/标定的分析。
- 独立 Python 运行：固定 RNG 种子 `20261116`，80 次 oracle 相位 MLE、35 次 HOM 联合 MLE、286×3 个预算比较、两类总体失配优化，以及各类 Fisher/KL 检验。通过 **12 项本地回归测试**。
- 完整新批次运行脚本 `batch.py`、`test_batch.py`、机器可读 `results.json`、`summary.csv` 作为本次 ChatGPT 会话的可下载可复现实验压缩包提供；**这些四个文件尚未同步到 GitHub 仓库**。仓库内只已提交各轮报告，因此请勿将仅报告提交等同于代码存档。
- 环境：Python 3、NumPy、SciPy。运行：`python batch.py results.json`；`python -m unittest test_batch.py -v`。
- 所有结果都仅针对明确定义的简化装置、先验参数和实验计数；不得把假设中的永久光子身份替换为普通的可测模式重叠或闭环相位。

## 研究门槛

下一批次不宜仅仅围绕已知量子干涉模型调参。必须先给出永久身份假说相对于标准理论的**不同、定量、守恒、可证伪**预测，并检查是否已被现有实验排除。若没有独有预测，应明确维持“在当前可操作测量下不可区分”的状态。
