# v3.20：相似变换保持概率，不保证物理表示合法

**日期：2026-11-20。反方审稿阶段：v3.12–v3.21。** 全部是标准量子信息有限维数学、合成统计和文献比对。**不包含真实光子实验、完整 QED，也不是永久光子身份发现。** 本地独立模型已运行10/10项测试。复现：[GitHub模型](../models/identity_referee_v312_v321.py)、[GitHub回归测试](../tests/test_identity_referee_v312_v321.py)。

抽象序列概率P_k=eᵀG^kρ，给可逆B，取ρ'=Bρ、e'ᵀ=eᵀB⁻¹、G'=BGB⁻¹，则P'_k=P_k。数值使用2×2矩阵、k=0..11，最大差1.1102230246e−16。这是线性状态空间的表示同构，不能据此把任意变换后的矩阵都视为标准密度矩阵/量子CPTP通道；GST中物理约束的处理有细节。**审稿要求**：不要用这种数学规范自由度直接证明永久光子身份具有某种实体同一性或额外物理。

**核查文献：** [Gate Set Tomography (Nielsen et al., 2021)](https://quantum-journal.org/papers/q-2021-10-05-557/)；[HOM interference for mixed states](https://doi.org/10.1139/cjp-2023-0312)；[Experimental GST gauge freedom (2017)](https://www.nature.com/articles/ncomms14485)；[Realistic HOM source limitations (2026)](https://www.mdpi.com/2304-6732/13/9/846)。
