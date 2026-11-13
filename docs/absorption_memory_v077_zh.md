# v0.77 光子吸收—储存—再发射：永久身份与普通量子记忆的操作性等价

## 核心结论

光学量子信息能够在吸收时映射到材料激发、随后通过相干读取返回光场。这一事实与“原来那一个光子仍然存在”不是同一个命题。有限维模型发现：一种假设的永久身份比特 H 与普通环境记忆比特 M，若动力学和允许测量由辅助空间酉同构联系，则实验上严格不可区分。

## 模型

在单激发空间内取三个基态 |a>、|b>、|e>，分别为信号光学模式、参考光学模式、材料激发；其中 |e> 不是光子。辅助比特 |h> 标记“身份”或“环境记忆”。输入

\[
|\psi_{\rm in}\rangle=(|a\rangle+|b\rangle)/\sqrt 2.
\]

相干吸收幺正变换为

\[
U_{ae}(\theta)=\begin{pmatrix}
\cos\theta&0&-i\sin\theta\\0&1&0\\-i\sin\theta&0&\cos\theta
\end{pmatrix}.
\]

储存期间，施加由辅助比特控制的相位

\[
U_{\mathrm{hold}}=I_6+(e^{i\phi}-1)|e\rangle\langle e|\otimes|1\rangle\langle1|.
\]

读取由吸收变换的逆操作实现：
\[
U_{\mathrm{tot}}=(U_{ae}^{\dagger}\otimes I_2)U_{\mathrm{hold}}(U_{ae}\otimes I_2).
\]

对于 \(\theta=\pi/2\)，信号模式 a 的激发转入 e，而旁路 b 不变；读取之后光学态为
\[
|\psi_h\rangle=(e^{ih\phi}|a\rangle+|b\rangle)/\sqrt2.
\]

注意：吸收时材料激发人口为 1/2，光路 a 的人口为 0，光路 b 的人口仍为 1/2——不能声称整个输入光学激发都已经消失。

## 实验概率

干涉输出 |+>=(|a>+|b>)/√2 和 |->=(|a>-|b>)/√2 满足
\[
P_+(h)=(1+\cos(h\phi))/2,\qquad P_-(h)=(1-\cos(h\phi))/2,
\]
且两种候选光学态的迹距离为
\[
D(\rho_0,\rho_1)=|\sin(\phi/2)|.
\]

\(\phi=\pi\) 时，h=0 的 P+=1，h=1 的 P+=0；但两种情况下 a、b 两个单独模式的强度都为 1/2。

这证明可耦合的隐藏比特的**状态**可辨识，但不能证明隐藏比特的**解释**为永久光子个体身份。

## 酉重标记的严格等价

令 X 交换辅助比特两个基态，J=I_3⊗X，并定义普通环境记忆模型
\[
U_M=J U_H J^\dagger,\quad \rho_M=J\rho_H J^\dagger.
\]
于是两个模型的输出满足 \(\rho'_M=J\rho'_H J^\dagger\)。对系统可观测量 E⊗I 有
\[
\operatorname{Tr}[(E\otimes I)\rho'_M]=\operatorname{Tr}[(E\otimes I)\rho'_H].
\]

如果把环境测量也用 J 一致变换，所有联合测量预测同样相等。这是一个明确的**操作性等价反例**，不是关于所有可能永久身份理论的一般 no-go 证明。

## 实际数值结果

| 指标 | 结果 |
|---|---:|
| φ=π，h=0：P+ | 1 |
| φ=π，h=1：P+ | 0 |
| φ=π：光学输出迹距离 | 1 |
| φ=π/2：光学输出迹距离 | 0.7071067811865474 |
| 吸收后材料激发人口 | 0.5 |
| 吸收后信号光路 a 人口 | 约 0 |
| 身份模型与同构记忆模型的系统态差范数 | 0 |

本地 Python **31 项 unittest 全部通过**；本次 GitHub 代码和测试在下列独立版本文件中给出。GitHub 提交本身不代表 GitHub CI 已执行。

## 局限

本模型是三维单激发子空间与一个二能级辅助空间，不是完整 QED，不包含非马尔可夫噪声、损失、材料多能级细节、自由空间辐射及 Lorentz 协变性论证。完美可逆读取是理想化条件。即便观测到此类相位，也可以由普通的材料相干记忆解释；不是光子身份跨吸收存续的独立证据。

**下一轮 v0.78：** 引入振幅损耗、环境退相干及实验计数统计，计算干涉可见度/信息分辨阈值，审计身份模型能否提供普通开放量子系统模型无法拟合的额外预言。

## 参考

1. Shore & Knight, *The Jaynes–Cummings Model* (1993), https://doi.org/10.1080/09500349314551321
2. Heshami et al., *Quantum memories: emerging applications and recent advances* (2016), https://pmc.ncbi.nlm.nih.gov/articles/PMC5020357/
3. *Optical Quantum Memory and its Applications in Quantum Communication Systems* (2020), https://doi.org/10.6028/jres.125.002

## 本地完整版

本轮研究完整源码、完整测试日志、实验脚本与报告见会话附件 photon_v077_complete.zip。