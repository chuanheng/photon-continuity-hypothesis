# v1.88：固定假设的证据积累尺度

**日期：2026-11-17。研究状态：** Python/NumPy/SciPy 中实际执行的有限维量子通道合成计算，种子 20261117；不是实际光学实验、完整 QED 计算或对永久光子身份的支持。运行脚本与测试：[模型](../models/identity_channel_audit_v182_v191.py)、[测试](../tests/test_identity_channel_audit_v182_v191.py)。

**解析计算**：若两个假设 p0=0.5、p1=0.68 完全指定，N 次独立 Bernoulli 观测的候选分布下期望对数似然比 N D_KL。N=200 时为 13.2555445975 nat；令期望对数似然比等于 5，形式上的样本代理量 N≈75.4401。**注意**：N≈75.44 不是检验功效、显著性或置信水平的正式样本量，故下一轮使用精确二项检验。

**主要理论参考：** Stinespring 扩张及其非唯一性：https://doi.org/10.1109/TIT.2008.917696；开放量子系统标准通道理论见 Nielsen & Chuang *Quantum Computation and Quantum Information*。
