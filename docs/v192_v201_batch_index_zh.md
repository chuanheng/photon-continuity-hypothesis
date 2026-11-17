# 光子连续性假说：v1.92–v2.01 十轮理论综合审查

**研究日期：2026-11-17。** 这是合成统计和解析守恒反例。实际运行的 Python 3 / NumPy / SciPy 计算通过 10 项单元测试；**不是实际光学实验，标准模型参数边界未得到 QED 或独立测量支持，不是永久身份的实验验证。**

## 十轮研究目录

| 版本 | 主题 | 报告 |
|---|---|---|
| v1.92 | 历史候选机制分类 | [查看](./v192_candidate_taxonomy_zh.md) |
| v1.93 | 封闭系统能量守恒筛选 | [查看](./v193_energy_conservation_filter_zh.md) |
| v1.94 | 不可观测身份与环境等价 | [查看](./v194_observational_equivalence_filter_zh.md) |
| v1.95 | 自由标准模型的 KL 轮廓 | [查看](./v195_profile_likelihood_null_family_zh.md) |
| v1.96 | 独立参考的有界标准模型 | [查看](./v196_independent_reference_constraint_zh.md) |
| v1.97 | 5000 次精确二项检验 | [查看](./v197_exact_test_5000_zh.md) |
| v1.98 | 参考标定漂移的退化 | [查看](./v198_calibration_drift_stress_zh.md) |
| v1.99 | 三终点多重检验控制 | [查看](./v199_multiple_testing_control_zh.md) |
| v1.100 | 固定种子合成验证 | [查看](./v200_seeded_pseudoexperiment_zh.md) |
| v2.01 | 论文级综合审查结论 | [查看](./v201_synthesis_gate_zh.md) |

## 复现

- [统一计算代码](../models/identity_synthesis_v192_v201.py)
- [10 项回归测试](../tests/test_identity_synthesis_v192_v201.py)
- 本次对话提供完整独立本地运行数据包（batch.py、test_batch.py、results.json、summary.csv、README.md）；GitHub 仓库的源码是同一公式与种子整理版。

```bash
python -m models.identity_synthesis_v192_v201
python -m unittest discover -s tests -p 'test_identity_synthesis_v192_v201.py' -v
```

## 本批次核心数值

- 8 类历史机制经过守恒与操作等价分类；目前未找到永久身份独有动力学。
- 合成候选点击概率 0.08。若标准模型可以取 q=0.08，则最小 KL=0。
- **人为施加的**参考上界 q∈[0.03,0.06] 下，最小 KL=0.0032288569928560565 nats/event，最优标准边界 q=0.06。这个上界**没有**来自真实实验或 QED 的物理约束，不能视为正式新物理证据。
- N=5000、单侧 α≤0.05：拒绝阈值 ≥329 次点击，实际 α=0.04632877151629593；p=0.08 下精确功效 0.9999358296578974。
- 上界漂移 0.005、0.01、0.015、0.02 后，轮廓 KL 约为 0.001732119、0.000736469、0.000176620、0；当上界放宽至 0.08 时标准模型与候选再度完全等价。
- 三个预先选定检验的 Bonferroni 单项 α=0.05/3：拒绝阈值 ≥337，实际 α=0.016063662149256176，单项精确功效 0.9996486825763494。
- RNG seed=20261117 的单次 N=5000 合成二项采样：点击数 383，对 q=0.06 边界的单侧 p 值约 1.1130892427544515×10^-6；这是**模拟数据，未真实预注册**。

## 科学判断

这十轮没有证明光子永久身份，反而表明正式论文中必须清晰区分：

1. 拒绝某个固定的简单零假设；
2. 拒绝由独立校准和物理守恒限制的复合标准模型；
3. 拒绝 QED 在具体实验条件下允许的所有合理背景模型；
4. 证实某个新理论的**独有且预先提出**的可检验概率差。

本批次最多展示了第 2 层在一个**假设上界成立的合成统计例子**中如何实现；不能直接推论已经达到第 3 或第 4 层。

## 参考

- Englbrecht et al. (2024), [Indistinguishability of Identical Bosons from a Quantum Information Theory Perspective](https://doi.org/10.1103/PhysRevLett.132.050201), PRL 132, 050201。
- Suzuki et al. (2020), [Quantum state estimation with nuisance parameters](https://doi.org/10.1088/1751-8121/ab8b78), J. Phys. A 53, 453001。
- Probing Context-Dependent Errors in Quantum Processors (2019), [PRX 9 021045](https://doi.org/10.1103/PhysRevX.9.021045)。

**下一工作优先级：** 不再将版本迭代本身视作证据。优先寻找可定义的新身份场与操作、跨吸收/再发射的物理标记、完整 QED 标准基线和真正独立、可复核的标定边界；如均无法建立，应维持“不可辨识、未获独有支持”的结论。
