# v3.16：相同混合态在真正共享量子通道下保持一致

**日期：2026-11-20。反方审稿阶段：v3.12–v3.21。** 全部是标准量子信息有限维数学、合成统计和文献比对。**不包含真实光子实验、完整 QED，也不是永久光子身份发现。** 本地独立模型已运行10/10项测试。复现：[GitHub模型](../models/identity_referee_v312_v321.py)、[GitHub回归测试](../tests/test_identity_referee_v312_v321.py)。

将I/2分解为Z基系综|0>,|1>各1/2，或X基系综|+>,|->各1/2。对全部纯态应用同一个固定退相干通道E(ρ)=.8ρ+.2 ZρZ，再按权重求平均。两种输出迹距离1.1102230246e−16。这个结果是量子通道仿射性直接给出的，没有提供超出已知理论的永久身份预测，也没有否认v3.14的不同S–E相关性反馈情形。

**核查文献：** [Gate Set Tomography (Nielsen et al., 2021)](https://quantum-journal.org/papers/q-2021-10-05-557/)；[HOM interference for mixed states](https://doi.org/10.1139/cjp-2023-0312)；[Experimental GST gauge freedom (2017)](https://www.nature.com/articles/ncomms14485)；[Realistic HOM source limitations (2026)](https://www.mdpi.com/2304-6732/13/9/846)。
