# v1.85：振幅阻尼的守恒酉扩张

**日期：2026-11-17。研究状态：** Python/NumPy/SciPy 中实际执行的有限维量子通道合成计算，种子 20261117；不是实际光学实验、完整 QED 计算或对永久光子身份的支持。运行脚本与测试：[模型](../models/identity_channel_audit_v182_v191.py)、[测试](../tests/test_identity_channel_audit_v182_v191.py)。

**模型**：系统与环境都是二能级，环境初始 |0>；全局 4×4 酉矩阵仅在 |1,0>、|0,1> 两态间旋转，cosϑ=sqrt(1−γ)、sinϑ=sqrtγ。联合激发数 N=n_S+n_E 在该交换演化下守恒。**数值**：酉性误差约 2.66×10^-17；与标准 Kraus 通道四个矩阵基的输出最大差 0；[U,N] 最大矩阵元误差 0。**注意**：激发数守恒不等于全部真实电磁过程的光子数守恒；这是有限二能级系统。

**主要理论参考：** Stinespring 扩张及其非唯一性：https://doi.org/10.1109/TIT.2008.917696；开放量子系统标准通道理论见 Nielsen & Chuang *Quantum Computation and Quantum Information*。
