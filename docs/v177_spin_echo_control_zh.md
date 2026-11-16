# v1.77：中间控制操作放大环境记忆差异

**日期：2026-11-17。研究性质：** 本批次使用两能级相位退相干的合成量子信息模型（θ=0.6）；并非完整光子吸收/再发射实验，不是永久光子身份的证据。所有概率为模型计算，不是实测。完整运行见 [Python 复现代码](../models/identity_process_v172_v181.py) 与 [测试](../tests/test_identity_process_v172_v181.py)。

在两次相位作用之间施加 X 操作。固定±环境中 U± X U±=X，初始 |+> 恢复至 |+>，正端口概率在浮点精度内为 1；独立重置环境对应 (1+cos²0.6)/2=0.8405894386191679。差异 0.15941056138083143。**结论：** 这是普通 spin echo 的噪声相关性效果，不是身份专有机制。

**参考：** Pollock et al. (2018), *Non-Markovian quantum processes: Complete framework and efficient characterization*, https://doi.org/10.1103/PhysRevA.97.012127 。
