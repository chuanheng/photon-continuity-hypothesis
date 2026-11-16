# v1.22–v1.31：光子连续性假说，十轮机制与可证伪性批次

**完成日期：** 2026-11-16；**研究性质：** 解析推导和合成数值模拟；非真实实验，未验证永久身份。与 v1.12–v1.21 不同，此批次重点从统计标定转向**新动力学机制必须满足什么条件**。

## 十轮入口

| 版本 | 完成主题 | 研究报告 |
|---|---|---|
| v1.22 | 不可访问身份标签的观测等价 | [报告](./v122_invisible_identity_zh.md) |
| v1.23 | 保留硬光子原能量并激发物质导致守恒冲突 | [报告](./v123_energy_no_go_zh.md) |
| v1.24 | 可守恒的降能出射通道 | [报告](./v124_soft_exit_conservation_zh.md) |
| v1.25 | 三能量等价末态的酉散射构造 | [报告](./v125_unitary_three_channel_zh.md) |
| v1.26 | 含探测效率和暗计数的软光子信号 | [报告](./v126_soft_detection_statistic_zh.md) |
| v1.27 | 标准基线自由拟合使新通道不可辨识 | [报告](./v127_baseline_absorption_zh.md) |
| v1.28 | 单探测档位 Jacobian 秩亏 | [报告](./v128_single_setting_rank_zh.md) |
| v1.29 | 两档已知效率恢复局部满秩 | [报告](./v129_two_efficiency_rank_zh.md) |
| v1.30 | 种子确定的有限样本与近似功效 | [报告](./v130_finite_binomial_power_zh.md) |
| v1.31 | 新物理可证伪性的判定门槛 | [报告](./v131_decision_gate_zh.md) |

## 关键数值

- v1.23：入射硬光子能量 3、出射仍为 3，同时靶激发增加 2，将违反封闭系统能量守恒 2 个单位。
- v1.24–v1.25：软光子能量 1+靶激发能量 2 与初始硬光子能量 3 匹配；三态能量等价子空间可构造严格酉性散射。第一列出射概率 (0.70,0.25,0.05)，独立正交性数值核查误差 2.22e-16。
- v1.26：假设标准软光子出射 b0=0.04、候选 b1=0.055，探测效率 0.7、暗点击 0.01，则点击 p0=0.03772、p1=0.048115，KL(p1||p0)=0.0013727095 nat/轮。
- v1.27：若标准模型的 b0 可以自由拟合，取 b0'=0.055，和候选模型相同，则此单项点击观测的 KL **严格等于 0**。
- v1.28–v1.29：单个已知探测效率下，软出射率 b 和暗计数 d 的观测 Jacobian 秩为 1；两档已知效率 0.7/0.9 且共用同一 d 时，Jacobian 恢复秩 2，JᵀJ 的特征值约 (0.0125024,3.135708)。这不是 Fisher 精度下界。
- v1.30：种子 20261116/20261117，N=10000，每组采样点击计数 414/505；已知参数的简单假设下对数似然比 19.7913，正态近似单侧 α=0.05 功效约 0.99965。允许标准基线拟合后，此功效不成立。
- v1.31：目前**没有身份标签本身的独特可观测预测**。量子光学和一般 QED 中，普通非弹性散射、荧光及探测背景是必须首先排除的解释。

## 运行方式

- [完整标准库 Python 模型](../models/identity_mechanisms_v122_v131.py)
- [十个版本关联的回归测试](../tests/test_identity_mechanisms_v122_v131.py)

```bash
python3 models/identity_mechanisms_v122_v131.py
python3 -m unittest discover -s tests -p 'test_identity_mechanisms_v122_v131.py' -v
```

完整 GitHub 回归测试尚待 CI 或有仓库代码的执行环境单独确认；本次对关键数值（KL、点击计数、Jacobian、Householder 正交性）完成了独立 Python 核查和十项版本结论的一致性检查。

## 参考背景与科学边界

- ENS Advanced QM: https://www.phys.ens.psl.eu/~nascimbene/enseignement/aqm/ （相同粒子的标签与观测对称性）
- NIST: https://www.nist.gov/publications/indistinguishability-single-photons-dissimilar-single-photon-sources （标准光子不可区分性测量）
- Menssen et al. PRL 118,153603 (2017) https://doi.org/10.1103/PhysRevLett.118.153603 （多光子干涉与内部模式）

本批次提出的三能级软光子支路不构成永久光子身份的新理论，也没有给出实际 QED 截面。若未来拟提出新可证伪预测，必须给出与标准 QED 明确不同且在干扰参数剖面化后仍不同的观测分布。
