# v1.80：标准非马尔可夫噪声完全吸收候选差异

**日期：2026-11-17。研究性质：** 本批次使用两能级相位退相干的合成量子信息模型（θ=0.6）；并非完整光子吸收/再发射实验，不是永久光子身份的证据。所有概率为模型计算，不是实测。完整运行见 [Python 复现代码](../models/identity_process_v172_v181.py) 与 [测试](../tests/test_identity_process_v172_v181.py)。

如果标准模型允许“每次实验从±两个失谐值中抽一次，并在实验期间保持固定”的准静态经典噪声，那么 v1.76 两时间统计与 v1.77 回波结果均与候选隐藏寄存器完全一致。对于该标准对照，最小 KL=0；不属于新物理效应。需区分“对重置环境检验的正 KL”和“对具有记忆的标准模型检验的零 KL”。

**参考：** Pollock et al. (2018), *Non-Markovian quantum processes: Complete framework and efficient characterization*, https://doi.org/10.1103/PhysRevA.97.012127 。
