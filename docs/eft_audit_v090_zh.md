# v0.90：规范不变 EFT 候选与光子永久身份的独立可证伪性

**研究性质：** 数学、有效场论与数值一致性审查；不是实验发现或关于原始光子永久身份的证明。单位 \(\hbar=c=1\)，Minkowski 度规 \((+---)\)。

## 1. 被审查的场论

延续 v0.76，引入电磁中性的复标量 \(S\)：

\[
\mathcal L=-\tfrac14F_{\mu\nu}F^{\mu\nu}
+\partial_\mu S^*\partial^\mu S-m_S^2|S|^2-\lambda|S|^4
+\frac{c_6}{\Lambda^2}|S|^2F_{\mu\nu}F^{\mu\nu}.
\]

由于 \(S\) 电磁中性，普通偏导足够；电磁局域 \(U(1)\) 作用于 \(A_\mu\)，保持 \(F_{\mu\nu}\) 不变；\(|S|^2\) 和 \(F^2\) 均为 Lorentz 标量。额外整体相位 \(S\to e^{i\theta}S\) 对应全局 \(U(1)_S\)，Noether 守恒荷属于**标量场**，并不是某颗历史光子跨吸收/再发射时的个体身份。

场的质量维度：\([S]=1,[F]=2\)，所以 \([|S|^2F^2]=6\)，其 Wilson 系数为 \(c_6/\Lambda^2\)。这属于常见的中性标量-光子 EFT 耦合形式；纯光子 Euler–Heisenberg 的首个 \(F^4\) 算符为维度八，二者需要区分。[1][2]

## 2. Ward 恒等式及散射振幅

两光子接触顶点的张量可写成（略去 S 矩阵相位与整体符号约定）

\[
V^{\mu\nu}(k_1,k_2)=(k_1\cdot k_2)\eta^{\mu\nu}-k_2^\mu k_1^\nu,
\quad
\mathcal M\propto 4\frac{c_6}{\Lambda^2}\epsilon_{1\mu}V^{\mu\nu}\epsilon_{2\nu}.
\]

通过逐项缩并或 SymPy 符号代数可得

\[
k_{1\mu}V^{\mu\nu}=0,\qquad V^{\mu\nu}k_{2\nu}=0.
\]

因此两个外光子的极化分别可作规范平移而不改变接触振幅。此必要条件与 QED 的 Ward 结构一致，[3] 但不证明全部量子化、重整化、因果性及 UV 完成已成立。

进一步在四维 Minkowski 空间：

\[
V^{\mu\nu}V_{\mu\nu}=2(k_1\cdot k_2)^2+k_1^2k_2^2.
\]

对两个实光子 \(k_i^2=0\)，能量均为 E、夹角 \(\theta\)，有 \(k_1\cdot k_2=E^2(1-\cos\theta)\)，物理偏振求和给出

\[
\sum_{\lambda_1,\lambda_2}|\mathcal M|^2
=\frac{32c_6^2}{\Lambda^4}E^4(1-\cos\theta)^2.
\]

这是所选接触振幅的平方，不是包含初态平均、通量、相空间或反应阈值的实验散射截面。若要把它用于 \(SS^*\leftrightarrow\gamma\gamma\)，还须独立施加整体四动量守恒。

## 3. 常数背景不构成光子质量或永久身份

若 \(|S|^2=s_0\) 为常数，则

\[
\mathcal L_\gamma=-\frac{Z}{4}F^2,\quad Z=1-4c_6s_0/\Lambda^2.
\]

\(Z>0\) 可用常数场重定义规范化自由电磁作用量，平面波仍有 \(k^2=0\)。单独看到 \(Z\neq1\) 不能声称光速改变、出现光子质量或多出历史光子身份。有带电物质或空间变化的 S 背景时必须另外计算真实观测量。

本轮示例 \(c_6=1,\Lambda=10,s_0=0.2\)：\(Z=0.992\)，自由光子色散不变。

## 4. 可辨识性

若只使用此一个算符，振幅通过 \(g=c_6/\Lambda^2\) 表达；\((c_6,\Lambda)=(1,10)\) 与 \((4,20)\) 给出同样的 \(g=0.01\)。仅从这种振幅无法独立识别这两个参数，相关 Fisher 参数块至多秩一。

即使实验观测到该作用量描述的真实效应（且排除标准物理），也只能提示**存在某种额外中性标量场耦合**，不能据此识别光子历史个体。常规新标量 EFT 与所谓“身份 EFT”在同样耦合下的预测一致。**因此本轮没有产生 PCH-A 独有可证伪的物理预测。**

## 5. 本轮复现与数值

在 Python 3 + NumPy + SymPy 的本地环境中，39/39 项 unittest 通过。包括：全符号 Ward 恒等式、非零夹角和外壳/离壳张量收缩、Polarization sum、规范平移、Lorentz boost、算符维度、Noether 整体相位不变性、健康动能号、Wilsonian 参数冗余。数值角度 \(\theta=0,\pi/6,\pi/3,\pi/2,2\pi/3,\pi\)，选能量 E=2、c6=1、Lambda=10，对应极化振幅平方之和分别为 0、约0.000919、0.0128、0.0512、0.1152、0.2048（任意自然单位下的顶点比较数值）。不应当解释为可直接测得的概率。

## 6. 研究定位及下一步

**结论：候选项可以满足被测规范与 Lorentz 必要条件；但它只是已有类型的有效场论交互作用，没有将“原始光子永久存在”转化为独立的新物理预测。**

v0.91 建议严格定义 QED 吸收—再发射中“同一个光子”的操作性含义，明确 Fock 态、场模、输入输出散射态和物质激发之间的差异，再寻找可以反驳普通模型的物理定量预测；否则不应继续用新场解释未经定义的光子历史身份。

## 文献

[1] *Matching and positivity beyond minimal coupling in effective theories of photons and gravitons*, 2025, https://doi.org/10.1140/epjc/s10052-025-13879-7

[2] *On-Shell Calculation of Low-Energy Photon–Photon Scattering*, 2025, https://www.mdpi.com/2218-1997/11/5/134

[3] Srednicki, *Quantum Field Theory* draft, Ward Identities in QED, https://web.physics.ucsb.edu/~mark/ms-qft-DRAFT.pdf
