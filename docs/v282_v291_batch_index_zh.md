# v2.82–v2.91 十轮研究：独立标定、统计满秩、漂移及永久身份不可辨识性

**2026-11-19。** 十轮数值研究已实际执行：本地 Python 3/NumPy 模型、2,000 次 Monte Carlo 重复、10/10 回归测试通过。**这些结果全部来自合成二项统计模型，不是光学实验、标准 QED 排除证据或永久光子身份的新物理预测。**

## 逐轮研究报告

| 版本 | 研究问题 | 独立中文报告 |
|---|---|---|
| v2.82 | 主测量 Fisher 秩亏 | [查看](./v282_single_readout_fisher_rank_zh.md) |
| v2.83 | 可见度与存储独立参考 | [查看](./v283_two_independent_references_zh.md) |
| v2.84 | 暗/亮探测器标定 | [查看](./v284_detector_dark_bright_calibration_zh.md) |
| v2.85 | 五通道固定种子模拟 | [查看](./v285_seeded_five_channel_experiment_zh.md) |
| v2.86 | Fisher 不确定度与 Monte Carlo 覆盖 | [查看](./v286_fisher_MC_uncertainty_zh.md) |
| v2.87 | 参考漂移的参数偏差 | [查看](./v287_reference_drift_bias_zh.md) |
| v2.88 | 多角度扫描的普通环境等价 | [查看](./v288_multi_theta_standard_relabel_zh.md) |
| v2.89 | 固定标准 vs 复合标准模型 KL | [查看](./v289_composite_null_KL_zh.md) |
| v2.90 | SPAM 与模型规范自由度 | [查看](./v290_SPAM_gauge_physical_interpretation_zh.md) |
| v2.91 | 永久身份独有证据门槛 | [查看](./v291_identity_falsifiability_gate_zh.md) |

## 统一概率模型及参考设计

令可见模式系数 v=.95、普通存储相干 c=.85、额外候选因子 s=.8、探测效率 η=.9、暗计数 d=.01、探针角 θ=.6，主实验的 Bernoulli 点击率为 p=d+(1−d)η(1+vcs cosθ)/2=**0.693025812621701**。单独的四种参考点击概率为：

- 存储参考 (1+c)/2=0.925（5000 次）
- 可见度参考 (1+v)/2=0.975（5000 次）
- 暗计数参考 d=.01（5000 次）
- 亮参考 d+(1−d)η=.901（5000 次）

主实验采样 10000 次。全部参考被人为假定可独立标定、和主实验共享稳定参数，因此这些数学测试**不是实际硬件已达到的标定准确度**。

## 主要实测计算结果（“测”指合成模型统计）

1. 只用主点击读出对五个参数的 Fisher 信息秩为 1。
2. 加两项独立参考概率，概率雅可比秩为 3；加入亮/暗标定后完整 Fisher 秩为 5，数值特征值全正。
3. NumPy default_rng(seed=20261119) 的五组单次合成计数是 **[6947,4603,4875,49,4518]**，估计的 (v,c,s,η,d) 分别约为 (.95,.8412,.807445,.902646,.0098)。
4. Fisher 预测 s 的标准误约 **0.0206026**。2000 次重复模拟经验标准差 **0.0204858**，固定理论 Fisher 正态区间覆盖 **95.3%**。
5. 主实验普通存储系数若从参考 .85 漂移到 .83 而分析仍强制共享 .85，估计的 s 平均值下移到 **0.78220346**（偏差 −0.01779654）。统计标定与物理漂移必须分开审查。
6. 探针角 θ=0,.3,.6,.9 的光学正端口概率分别约为 .823、.80857369、.76658340、.70078002；若标准量子模型允许一个**普通额外环境可见度** r=s=.8，则每一个角度均被准确复现，最大差 0。
7. 错误强行固定 s=1 且不容许环境衰减时，主实验简单 Bernoulli KL=**0.00901883647** nat/次；纳入标准额外环境 r 后，最小 KL=**0**。
8. Fisher 满秩与物理本体可观测性是两回事。即使有效参数 s 在五参数限定模型中能估计，它与普通未观测环境系数仍可操作等价。

## 复现

- [GitHub 整理版计算模型](../models/identity_calibration_v282_v291.py)
- [GitHub 十项测试](../tests/test_identity_calibration_v282_v291.py)

```bash
python -m models.identity_calibration_v282_v291
python -m unittest discover -s tests -p 'test_identity_calibration_v282_v291.py' -v
```

本次对话另提供实际执行的原始模型和测试文件、JSON、CSV 与日志 ZIP 包。GitHub 版本使用相同方程、参数与 RNG 种子，但因结构整理与本地脚本不逐字相同；GitHub CI 尚未独立核验。

## 物理结论与下一步

**没有得到永久光子个体身份独有预测或真实光学实验证据。** 本批次证明理想独立标定可以局部识别五个预先设定的统计参数，却不能排除一个具有相同效应的普通环境物理过程。增加样本、增加角度扫描或改善 Fisher 精度，不会自动赋予 s 永久身份的物理解释。下一批次优先构造实际可测的非标准、交换对称、规范与相对论约束下的新身份动力学；若无法完成，应将假说限定为当前操作集合下无法证伪的本体叙述，而不把参数估计成功当作新物理。

## 相关文献

- Nielsen et al., *Gate Set Tomography*, Quantum 5,557 (2021), https://quantum-journal.org/papers/q-2021-10-05-557/
- *Tomography of Optical Single-Qubit Quantum Memory* (2022), https://link.springer.com/article/10.1134/S0021364022600951
- *Detecting correlated errors in SPAM tomography* (2015), https://doi.org/10.1103/PhysRevA.92.042312
