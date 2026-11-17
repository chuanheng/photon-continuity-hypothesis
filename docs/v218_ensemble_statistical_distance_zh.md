# v2.18：差异的理论统计尺度

**日期：2026-11-17。科学边界：** 本报告属于有限维单量子比特非线性映射的数学反例审查。它**不是光子场论机制、真实实验或永久光子身份的预测/证据**。统一代码：[模型](../models/identity_nonlinear_v212_v221.py)；[十项测试](../tests/test_identity_nonlinear_v212_v221.py)。本地原始版本使用 Python 标准库、固定随机种子，10 项单元测试全部通过。

v2.17 两个 X 正端口 Bernoulli 分布为 P_A=0.5 与 P_B=0.4。D_KL(Bern(0.4)||Bern(0.5))=0.020135513550688863 nat/次，若把 A 当成完全指定零假设，在 B 下 1000 次观测的期望 log-LR 为 20.13551355。形式上 5/KL≈248.32 次仅是固定模型的期望 log-LR 代理值，**不是特定显著性与检验功效的样本数**。上述差异只发生在未证实物理合法性的玩具机制中。

**参阅：** Simon, Bužek & Gisin (2001), https://doi.org/10.1103/PhysRevLett.87.170405；Hughston–Jozsa–Wootters ensemble theorem 的远端制备讨论 https://arxiv.org/abs/quant-ph/0310001。
