# v3.15：不同制备可能意味着不同实际量子通道

**日期：2026-11-20。反方审稿阶段：v3.12–v3.21。** 全部是标准量子信息有限维数学、合成统计和文献比对。**不包含真实光子实验、完整 QED，也不是永久光子身份发现。** 本地独立模型已运行10/10项测试。复现：[GitHub模型](../models/identity_referee_v312_v321.py)、[GitHub回归测试](../tests/test_identity_referee_v312_v321.py)。

两个实验从相同|+>系统态出发。设置A施加恒等通道，设置B施加完全Z退相干通道E(ρ)=(ρ+ZρZ)/2。输出分别为|+><+|与I/2，迹距离0.5。两个都是合法CPTP通道，差异完全由设置相关控制/环境噪声造成。若把它们错误视作“同一个共享固定通道”，会把普通制备误差误判为新增身份效应。实验设计必须确认控制脉冲、温漂、光源与材料环境在不同设置下保持物理上有效的共享参数。

**核查文献：** [Gate Set Tomography (Nielsen et al., 2021)](https://quantum-journal.org/papers/q-2021-10-05-557/)；[HOM interference for mixed states](https://doi.org/10.1139/cjp-2023-0312)；[Experimental GST gauge freedom (2017)](https://www.nature.com/articles/ncomms14485)；[Realistic HOM source limitations (2026)](https://www.mdpi.com/2304-6732/13/9/846)。
