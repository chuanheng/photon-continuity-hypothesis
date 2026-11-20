# v3.13：封闭仪器假设下的不可辨识性再核查

**日期：2026-11-20。反方审稿阶段：v3.12–v3.21。** 全部是标准量子信息有限维数学、合成统计和文献比对。**不包含真实光子实验、完整 QED，也不是永久光子身份发现。** 本地独立模型已运行10/10项测试。复现：[GitHub模型](../models/identity_referee_v312_v321.py)、[GitHub回归测试](../tests/test_identity_referee_v312_v321.py)。

当任何可访问量子仪器均是固定S系统的CP映射，并且没有E→S的反馈，两个实验具有相同可见初态，则可按测量记录对条件态归纳证明其所有记录分布一致。数值先对两种无关标签准备计算可见边缘态，再在同一S通道作用下比较；200组随机复数密度矩阵测试最大输出迹距离2.4980356865e−16。数值误差来自浮点而非统计效应。**定理并不推出“只要初始S边缘态相同，未来一定不可区分”**；相关环境能使这句话失效，见v3.14。

**核查文献：** [Gate Set Tomography (Nielsen et al., 2021)](https://quantum-journal.org/papers/q-2021-10-05-557/)；[HOM interference for mixed states](https://doi.org/10.1139/cjp-2023-0312)；[Experimental GST gauge freedom (2017)](https://www.nature.com/articles/ncomms14485)；[Realistic HOM source limitations (2026)](https://www.mdpi.com/2304-6732/13/9/846)。
