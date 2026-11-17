# v2.22–v2.31 十轮研究：非线性候选的远端制备与无信号条件审查

**完成日期：2026-11-17。** 本批次基于 Bell 双量子比特纯态和两种合法 Alice 远端 POVM 解析构造及数值验证，**不是实际光学实验、没有证明现实中能够超光速通信，也不是永久光子身份的新预测。**

## 十轮详细报告

| 版本 | 主题 | 报告 |
|---|---|---|
| v2.22 | Bell 态与远端制备前提 | [查看](./v222_bell_pair_zh.md) |
| v2.23 | 二结果远端制备 | [查看](./v223_two_outcome_steering_zh.md) |
| v2.24 | 三结果远端 POVM | [查看](./v224_three_outcome_povm_zh.md) |
| v2.25 | 无条件本地密度矩阵一致性 | [查看](./v225_equal_reduced_density_zh.md) |
| v2.26 | 逐分支非线性导致概率差 | [查看](./v226_nonlinear_branch_difference_zh.md) |
| v2.27 | 无信号条件与理论冲突 | [查看](./v227_conditional_superluminal_signalling_zh.md) |
| v2.28 | 精确二项检验与样本尺度 | [查看](./v228_exact_binomial_test_zh.md) |
| v2.29 | 非线性强度敏感性 | [查看](./v229_lambda_sensitivity_zh.md) |
| v2.30 | 密度矩阵演化修复的代价 | [查看](./v230_density_only_repair_tradeoff_zh.md) |
| v2.31 | 候选拒绝与永久身份判定 | [查看](./v231_no_go_and_identity_status_zh.md) |

## 核心推导

定义两个远端制备的 Bob 纯态系综：

- A = {(1/2, Bloch(+1,0,0)),(1/2, Bloch(−1,0,0))}；
- B = {(1/3, Bloch(1,0,0)),(1/3, Bloch(−1/2,0,+√3/2)),(1/3, Bloch(−1/2,0,−√3/2))}。

两组 **Bob 未条件化密度矩阵相同，都为 I/2**。

取共同 Bell 态 |Φ+>=(|00>+|11>)/√2。对每个目标状态 ρ_i 和权重 w_i，Alice 可使用 E_i=2w_iρ_i^T 作为其 POVM 效果算符，以在 Bob 端远端制备相应的条件纯态（Alice 不向 Bob 透露单次测量结果）。在此显式构造中：

- A POVM 完备性误差 0，各分支权重 1/2；
- B POVM 完备性误差 1.11×10^-16，各分支权重 1/3，最小效果特征值约 0；
- Bob 未条件化密度矩阵的两方案迹距离 0。

使用 v2.14 的纯态分支非线性映射 N_λ(x,y,z)=((1−2λx²)x,(1−2λx²)y,z)，λ=0.4。**假设对每一个远端制备分支分别作用再求和**，得 X 正端口概率 P_A=0.5、P_B=0.4。两种输出态迹距离 0.1，KL(Bern(.4)||Bern(.5))=0.02013551355 nats/event。

因此，如果 Alice 的本地测量选择不需通过经典通信就能控制 Bob 的分支演化结果，这一候选规则将在通常遥远类空间隔的条件下形成超光速信号。**这是一条有明确定义假设的理论冲突，不是真实通信实验，不自动适用于所有非线性理论。**

## 有限样本与强度

- 1000 次独立样本，单侧精确二项检验 H0:p=0.5 vs H1:p=0.4，目标 α≤0.05：拒绝阈值点击数≤473，真实错误率 0.04684364574，理论功效 0.99999874518。NumPy 固定种子 20261117 的两组 1000 次合成点击数为 485 和 377。
- λ∈[0,0.5] 时，这两组系综预测 P_A=0.5、P_B=0.5−λ/4；λ=0 时该信号消失。
- 改为只作用于 Bob 的未条件化密度矩阵时，两组局域输出均 P=0.5，该远端通信路径消失，但它无法同时保持逐纯态分支演化的混合一致性。任意单一公共输出相对两组目标态的最大迹距离至少 0.05。

## 审查结论

**v2.14–v2.21 的确定性、逐纯态系综分支非线性映射在标准纠缠远端制备、Born 统计和无超光速信号要求同时成立时不合格。** 它本来就不是由光子永久身份的微观动力学推导而来，因此该候选被审查排除并不等于永久光子身份已被普遍证明不存在。项目依然没有物理一致、标准 QED 不能重新拟合的独有身份预测。

## 复现文件

- [GitHub 整理版研究模型](../models/identity_remote_steering_v222_v231.py)
- [GitHub 十项测试](../tests/test_identity_remote_steering_v222_v231.py)

```bash
python -m models.identity_remote_steering_v222_v231
python -m unittest discover -s tests -p 'test_identity_remote_steering_v222_v231.py' -v
```

依赖 NumPy、SciPy。独立本地运行文件 study.py、test_study.py、results.json、summary.csv、tests.log、README.md 可通过本对话 ZIP 下载；本地 10/10 测试**实际执行且全部通过**。GitHub 整理版与本地脚本为同一模型、同一参数与主要计算路径，但不是逐字节相同文件；GitHub CI 尚未单独核验。

## 文献

- Simon, Bužek & Gisin (2001), [No-Signaling Condition and Quantum Dynamics](https://doi.org/10.1103/PhysRevLett.87.170405)
- Halvorson (2004), [Remote preparation of arbitrary ensembles and quantum bit commitment](https://arxiv.org/abs/quant-ph/0310001)
- [IBM Quantum: Hughston–Jozsa–Wootters theorem](https://qiskit.qotlabs.org/learning/courses/general-formulation-of-quantum-information/purifications-and-fidelity/purifications)

下一批次若继续，建议研究与无信号条件一致的随机非线性轨迹：**其平均量子通道仍保持线性 CPTP**，并诚实说明这是否能产生超出标准理论的新身份可测预测。
