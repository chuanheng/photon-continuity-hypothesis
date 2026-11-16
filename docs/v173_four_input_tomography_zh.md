# v1.73：四种输入态的过程一致性

**日期：2026-11-17。研究性质：** 本批次使用两能级相位退相干的合成量子信息模型（θ=0.6）；并非完整光子吸收/再发射实验，不是永久光子身份的证据。所有概率为模型计算，不是实测。完整运行见 [Python 复现代码](../models/identity_process_v172_v181.py) 与 [测试](../tests/test_identity_process_v172_v181.py)。

对 |0>、|+>、(|0>+i|1>)/√2、(|0>−|1>)/√2 计算输出密度矩阵。与标准相位翻转通道 E(ρ)=[(1+c)ρ+(1−c)ZρZ]/2 对比，c=cos(0.6)=0.8253356149，最大矩阵元差 1.11e−16。**局限：** 四态比较是此参数化通道的强一致性数值测试，不等于实际量子过程层析。

**参考：** Pollock et al. (2018), *Non-Markovian quantum processes: Complete framework and efficient characterization*, https://doi.org/10.1103/PhysRevA.97.012127 。
