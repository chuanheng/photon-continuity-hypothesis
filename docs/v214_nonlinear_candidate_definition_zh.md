# v2.14：一个可明确否证的态依赖退相干候选

**日期：2026-11-17。科学边界：** 本报告属于有限维单量子比特非线性映射的数学反例审查。它**不是光子场论机制、真实实验或永久光子身份的预测/证据**。统一代码：[模型](../models/identity_nonlinear_v212_v221.py)；[十项测试](../tests/test_identity_nonlinear_v212_v221.py)。本地原始版本使用 Python 标准库、固定随机种子，10 项单元测试全部通过。

用 Bloch 坐标 ρ=(I+xX+yY+zZ)/2，定义 N_λ:(x,y,z)→(cx,cy,z)，c=1−2λ x²，取 λ=0.4。它不同于固定通道：因子 c 依赖输入 x。对于 |+>（x=1）变换后 x'=0.2；对于 |0>（x=0,z=1）维持不变。**重要：** 这个数学候选只用来检验非线性规则的困难，未推导出光子身份新哈密顿量、规范一致场耦合或其物理来源；不能据“成功构造”称作已发现新机制。

**参阅：** Simon, Bužek & Gisin (2001), https://doi.org/10.1103/PhysRevLett.87.170405；Hughston–Jozsa–Wootters ensemble theorem 的远端制备讨论 https://arxiv.org/abs/quant-ph/0310001。
