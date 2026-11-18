# v2.52–v2.61 十轮研究：隐藏光子标签的可访问操作代数与交换对称探针

**研究日期：2026-11-18。** 实际执行 Python/NumPy 有限维数学研究；10/10 本地测试通过。**不是完整 QED、没有真实光子实验，没有永久身份的独有物理预测。**

## 逐轮报告

| 版本 | 研究主题 | 独立报告 |
|---|---|---|
| v2.52 | 不可访问标签的操作代数 | [查看](./v252_accessible_algebra_zh.md) |
| v2.53 | 交换对称集体耦合 | [查看](./v253_symmetric_coupling_zh.md) |
| v2.54 | 探针 X 基标签读出 | [查看](./v254_probe_readout_zh.md) |
| v2.55 | 统计混合与通道线性 | [查看](./v255_linearity_mixture_zh.md) |
| v2.56 | 当前探针不可读的相干量 | [查看](./v256_coherence_invisible_zh.md) |
| v2.57 | 通过探针 Z 基读取分布 | [查看](./v257_second_probe_observable_zh.md) |
| v2.58 | 极化与耦合强度的 Fisher 秩亏 | [查看](./v258_identifiability_theta_m_zh.md) |
| v2.59 | 两种标签输入合成计数 | [查看](./v259_synthetic_probe_counts_zh.md) |
| v2.60 | 探针能量交换审查 | [查看](./v260_energy_bookkeeping_zh.md) |
| v2.61 | 永久身份独有性最终判断 | [查看](./v261_observability_decision_zh.md) |

## 模型

两个相同玻色子各有二能级内部标签，四维计算空间中只允许对称玻色子子空间（维数 3）。定义交换算符 S，集体内部量 A=(Z⊗I+I⊗Z)/2，及无量纲探针耦合 H_int=A⊗Y_probe，U(θ)=exp(−iθH_int/2)，θ=0.8。这个有限维集体内部态耦合通过 [H_int,S⊗I_probe]=0 的交换对称测试，但**不是**满足光子 QED 规范与洛伦兹约束的具体新场论。

## 十轮核心结果

1. 未耦合时不同标签状态的探针约化态相同（误差 0），信息在该受限操作代数下不可测。
2. 随意的“第一光子槽位 Z”算符与 S 对易子 Frobenius 范数 2.828427；集体对称 A 与 S 的对易子为 0。
3. θ=0.8 下，标签 |00>、|ψ+>=(|01>+|10>)/√2、|11> 分别给探针 X+ 概率 **0.858678、0.500000、0.141322**。
4. 对称合法输入态的统计混合遵守通道线性：先混合再演化与先演化再平均误差 0。
5. 相干 (|00>+|11>)/√2 与其去相干混合态在当前探针完整输出态上迹距离约 **1.25e−16**；该耦合无法访问这组相干相位。
6. 对称 |ψ+> 与等权 |00>/<11| 混合有相同 <A>=0，但探针 Z+ 分别是 **1.000000、0.848353**，可检验集体内态分布的差异 0.151647；属于普通高阶内部量统计。
7. 一组 X+ 读数 P=(1+m sinθ)/2 对未知 m、θ 的 Fisher 矩阵秩为 1，N=1000、m=0.6 下非零特征值 846.0863；不能只凭该读数区分标签极化与耦合强度变化。
8. NumPy seed=20261118，每组 1000 次二项合成采样，|00> 与 |11> 的 X+ 事件数 **858、153**，简单假设 KL=1.29436 nats/事件；这只能区分普通内部标签的极化，不是永久身份的证据。
9. 相互作用 H_int 与探针自由能代理 H_probe=I⊗Z 不对易，范数 4；尚未说明驱动能量、局域性、洛伦兹协变性和完整 QED 一致性，**不能宣称所有守恒律已经满足**。
10. 若标签真正可测，它必须作为物理内部自由度进入标准量子理论；当前集体耦合没有对光子永久个体身份的操作定义及独有场论预测。

## 复现实验

- [GitHub Python 模型](../models/identity_operator_v252_v261.py)
- [GitHub 十项回归测试](../tests/test_identity_operator_v252_v261.py)

```bash
python -m models.identity_operator_v252_v261
python -m unittest discover -s tests -p 'test_identity_operator_v252_v261.py' -v
```

依赖 Python3、NumPy。在会话中另附原始本地计算快照 ZIP（`model.py`, `test_model.py`, `results.json`, `summary.csv`, `tests.log`），已实际执行 10/10 测试。GitHub 版本按同一数学模型与参数整理，未单独验证 GitHub CI。

## 理论背景

- [Quantum Statistics of Identical Particles](https://link.springer.com/article/10.1007/s10701-022-00596-4)
- [Graduate Quantum Mechanics: Identical Particles](https://etneil.github.io/grad_qm_lec_notes/identical_particles.html)
- [The Hong–Ou–Mandel experiment review](https://link.springer.com/article/10.1140/epjd/s10053-022-00525-0)

**后续优先级：** 建立与身份标签相互作用的真实光学实现、对称性/能量来源、标准内部模式对照和跨吸收—再发射的严格操作定义。在这一条件成立之前，不应把“探针能够测出集体内部态”改写成“永久光子身份得到验证”。
