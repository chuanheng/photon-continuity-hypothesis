# v2.13：固定量子通道的仿射混合定律

**日期：2026-11-17。科学边界：** 本报告属于有限维单量子比特非线性映射的数学反例审查。它**不是光子场论机制、真实实验或永久光子身份的预测/证据**。统一代码：[模型](../models/identity_nonlinear_v212_v221.py)；[十项测试](../tests/test_identity_nonlinear_v212_v221.py)。本地原始版本使用 Python 标准库、固定随机种子，10 项单元测试全部通过。

**标准比较条件：** 对一个固定的、与输入制备细节无关的 CPTP 通道 E，当 ρ=Σ_i w_iρ_i 时，E(ρ)=Σ_i w_i E(ρ_i)。这源自线性性，适用于不同经典随机化程序产生的相同输入密度算符。标准量子测量的输出概率为 Tr[M E(ρ)]。**局限：** 如果设备实际上根据制备标签、控制脉冲或环境状态改变，那么各次实验不是同一个 E；在排除这种标准上下文变化前，不能把仿射性偏差解释为新量子力学。参考 Simon–Bužek–Gisin, PRL 87,170405 (2001)。

**参阅：** Simon, Bužek & Gisin (2001), https://doi.org/10.1103/PhysRevLett.87.170405；Hughston–Jozsa–Wootters ensemble theorem 的远端制备讨论 https://arxiv.org/abs/quant-ph/0310001。
