# v1.75：单步隐藏量子寄存器与经典噪声等价

**日期：2026-11-17。研究性质：** 本批次使用两能级相位退相干的合成量子信息模型（θ=0.6）；并非完整光子吸收/再发射实验，不是永久光子身份的证据。所有概率为模型计算，不是实测。完整运行见 [Python 复现代码](../models/identity_process_v172_v181.py) 与 [测试](../tests/test_identity_process_v172_v181.py)。

把固定隐藏二能级环境的 Z 本征态等权分布，经过受控相位耦合后对环境求迹，恰与等权经典随机 U± 的随机酉通道一致。|+> 输入的一步 X 正端口概率为 (1+cos0.6)/2=0.9126678074548387。相同单步 POVM 输出的 KL 为 0。**结论：** 无法由一次测量区分量子寄存器与经典环境变量。

**参考：** Pollock et al. (2018), *Non-Markovian quantum processes: Complete framework and efficient characterization*, https://doi.org/10.1103/PhysRevA.97.012127 。
