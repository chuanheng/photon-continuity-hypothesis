# v1.79：固定种子的有限样本辨别

**日期：2026-11-17。研究性质：** 本批次使用两能级相位退相干的合成量子信息模型（θ=0.6）；并非完整光子吸收/再发射实验，不是永久光子身份的证据。所有概率为模型计算，不是实测。完整运行见 [Python 复现代码](../models/identity_process_v172_v181.py) 与 [测试](../tests/test_identity_process_v172_v181.py)。

在 v1.76 固定环境为真实生成模型时，用 NumPy RNG seed=20261117 生成 N=1000 的二项计数，X 正端口观测到 694 次；真实期望为 681.1789 次。简单假设固定环境对逐次重置环境的样本 logLR=66.1698149853132，期望 logLR=77.75274549369485。**局限：** 这是单次合成重复、不含复杂干扰参数；不是多次重复功效/覆盖率分析。

**参考：** Pollock et al. (2018), *Non-Markovian quantum processes: Complete framework and efficient characterization*, https://doi.org/10.1103/PhysRevA.97.012127 。
