# v1.76：固定环境与逐次重置的两时间对照

**日期：2026-11-17。研究性质：** 本批次使用两能级相位退相干的合成量子信息模型（θ=0.6）；并非完整光子吸收/再发射实验，不是永久光子身份的证据。所有概率为模型计算，不是实测。完整运行见 [Python 复现代码](../models/identity_process_v172_v181.py) 与 [测试](../tests/test_identity_process_v172_v181.py)。

比较两次相同相位曝光之间未施加操作的测量。若每轮曝光由同一个固定±随机相位支配，X 正端口概率 (1+cos1.2)/2=0.6811788772383363；若两次曝光独立重新抽样，概率 (1+cos²0.6)/2=0.8405894386191679。差异 −0.15941056138083165，简单假设 Bernoulli KL(Pstatic||Preset)=0.07775274549369485 nat/次。**结论：** 单步通道相同但两时间统计不一定相同；这可区分环境记忆假设，不足以检验永久光子身份。

**参考：** Pollock et al. (2018), *Non-Markovian quantum processes: Complete framework and efficient characterization*, https://doi.org/10.1103/PhysRevA.97.012127 。
