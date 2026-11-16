# 光子连续存在假说 v0.75：永久身份标签的一致性审计

> 状态：深度研究结论整理稿（2026-11-13）。本文依据已完成的 v0.75 深度研究报告重整关键结果，不是逐字原始报告。原研究在其执行环境中报告 21/21 项测试通过；本次 GitHub 同步没有重新执行那些原始测试，也未取得原始 Python 文件。

## 执行摘要

本轮结论是一个**有条件的 no-go**，而不是否定一切可能隐藏自由度的绝对定理。

1. **槽位身份 no-go**：在标准相同玻色子的对称 \(n\) 粒子 Hilbert 空间，无法将未对称张量积中第 \(i\) 个因子的序号升级为可区分的、逐粒子的物理身份算符。
2. **内部自由度反例**：可以把单粒子空间改成 \(\mathfrak h\otimes\mathcal K_I\)，再取对称 Fock 空间；内态不同不违反交换对称性。但这是增加模型结构，不是对现有光子的逐粒子身份的证明。
3. **不可接触的身份标签不可辨识**：如果所有允许的制备、通道、测量都不访问身份空间，系统统计不能决定其存在与否。
4. **可耦合的标签可测但仍不能证明永久个体性**：任何新可观测偏差，都必须排除已知偏振、谱宽、时间模式等内部/外部可区分性。
5. **标准 QED 光子数不普遍守恒**，不存在现成的逐光子历史身份守恒荷。所谓“吸收之后原光子仍在”，需要提出额外承载者和一致的局域动力学。

## 一、严格的槽位算符 no-go

设
\[
\mathcal H_B^{(n)}=\operatorname{Sym}^n\mathfrak h
\]
且 \(U_\pi\) 是置换群 \(S_n\) 的作用。对任意 \(|\psi\rangle\in\mathcal H_B^{(n)}\)，
\[
U_\pi|\psi\rangle=|\psi\rangle.
\]

假设逐槽位算符族 \(J_i\) 满足自然的交换协变条件
\[
J_{\pi(i)}=U_\pi J_i U_\pi^\dagger.
\]
因为在对称空间上 \(U_\pi=I\)，立即得到
\[
J_1=J_2=\cdots=J_n.
\]
因此不存在能够把张量槽位 1、2、……提升为独立可观测个体标签、同时保持上述协变条件的非平凡 \(J_i\)。

对于两玻色子，交换算符 \(S\) 和对称投影 \(P_+=(I+S)/2\) 满足
\[
P_+(A\otimes I)P_+=P_+(I\otimes A)P_+.
\]

**适用边界：** 此证明禁止的是张量槽位编号所声称的物理身份，而非一切内部态、模式标签、可守恒荷或本体论解释。

## 二、允许内部量子数，但必须承认新增结构

构造
\[
\mathcal F_s(\mathfrak h\otimes\mathcal K_I).
\]
即使 \(\mathcal K_I\) 携带正交态 \(|0\rangle_I,|1\rangle_I\)，整体仍可采用玻色对称化。

一个简单的带标签两模式 Hamiltonian 为
\[
H_{\rm BS}=J\sum_{\lambda=0,1}
(a^\dagger_{a\lambda}a_{b\lambda}+a^\dagger_{b\lambda}a_{a\lambda}),
\]
其标签占据数 \(N_\lambda=\sum_m a^\dagger_{m\lambda}a_{m\lambda}\) 满足
\[
[H_{\rm BS},N_\lambda]=0.
\]
这是严格守恒内部标签的一致**有限模式模型**，并非真实光子的历史身份保持定理。若要给每一个历史光子一个唯一标签，所需态空间与守恒结构远比这一双标签演示更强。

## 三、操作性可辨识：无法观测不等于规范冗余

若身份空间 \(I\) 的演化为恒等，测量效应为 \(M_o^{(S)}\otimes I_I\)，则
\[
p(o)=\operatorname{Tr}\{[M_o^{(S)}\otimes I_I](\mathcal E_S\otimes {\rm id}_I)(\rho_{SI})\}
=\operatorname{Tr}[M_o^{(S)}\mathcal E_S(\rho_S)]
\]
其中 \(\rho_S=\operatorname{Tr}_I\rho_{SI}\)。

因此，在所述操作集合下，一切系统量子过程层析也不能唯一恢复身份标签。若身份标签与探针耦合，例如 \(H_{PI}=gZ_P\otimes Z_I\)，可能在保持 \([H_{PI},Z_I]=0\) 的同时产生可辨别相位；**标签守恒并不意味着标签不可测量**。但只要未给出独立测量协议和误差模型，这仍属玩具示例。

**规范冗余须另行证明**：要把身份标签视为规范变量，必须明确规范群、约束、可观测量代数及同一规范轨道的物理等价关系。

## 四、QED 的主要一致性障碍

标准 QED 的相互作用项形式为
\[
H_{\rm int}\sim e\int d^3x\,\bar\psi\gamma^\mu\psi A_\mu.
\]
因电磁场算符含 \(a+a^\dagger\)，一般有
\[
[N_\gamma,H_{\rm int}]\ne0.
\]

这表示相互作用中光子产生与湮灭，而不是某个额外“个体性守恒荷”已被证明不可能。若 PCH-A 声称身份跨吸收与再发射持续存在，就必须指定光子数减少时身份存于何处、如何局域转移，且维持 Lorentz 协变、QED 规范结构及 Ward–Takahashi 恒等式。

## 五、数值和实验可检验性

HOM 两光子 coincidence 的理想模型为
\[
P_c=\frac{1-|\langle\alpha|\beta\rangle|^2}{2}.
\]
完全相同内态给出 \(P_c=0\)，正交内态给出 \(P_c=1/2\)。但降低的可见度也可来自普通偏振、时间及频谱模式失配，不能由此单独推断永久身份。

原 v0.75 深度研究报告声明其 Python 数值模型和单元测试已运行 **21/21 通过**。该报告汇总的主要检查包括：
- 槽位身份算符在对称子空间上的压缩差为 0（数值精度内）。
- 守恒标签模型 \(\|[H,Q_I]\|_2=0\)。
- 截断 QED-like 模型 \(\|[H_{\mathrm int},N]\|_2=2.8569700139\ne0\)；这是特定截断模型的参数相关数值，不是 QED 的普适常数。
- HOM 内态重叠对 coincidence 的影响。
- 可耦合身份探针在选择参数下可达到迹距离 1。

**复现状态：** 21 项测试是原深度研究环境的执行记录。本次不能获取其原始源码和日志，故没有在当前环境独立核验，不将测试文件标记为已推送。

## 六、对 PCH-A 的判定

| 命题 | 审计结论 |
| --- | --- |
| 张量槽位编号就是不可交换的永久个体身份 | **条件性 no-go**，与标准对称玻色空间结构冲突 |
| 添加可守恒内部标签 | **数学上可构造**，但不是永久历史身份的证明 |
| 永不与可观测量耦合的标签 | **操作性不可辨识** |
| 允许身份影响可观测过程 | **原则上可检验**，但必须提出非平凡动力学 |
| 标准 QED 已包含逐光子永久身份守恒量 | **无此现成结构** |
| 现有实验独立支持 PCH-A | **尚无** |

**总论断：** PCH-A 尚未被一个包打天下的 no-go 定理绝对排除，但当前仍不能称为已建立的替代 QED 物理理论；若持续只添加无可观测后果的标签，它更接近数学重标记和本体论解释。

## 七、v0.76 建议

1. 写出 Lorentz 协变、局域、规范一致的最小身份场 Lagrangian，严格清点自由度。
2. 由对称性而非人工约定推导 Noether 荷及其守恒流。
3. 为光子吸收—再发射给出身份信息的局域传递机制。
4. 检查 Ward–Takahashi 恒等式、物理横向极化、幺正性与微观因果性。
5. 提出不能被普通附加内态模型复制的 S 矩阵或多时关联函数预测。
6. 预先设定停止条件：若所有结果都可被不可访问 ancilla 或普通多组分场重参数化，则将永久身份降格为解释性标签。

## 参考文献

- Messiah, A. M. L. & Greenberg, O. W. (1964), *Symmetrization Postulate and Its Experimental Foundation*, Physical Review 136, B248. https://doi.org/10.1103/PhysRev.136.B248
- Girardeau, M. D. (1965), *Permutation Symmetry of Many-Particle Wave Functions*, Physical Review 139, B500. https://doi.org/10.1103/PhysRev.139.B500
- Wick, G. C., Wightman, A. S. & Wigner, E. P. (1952), *The Intrinsic Parity of Elementary Particles*. https://doi.org/10.1103/PhysRev.88.101
- Doplicher, S., Haag, R. & Roberts, J. E. (1971), *Local Observables and Particle Statistics I*. https://inspirehep.net/literature/67575
- Stinespring, W. F. (1955), *Positive Functions on C*-Algebras*. https://doi.org/10.1090/S0002-9939-1955-0069403-4
- Choi, M.-D. (1975), *Completely Positive Linear Maps on Complex Matrices*. https://doi.org/10.1016/0024-3795(75)90075-0
- Weinberg, S., *The Quantum Theory of Fields*. Cambridge University Press. https://www.cambridge.org/core/books/quantum-theory-of-fields/0E0C89894938BE38EE0BCCDB1BC857E5/listing

## 来源与可追溯性

本文件整理自 2026-11-13 已完成的 v0.75 深度研究报告。原报告的文件名为 \`/mnt/data/photon_v075/docs/consistency_audit_v075_zh.md\`，但该文件未挂载到本次会话的可用文件环境。本 GitHub 版本因此是研究**结论整理稿**，而非对不可访问原文件的逐字复制。