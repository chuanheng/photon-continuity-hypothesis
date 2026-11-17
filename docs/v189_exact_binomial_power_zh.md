# v1.89：精确二项检验与复现实验

**日期：2026-11-17。研究状态：** Python/NumPy/SciPy 中实际执行的有限维量子通道合成计算，种子 20261117；不是实际光学实验、完整 QED 计算或对永久光子身份的支持。运行脚本与测试：[模型](../models/identity_channel_audit_v182_v191.py)、[测试](../tests/test_identity_channel_audit_v182_v191.py)。

**方案**：N=200，H0:p0=0.5、H1:p1=0.68，单侧 α≤0.05。遍历二项分布尾部，最小拒绝阈值为观察到基态≥113次，H0 实际尾概率 0.0384188161；H1 下精确功效 0.9997480618。NumPy RNG 种子 20261117 生成 140 个基态结果，样本 logLR=16.2706318070。**范围**：这是合成采样和精确分布计算，无器件系统误差、模型选择或复合假设 nuisance。

**主要理论参考：** Stinespring 扩张及其非唯一性：https://doi.org/10.1109/TIT.2008.917696；开放量子系统标准通道理论见 Nielsen & Chuang *Quantum Computation and Quantum Information*。
