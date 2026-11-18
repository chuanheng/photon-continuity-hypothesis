# v2.41：随机轨迹修复的成效与新物理门槛

**版本批次：v2.32–v2.41；日期：2026-11-18。** 标准有限维振幅阻尼/量子轨迹数学模拟，不是永久光子身份理论、真实光学实验或完整相对论 QED。使用 NumPy，固定种子 20261118。实际本地测试 10/10 通过。复现：[GitHub 模型](../models/identity_trajectories_v232_v241.py)、[GitHub 十项测试](../tests/test_identity_trajectories_v232_v241.py)。

条件轨迹的归一化可以非线性、随机，整体概率仍保持标准的线性量子通道，且在本次 Bell 纠缠态试验中满足无信号条件。这个理论修复明确克服了 v2.22–v2.31 逐远端纯态分支非线性模型的冲突，却把平均动力学重新带回标准开放量子系统/Lindblad-可展开范畴。**这不证明存在永久光子身份，也没有产生标准理论无法解释的独有实验预测。** 未推导出身份标签的独立场论耦合、完整 QED 或洛伦兹协变性。下一步应寻找（或证明无法建立）能同时通过基本一致性要求、且与标准 QED 所允许操作概率不同的候选动力学；若仍无，须把假说维持为不可辨识的本体解释。

**标准理论参照：** [Quantum trajectory framework for general time-local master equations, Nature Communications (2022)](https://doi.org/10.1038/s41467-022-31533-8)；[Quantum trajectories in monitored systems, PTEP (2026)](https://academic.oup.com/ptep/article/2026/5/052A01/8530537)。
