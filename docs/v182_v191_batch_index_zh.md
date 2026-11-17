# v1.82–v1.91 十轮连续研究：操作等价、耗散量子通道与新物理门槛

**日期：2026-11-17。研究性质：** 标准有限维量子信息模型和合成统计计算。十项本地回归测试通过。**从未进行真实光学实验，未构造永久光子身份的独有 QED 预测。**

| 版本 | 研究主题 | 独立报告 |
|---|---|---|
| v1.82 | 身份旁观标签的操作等价 | [阅读](./v182_spectator_label_no_go_zh.md) |
| v1.83 | Kraus 分解的非唯一性 | [阅读](./v183_kraus_nonuniqueness_zh.md) |
| v1.84 | 振幅阻尼通道合法性 | [阅读](./v184_amplitude_damping_cptp_zh.md) |
| v1.85 | 守恒的系统—环境酉扩张 | [阅读](./v185_unitary_dilation_energy_zh.md) |
| v1.86 | 非幺正通道的观测见证 | [阅读](./v186_nonunitality_witness_zh.md) |
| v1.87 | 限制随机酉模型的 KL 区分 | [阅读](./v187_restricted_model_KL_zh.md) |
| v1.88 | 固定假设证据积累 | [阅读](./v188_evidence_accumulation_zh.md) |
| v1.89 | 精确二项检验 | [阅读](./v189_exact_binomial_power_zh.md) |
| v1.90 | 完整标准振幅阻尼拟合 | [阅读](./v190_standard_damping_profile_zh.md) |
| v1.91 | 永久身份的可证伪性门槛 | [阅读](./v191_operational_falsifiability_gate_zh.md) |

## 核心科学结果

**两种不同问题必须区分：**

1. 标准随机酉噪声 `E(I/2)=I/2`，而标准振幅阻尼 γ=0.36 预测输出 `diag(0.68,0.32)`，因此两者可由最大混合输入和 Z 测量区分。Bernoulli KL=0.06627772298751897 nat/event。
2. 但振幅阻尼本来就是标准量子理论的一类非幺正系统通道。若允许标准模型含该机制并拟合 γ=0.36，则完整单系统量子通道逐项相同，profile KL=0。**拒绝随机酉噪声，不等于证明永久光子身份或拒绝 QED。**

- Kraus 完备性误差 0。
- 4×4 环境扩张的酉性数值误差 2.66×10^-17，偏迹后与振幅阻尼通道的四个算符基的输出误差 0，总激发数守恒。
- 随机酉通道保持最大混合态，振幅阻尼输出相对最大混合态的迹距离 0.18。
- N=200、单侧精确二项检验 α≤.05，拒绝阈值 ≥113 次基态，真实第一类错误概率 0.0384188161、备择下精确功效 0.9997480618。
- NumPy RNG seed=20261117，200 次备择模拟产生 140 次基态、样本对数似然比 16.270631807。
- **纯身份旁观标签零影响；没有任何新身份特有的实验证据。**

## 复现操作

[仓库模型](../models/identity_channel_audit_v182_v191.py) · [仓库测试](../tests/test_identity_channel_audit_v182_v191.py)

```bash
python -m models.identity_channel_audit_v182_v191
python -m unittest discover -s tests -p 'test_identity_channel_audit_v182_v191.py' -v
```

Python3、NumPy、SciPy。本对话另提供本地运行压缩包，包含 `batch.py`、`test_batch.py`、`results.json`、`summary.csv`、`README.md`；GitHub 模型为同数学模型和参数的整理实现，但不与本地源脚本逐字节相同。**GitHub CI 状态尚未单独核实。**

## 理论门槛与研究判断

下一批次不应仅按版本号增加合成量子通道的参数。需要显式定义不违反相同玻色子交换对称、场论约束并且会影响某个可访问实验概率的“永久身份”动力学。只有对标准 QED 和合理物质/环境/探测干扰机制进行公平拟合之后，仍存在定量且可实验排除的差异，才具有新理论的科学意义。

## 参考

- Stinespring 扩张非唯一性和连续性：https://doi.org/10.1109/TIT.2008.917696
- 量子通道 Choi/Kraus 标准理论：https://quantum-journal.org/papers/q-2020-11-30-368/
