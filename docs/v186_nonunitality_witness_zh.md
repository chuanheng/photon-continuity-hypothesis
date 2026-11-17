# v1.86：最大混合态作为非幺正性见证

**日期：2026-11-17。研究状态：** Python/NumPy/SciPy 中实际执行的有限维量子通道合成计算，种子 20261117；不是实际光学实验、完整 QED 计算或对永久光子身份的支持。运行脚本与测试：[模型](../models/identity_channel_audit_v182_v191.py)、[测试](../tests/test_identity_channel_audit_v182_v191.py)。

**研究问题**：能否区分振幅阻尼与所有随机酉通道？**解析结果**：随机酉通道 E(I/2)=I/2；振幅阻尼使 I/2→diag((1+γ)/2,(1−γ)/2)=diag(0.68,0.32)。与原最大混合态的迹距离=γ/2=0.18。**结论**：这个输入加上 Z 基测量能排除任何纯随机酉对照；但排除随机酉噪声不等于排除标准开放量子系统。

**主要理论参考：** Stinespring 扩张及其非唯一性：https://doi.org/10.1109/TIT.2008.917696；开放量子系统标准通道理论见 Nielsen & Chuang *Quantum Computation and Quantum Information*。
