# v1.55：局域算符对易与非局域耦合

**2026-11-16 · v1.52–v1.61 批次。** 使用有限维矩阵、格点相位与理想概率进行计算；不是量子电动力学的新理论、完整洛伦兹协变证明或真实实验。代码：[模型](../models/identity_qft_gates_v152_v161.py)、[测试](../tests/test_identity_qft_gates_v152_v161.py)。

在两个二能级系统中，[Z⊗I,I⊗X]=0；引入 H_int=Z⊗X 后，[H_int,I⊗Z] 的 Frobenius 范数为 4。**结论**：分离张量因子的算符天然对易，但跨子系统耦合可以改变局域动力学；该系统没有空间距离、光锥或场算符，不能以此对易性证明微因果性或判定超光速。真实 QFT 要检验类空间隔的物理局域可观测量。参考：https://www.thphys.uni-heidelberg.de/courses/weigand/QFT1-12-13.pdf
