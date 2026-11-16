# v1.72：单步量子通道的完全正性与迹保持

**日期：2026-11-17。研究性质：** 本批次使用两能级相位退相干的合成量子信息模型（θ=0.6）；并非完整光子吸收/再发射实验，不是永久光子身份的证据。所有概率为模型计算，不是实测。完整运行见 [Python 复现代码](../models/identity_process_v172_v181.py) 与 [测试](../tests/test_identity_process_v172_v181.py)。

定义两个等权相位酉 U±=exp(∓iθZ/2)，θ=0.6，K±=U±/√2。检查 Σ K†K=I，最大误差 1.1102230246251565e−16。该随机酉通道是 CPTP。**局限：** CPTP 条件只说明映射数学合法，不说明其物理来源为永久身份。

**参考：** Pollock et al. (2018), *Non-Markovian quantum processes: Complete framework and efficient characterization*, https://doi.org/10.1103/PhysRevA.97.012127 。
