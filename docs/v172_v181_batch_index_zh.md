# v1.72–v1.81 十轮研究：多时间量子过程与环境记忆

**完成日期 2026-11-17。** 真实执行 NumPy 合成量子通道计算，并通过 10/10 项本地单元测试。本文不是实际光学实验，更不是永久光子身份的新物理验证。

| 版本 | 核心研究 | 报告 |
|---|---|---|
| v1.72 | Kraus 完备性 | [阅读](./v172_kraus_completeness_zh.md) |
| v1.73 | 多输入态检验 | [阅读](./v173_four_input_tomography_zh.md) |
| v1.74 | Choi 完全正性 | [阅读](./v174_choi_positive_zh.md) |
| v1.75 | 单时刻等价 | [阅读](./v175_one_time_equivalence_zh.md) |
| v1.76 | 两时间相关性 | [阅读](./v176_temporal_correlation_zh.md) |
| v1.77 | 回波操作 | [阅读](./v177_spin_echo_control_zh.md) |
| v1.78 | 四种中间操作 | [阅读](./v178_multi_interventions_zh.md) |
| v1.79 | 有限样本对数似然比 | [阅读](./v179_finite_sample_lr_zh.md) |
| v1.80 | 含记忆标准模型对照 | [阅读](./v180_standard_nonmarkov_profile_zh.md) |
| v1.81 | 永久身份可证伪门槛 | [阅读](./v181_operational_decision_gate_zh.md) |

## GitHub 复现

- [研究代码](../models/identity_process_v172_v181.py)
- [十项回归测试](../tests/test_identity_process_v172_v181.py)

```bash
python -m models.identity_process_v172_v181
python -m unittest discover -s tests -p 'test_identity_process_v172_v181.py' -v
```

需要 Python3 与 numpy。本地原始运行文件 batch.py、test_batch.py、results.json 一并保存在会话 ZIP 中；仓库中的源代码为同公式、同种子和同指标的整理版本。

## 本批次数值

单步退相干角 θ=0.6，c=cosθ=0.8253356149096783。
- Kraus 完备性误差 1.1102230246251565e−16。
- 四个输入态的标准相位翻转通道数值差 1.1102230246251565e−16。
- 归一化 Choi 态特征值 (0,0,0.08733219254516075,0.9126678074548389)，迹约 1。
- 单步 |+> 输入正端口概率 0.9126678074548387。
- 双步、无中间控制：固定环境 P+=0.6811788772383363，逐次独立重置 P+=0.8405894386191679，KL(static||reset)=0.07775274549369485 nat/次。
- X 回波：固定环境 P+≈1，重置环境 P+=0.8405894386191679。
- I,X,Y,Z 四个中间酉操作下，隐藏二能级环境与标准准静态经典随机环境对应的系统输出差 0。
- N=1000、numpy seed=20261117、固定环境生成模型：694 次正端口，样本 log LR=66.1698149853132，期望 logLR=77.75274549369485。

## 关键科学判断

这组实验**可以区分固定相关噪声和逐次重置噪声**。但允许标准模型使用实验内固定的准静态随机失谐后，全部模拟可访问统计与隐藏寄存器相同，模型最小 KL=0。因此这是开放量子系统记忆的演示，**不是永久身份的独有证据**。

**限制：** 模型是两态退相干，不是三光子干涉或者实际吸收—再发射过程；没有构造可寻址的光子身份自由度、相对论规范场或与全部标准 QED 候选的系统比较；没有做真实多时间过程张量重建。四种中间酉操作并不等于全部量子仪器操作的实验层析。

## 学术参考

- Pollock et al., [Operational Markov Condition for Quantum Processes](https://doi.org/10.1103/PhysRevLett.120.040405), PRL 120, 040405 (2018).
- Pollock et al., [Non-Markovian quantum processes: Complete framework and efficient characterization](https://doi.org/10.1103/PhysRevA.97.012127), PRA 97, 012127 (2018).

## 下一批次建议

v1.82–v1.91 首先尝试引入真正不被标准环境/量子存储重新参数化吸收的可操作机制。若无法做到，转向梳理假说的可检验性不可行边界和既有实验证据，而不是无止境增加版本号。
