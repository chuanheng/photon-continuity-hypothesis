# v3.19：二项检验的数值正确也不代表归因正确

**日期：2026-11-20。反方审稿阶段：v3.12–v3.21。** 全部是标准量子信息有限维数学、合成统计和文献比对。**不包含真实光子实验、完整 QED，也不是永久光子身份发现。** 本地独立模型已运行10/10项测试。复现：[GitHub模型](../models/identity_referee_v312_v321.py)、[GitHub回归测试](../tests/test_identity_referee_v312_v321.py)。

候选p1=.2408，固定参考p0=.095，n=200。选择单侧精确二项检验P_{p0}(K≥k)≤.05，得到最小拒绝阈值k=27；实际检验大小0.040273448344332406，候选下功效0.9999292017586787，简单假设KL=.09059719558758264。**审稿判定**：这只能否定该固定参考，无法否定允许内部模式重叠q_eff=.5184的完整标准族；后者可达到同一概率、profile KL=0。因此论文应把统计显著性和“非标准物理可辨识性”分别陈述。

**核查文献：** [Gate Set Tomography (Nielsen et al., 2021)](https://quantum-journal.org/papers/q-2021-10-05-557/)；[HOM interference for mixed states](https://doi.org/10.1139/cjp-2023-0312)；[Experimental GST gauge freedom (2017)](https://www.nature.com/articles/ncomms14485)；[Realistic HOM source limitations (2026)](https://www.mdpi.com/2304-6732/13/9/846)。
