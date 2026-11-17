# v1.84：合法的振幅阻尼量子通道

**日期：2026-11-17。研究状态：** Python/NumPy/SciPy 中实际执行的有限维量子通道合成计算，种子 20261117；不是实际光学实验、完整 QED 计算或对永久光子身份的支持。运行脚本与测试：[模型](../models/identity_channel_audit_v182_v191.py)、[测试](../tests/test_identity_channel_audit_v182_v191.py)。

**模型**：K0=diag(1,sqrt(1−γ))，K1=[[0,sqrtγ],[0,0]]；γ=0.36。检验 Σ K†K=I，矩阵最大误差=0。Kraus 表示确保完全正性；迹保持由完备性保证。**边界**：这是普通自发衰减/能量交换的量子信息模型，而非永恒光子粒子身份的机制。

**主要理论参考：** Stinespring 扩张及其非唯一性：https://doi.org/10.1109/TIT.2008.917696；开放量子系统标准通道理论见 Nielsen & Chuang *Quantum Computation and Quantum Information*。
