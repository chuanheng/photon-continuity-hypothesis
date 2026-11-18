# v2.32–v2.41：十轮随机量子轨迹、条件态非线性与无信号审查

**研究日期：2026-11-18。** 共完成十个独立主题，已在 Python/NumPy 实际运行 10 项对应测试，**10/10 通过**。本报告涉及标准开放量子信息理论，**不是完整 QED、没有真实实验，没有永久光子身份独有证据。**

## 十轮研究目录

| 版本 | 主题 | 独立研究报告 |
|---|---|---|
| v2.32 | Kraus 完备性 | [查看](./v232_kraus_consistency_zh.md) |
| v2.33 | 测量条件态跳跃概率 | [查看](./v233_conditional_jump_statistics_zh.md) |
| v2.34 | 概率加权平均的 CPTP 通道 | [查看](./v234_ensemble_CPTP_reconstruction_zh.md) |
| v2.35 | 轨迹展开的非唯一性 | [查看](./v235_unravelling_nonuniqueness_zh.md) |
| v2.36 | Bell 态局域操作无信号 | [查看](./v236_bell_no_signalling_channel_zh.md) |
| v2.37 | Alice 局域酉操作 | [查看](./v237_alice_local_operation_zh.md) |
| v2.38 | 不同输入系综的仿射一致性 | [查看](./v238_remote_ensemble_affinity_zh.md) |
| v2.39 | 20,000 次随机轨迹计数 | [查看](./v239_trajectory_monte_carlo_zh.md) |
| v2.40 | 双步通道和轨迹一致性 | [查看](./v240_two_round_trajectory_consistency_zh.md) |
| v2.41 | 永久光子身份结论与局限 | [查看](./v241_identity_falsifiability_verdict_zh.md) |

## 总结性数学结果

采用振幅阻尼强度 γ=0.36 的 K0=diag(1,sqrt(1−γ))、K1=[[0,sqrtγ],[0,0]]；初始 |+>=(|0>+|1>)/sqrt2。第 i 项测量条件概率 p_i=Tr(K_iρK_i†)，归一化条件态 ρ_i=K_iρK_i†/p_i；**虽然归一化条件更新可非线性，但非选择性演化 Σ_i p_iρ_i=Σ_iK_iρK_i† 是线性 CPTP 通道**。

- Kraus 完备性误差 0；跳跃概率 0.18，未跳跃 0.82。
- 按概率加权的条件态与直接通道输出迹距离 0，X 正端口概率 0.9。
- 另一 Kraus 展开 L±=(K0±K1)/sqrt2 的分支概率为 0.8、0.2，其第一个条件态与原展开第一个条件态迹距离约 0.20952909，但两个展开的非选择性输出态迹距离 5.55e−17。
- Bell 态上对 Bob 做非选择性局域量子通道，Alice 的边缘统计迹距离变化为 0；Alice 局域施加 X 后 Bob 无条件态变化仍为 0。
- 将 I/2 用 Z 本征态或 X 本征态等概率分解，分别按分支施加同一个固定线性通道后平均，输出迹距离约 1.11e−16；与被 v2.31 排除的确定性逐纯态非线性映射不同。
- NumPy seed=20261118、n=20,000 multinomial 随机轨迹标签：实际跳跃 3593 次（理论期望 3600）。
- 两次连续固定通道直接演化，与先枚举第一轮轨迹再加权施加第二轮通道的输出迹距离 1.39e−17；两轮后的 X 正端口概率 0.82。

**物理结论**：这种“随机非线性条件态 + 线性平均通道”是标准量子轨迹理论的常规结构，不是永久身份独有预测。它显示一种在有限量子信息模型内与无信号要求兼容的修复方法，但没有建立光子永久身份的场论模型。该批次验证不构成实际的洛伦兹协变或完整 QED 证明。

## GitHub 和本地复现

- [GitHub 整理版研究模型](../models/identity_trajectories_v232_v241.py)
- [GitHub 十项单元测试](../tests/test_identity_trajectories_v232_v241.py)

```bash
python -m models.identity_trajectories_v232_v241
python -m unittest discover -s tests -p 'test_identity_trajectories_v232_v241.py' -v
```

依赖 Python3/NumPy。另有本次对话可下载的完整独立本地运行快照：`model.py`、`test_model.py`、`results.json`、`summary.csv`、`tests.log` 和 `README.md`。两者使用相同模型与参数，源文件并非逐字节完全一致。GitHub CI 尚未独立核验。

## 理论背景

- [Quantum trajectory framework for general time-local master equations](https://doi.org/10.1038/s41467-022-31533-8), Nature Communications, 2022.
- [An Introduction to Monitored Quantum Systems and Quantum Trajectories: Spectrum, Typicality, and Phases](https://academic.oup.com/ptep/article/2026/5/052A01/8530537), PTEP, 2026.

## 下一步

后续应从无限轮次的标准量子通道示例转向严格识别永久身份特有的额外动力学及其物理独立性：明确新物理态、可寻址操作、玻色交换/规范/能动量/洛伦兹约束，并计算与完整 QED 及合理噪声模型竞争时的非零可观测差异。若无法做到，论文应将永久身份保留为不可操作检验的解释性假说。
