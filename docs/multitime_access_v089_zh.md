# v0.89 多时刻操作性可辨识性与光子身份边界

**论文性质**：有限维量子比特过程张量的教学式、可复现数学实例；不是 QED 动力学、不是光子持续身份的实验发现，也不宣称本例为原创数学定理。

## 背景

不能把单步量子信道相同视为整个多时刻过程相同。Pollock et al.（2018）对量子过程的操作性 Markov 条件进行了系统讨论；Milz 和 Modi（2021）给出了过程张量及量子随机过程的综述。多时刻过程以允许插入的控制操作为自变量，必要时必须允许中间测量、重制及后选择。

## 两个模型

初态 \(\rho_0=|0\rangle\langle0|\)，\(X\) 是 Pauli 位翻转。模型 fixed 抽取一次均匀随机数 r，然后连续两步都施加 \(X^r\)；模型 fresh 每步独立抽取均匀随机数 r,s。

二者每个时间步的单步 CPTP 信道都是

\[
\mathcal E(\rho)=\frac12(\rho+X\rho X).
\]

但任意中间 CP 操作 \(\mathcal A\) 之后的未归一化终态不同：

\[
\mathcal T_{\rm fixed}[\mathcal A](\rho_0)=\frac12\sum_r X^r\mathcal A(X^r\rho_0X^r)X^r;
\]
\[
\mathcal T_{\rm fresh}[\mathcal A](\rho_0)=\frac14\sum_{r,s}X^s\mathcal A(X^r\rho_0X^r)X^s.
\]

对 \(\mathcal A=\mathrm{id}\)，fixed 输出 \(\rho_0\)，fresh 输出 \(I/2\)，迹距离 \(D=\frac12\)。因此，单步等价不能推出多时刻等价。

## 因果断开实验

中间测量并重新制备 \(|0\rangle\)，对应单结果 Kraus 算子 \(K_0=|0\rangle\langle0|\)、\(K_1=|0\rangle\langle1|\)。分支各发生概率 1/2。fixed 条件末态分别为 \(|0\rangle\langle0|\) 和 \(|1\rangle\langle1|\)，fresh 末态在两个分支均为 \(I/2\)。故测量结果传递了关于环境的记忆信息，即便实验者已经重置系统。这是已有量子过程理论意义下的环境记忆现象，不证明“同一个原始光子跨吸收继续存在”。

## 信息完备的有限测试器

令 \(|0\rangle,|1\rangle,|+\rangle,|+i\rangle\) 为单比特信息完备的四个态。中间16个单分支 CP 操作为 \(\mathcal A_{pe}(\rho)=K_{pe}\rho K_{pe}^{\dagger}\)，其中 \(K_{pe}=|p\rangle\langle e|\)；末态四个效果 \(E_f=|f\rangle\langle f|\)。

16 个 CP 分支的 Choi 投影算子张成四乘四 Hermitian 空间，Gram 秩为16；四个末态效果张成二乘二 Hermitian 空间，Gram 秩为4；相应总共64个概率测试器张成64维线性空间。这些效果必须分别在不同实验设置中测量，**四个投影不是同一个四结果 POVM**。

在固定初态、恰有一次中间干预、只有最终系统测量的有限维范围内，两个线性过程泛函只要在这组线性完备的测试器上同值，便对其线性张成中的任何控制和效果同值。该命题源自线性代数，不是所有时间长度或所有光子实验的一般定理。

## 真实数值

| 指标 | 结果 |
|---|---:|
| 单步输入零态输出 | I/2 |
| 两步 fixed 末态 \(P(0)\) | 1 |
| 两步 fresh 末态 \(P(0)\) | 0.5 |
| 末态迹距离 | 0.5 |
| 因果断开结果0的发生概率 | 0.5 |
| fixed 结果0后的末态 \(P(0)\) | 1 |
| fresh 结果0后的末态 \(P(0)\) | 0.5 |
| 中间 CP 分支张成秩 | 16 |
| 末态效果张成秩 | 4 |
| 测试器总数 | 64 |
| fixed 与 fresh 的最大概率差 | 0.25 |
| fixed 与 fresh 的概率差 RMS | 0.09882117688026185 |
| fixed 模型内部标签及条件动力学一致重标记后的最大概率差 | 0 |
| 本地单元测试 | 33/33 通过，0.028s |

注意：把 r 改名为 \(r'=1-r\)，并同时把相应条件算子改为 \(X^{1-r'}\)，所有概率保持相同。仅靠同一随机变量换名不能证明存在永恒光子历史个体。

## 局限与后续

模型包含经典隐藏随机比特、二能级系统、两个时间步和一处操作插入。它既没有光子 Fock 量子场与吸收的微观构造，也没有 Lorentz、玻色对称和 QED 规范不变性证明。未来必须推导公平普通环境记忆模型无法复制的场论预测，才有讨论新物理身份自由度的依据。

参考文献：

1. Pollock et al. (2018), *Operational Markov Condition for Quantum Processes*, PRL 120, 040405. https://doi.org/10.1103/PhysRevLett.120.040405
2. Pollock et al. (2018), supplemental material (causal break and complete controls). https://journals.aps.org/prl/supplemental/10.1103/PhysRevLett.120.040405/20171215_PRL_supplemental.pdf
3. Milz & Modi (2021), *Quantum Stochastic Processes and Quantum non-Markovian Phenomena*, PRX Quantum 2, 030201. https://doi.org/10.1103/PRXQuantum.2.030201
