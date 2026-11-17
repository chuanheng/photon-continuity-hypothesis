# v2.12–v2.21 十轮研究：非线性候选、系综可区分性与物理一致性

**研究日期：2026-11-17。** 本批次**实际运行** Python 标准库的数学数值计算与 10 项独立回归测试（10/10 通过）。所有数据均为合成模型，**不是实际光学实验，也不是光子永久身份新预测**。

## 十轮目录

| 版本 | 独立研究主题 | 详细报告 |
|---|---|---|
| v2.12 | 历史机制审计与新机制门槛 | [阅读](./v212_hypothesis_scope_zh.md) |
| v2.13 | 标准 CPTP 仿射混合条件 | [阅读](./v213_affine_quantum_channel_zh.md) |
| v2.14 | 非线性退相干候选定义 | [阅读](./v214_nonlinear_candidate_definition_zh.md) |
| v2.15 | 输出态正性与局限 | [阅读](./v215_state_positivity_zh.md) |
| v2.16 | 混合态仿射性反例 | [阅读](./v216_affinity_violation_zh.md) |
| v2.17 | 同密度矩阵不同系综输出 | [阅读](./v217_same_density_different_ensembles_zh.md) |
| v2.18 | 系综概率 KL 与样本尺度 | [阅读](./v218_ensemble_statistical_distance_zh.md) |
| v2.19 | 共享线性通道的最小误差 | [阅读](./v219_affine_null_lower_bound_zh.md) |
| v2.20 | 探测损耗与随机采样 | [阅读](./v220_detector_and_seeded_counts_zh.md) |
| v2.21 | 无信号风险及永久身份判断 | [阅读](./v221_nosignaling_identity_verdict_zh.md) |

## 可重复运行

- [研究 Python 模型](../models/identity_nonlinear_v212_v221.py)
- [十项回归测试](../tests/test_identity_nonlinear_v212_v221.py)

```bash
python -m models.identity_nonlinear_v212_v221
python -m unittest discover -s tests -p 'test_identity_nonlinear_v212_v221.py' -v
```

仅需 Python 标准库。会话另有完整本地原始版本 `batch.py`、`test_batch.py`、`results.json`、`summary.csv` 与 README 的 ZIP 包。GitHub 为同一数学方法和种子整理的代码，并非逐字节相同文件。

## 主要数学结果

使用单量子比特 Bloch 向量 r=(x,y,z)，取非线性 N_λ(r)=((1−2λx²)x,(1−2λx²)y,z)，λ=0.4。

1. 取 0≤λ≤0.5，对每个输入 Bloch 球内态都保持正性、迹一。这**不能**推出通道的完全正性、适用于纠缠态的扩展或真实物理动力学。
2. 非线性算符不满足仿射混合律。对 |+>、|0> 的等权混合，`N(mix)` 与 `mix(N)` 的输出迹距离 **0.15**。
3. 两种具有完全相同输入密度算符 I/2 的纯态系综：A=|+>,|-> 各一半；B 的 Bloch 向量 (1,0,0)、(−0.5,0,√3/2)、(−0.5,0,−√3/2) 各占三分之一。分支非线性作用后平均，X 正端口概率 A=**0.5**，B=**0.4**，输出迹距离 **0.1**。
4. 这两组输出对任何**共享的、准备方式独立的线性 CPTP** 通道，都无法同时拟合；任一公共拟合输出态相对两者的最大迹距离至少 **0.05**。但是任何实际制备差异、初始环境相关性或控制串扰都必须在物理层面先排除。
5. 理想 KL(Bern(.4)||Bern(.5))=**0.02013551355** nat/次。设置 η=0.85、暗计数 d=0.02 后，可见点击概率 0.4365 和 0.3532，KL≈0.01438270311。
6. 固定种子 20261117、每组 n=1000，合成点击数 A=464、B=373，合并方差两比例 z≈4.12481，**不是现实实验结果**。
7. 非线性系综演化面临**无超光速信号条件**的严重理论挑战，尚未构造与纠缠和远端制备兼容的自洽演化。即使这个数学候选与固定 CPTP 通道不同，它也没有任何光子永久身份专属的动力学推导或真实观测证据。

## 新候选状态与论文写法

建议将本批次作为论文的**非线性扩展反例/一致性检验**章节，而不是当作新理论的成功构造。明确说明 `N_λ` 是人为选择的非线性玩具映射，其逐态正性不足以获得合法量子场论。最优先的下一阶段任务是构造远端制备/复合系统上的一致规则并检验无信号要求；如果不成立，应在理论上排除该候选，而不是继续调整其统计显著性。

## 独立理论背景

- Simon, Bužek & Gisin (2001), *No-Signaling Condition and Quantum Dynamics*, [PRL 87,170405](https://doi.org/10.1103/PhysRevLett.87.170405)
- Halvorson (2004), *Remote preparation of arbitrary ensembles and quantum bit commitment*, [arXiv quant-ph/0310001](https://arxiv.org/abs/quant-ph/0310001)
- [IBM Quantum Learning — Quantum channels](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/quantum-channels/quantum-channel-basics)
