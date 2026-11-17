# v2.21：无信号约束与身份独有预测审查

**日期：2026-11-17。科学边界：** 本报告属于有限维单量子比特非线性映射的数学反例审查。它**不是光子场论机制、真实实验或永久光子身份的预测/证据**。统一代码：[模型](../models/identity_nonlinear_v212_v221.py)；[十项测试](../tests/test_identity_nonlinear_v212_v221.py)。本地原始版本使用 Python 标准库、固定随机种子，10 项单元测试全部通过。

本批次展示一个**数学上可区分**的非线性候选，但它既不是完整合法量子通道，也未证明与无超光速信号兼容。相关文献 Simon、Bužek、Gisin, *No-Signaling Condition and Quantum Dynamics*, PRL 87,170405 (2001)，讨论给定状态与 Born 规则等假设下无信号与线性完全正映射的关系；Hughston–Jozsa–Wootters 远端制备定理显示相同密度矩阵的不同系综分解在纠缠情境中有操作联系。由于本候选没有给出纠缠系统上的自洽演化规则，不能声称已严格完成超光速信号协议，**只能标记为严重待排查的风险**。它与光子永久身份没有数学必然联系，也没有真实实验支持；后续必须先修复理论一致性，不能把非线性本身当作新物理验证。

**参阅：** Simon, Bužek & Gisin (2001), https://doi.org/10.1103/PhysRevLett.87.170405；Hughston–Jozsa–Wootters ensemble theorem 的远端制备讨论 https://arxiv.org/abs/quant-ph/0310001。
