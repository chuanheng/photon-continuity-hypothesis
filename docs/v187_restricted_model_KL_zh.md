# v1.87：振幅阻尼与随机酉统计可区分

**日期：2026-11-17。研究状态：** Python/NumPy/SciPy 中实际执行的有限维量子通道合成计算，种子 20261117；不是实际光学实验、完整 QED 计算或对永久光子身份的支持。运行脚本与测试：[模型](../models/identity_channel_audit_v182_v191.py)、[测试](../tests/test_identity_channel_audit_v182_v191.py)。

**实验**：制备最大混合态，在 Z 基测量基态。随机酉零假设 p0=0.50，振幅阻尼 γ=0.36 预测 p1=0.68。两种简单假设的 Bernoulli KL 为 D(p1||p0)=0.06627772298751897 nat/轮，严格大于零。**限制**：这个非零 KL 只对应**受限的随机酉模型类**；允许常规能量耗散时，标准量子理论就能产生 p1。

**主要理论参考：** Stinespring 扩张及其非唯一性：https://doi.org/10.1109/TIT.2008.917696；开放量子系统标准通道理论见 Nielsen & Chuang *Quantum Computation and Quantum Information*。
