# v0.91：光子吸收、原子激发与再发射的操作性身份审查

**科学定位：** Jaynes–Cummings 型量子光学有限维模型；不是光子永久身份的证明，也不是完整相对论 QED 的新预言。详细原始运行报告和源码见本轮本地完整 ZIP。

## 1. 标准 Fock 态

取原子基态 |g>、激发态 |e>，两个光学模式 a、b。单激发子空间的正交基：

\[
|a\rangle=|g,1_a,0_b\rangle,\quad
|e\rangle=|e,0_a,0_b\rangle,\quad
|b\rangle=|g,0_a,1_b\rangle.
\]

在共振、旋波近似下，依次控制两种模式与原子的相互作用：

\[
H_a/\hbar=g_a(a\sigma_++a^\dagger\sigma_-),\qquad
H_b/\hbar=g_b(b\sigma_++b^\dagger\sigma_-).
\]

打开 a–原子耦合一个面积为 \(g_at_a=\pi/2\) 的脉冲，然后打开 b–原子耦合一个面积为 \(g_bt_b=\pi/2\) 的脉冲：

\[
|a\rangle\xrightarrow{U_a}-i|e\rangle
\xrightarrow{U_b}-|b\rangle.
\]

两段间隔可以是有原子激发、但没有光场单光子占据的存储阶段；末态模式 a 的单光子数为0，模式 b 的单光子数为1。

| 阶段 | 光场光子数期望 | 原子激发数 | 总激发数 |
|---|---:|---:|---:|
| 输入 | 1 | 0 | 1 |
| 原子完全吸收后 | 0 | 1 | 1 |
| 输出模式 b 再发射后 | 1 | 0 | 1 |

这是**闭合、共振和可控模式耦合**的相干交换，而不是一般自由空间自发辐射的完整动力学描述。

## 2. 为什么守恒的不是光子数？

\[
N_{\text{ph}}=a^\dagger a+b^\dagger b,\qquad
N_{\text{ex}}=N_{\text{ph}}+\sigma_+\sigma_-.
\]

标准旋波近似下有 \([H_a,N_{\text{ex}}]=[H_b,N_{\text{ex}}]=0\)，但 \([H_{a,b},N_{\text{ph}}]\ne0\)。这表明可在光场模式与物质激发之间转移激发。三态单激发子空间中的 \(N_{\text{ex}}\) 本身为恒等矩阵，因此单在子空间中计算对易子是平凡的；本轮另在“原子 2 态 × a 模式 2 态 × b 模式 2 态”构成的**8维截断 Fock 空间**独立核对这组守恒关系。

这些守恒定律取决于 RWA 与所选系统；并不是说在全量 QED 中、任意物理过程下都有这样的“原子激发+光子数”守恒量。

## 3. 再发射的量子信道

从原子 |e> 与环境光模真空 |0> 出发，交换角度 θ 的演化满足：

\[
|e,0\rangle\to \cos\theta|e,0\rangle-i\sin\theta|g,1\rangle.
\]

对环境光模偏迹，原子通道由振幅阻尼 Kraus 算子描述：

\[
K_0=|g\rangle\langle g|+\cos\theta|e\rangle\langle e|,\qquad
K_1=-i\sin\theta|g\rangle\langle e|.
\]

\(K_0^\dagger K_0+K_1^\dagger K_1=I\)。标准 Fock 场模描述涉及湮灭入射模式的光量子与产生输出模式的光量子，而不要求存在能够贯穿此过程的可观测历史个体编号。

## 4. 相干信息的连续性 ≠ 个体光子的永久身份

增加一个不受耦合的参考光模 c，若初态 \(|\psi_0\rangle=\alpha|a\rangle+\beta|c\rangle\)，则上述受控操作把它变为 \(|\psi_f\rangle=-\alpha|b\rangle+\beta|c\rangle\)。这种相对相位和振幅传递展示的是**量子态的相干转移**，不是某一颗光子“原始身份”在没有场中光子的存储期仍然存在的证明。

若另加一个不影响系统动力学、也不能被仪器访问的隐藏身份辅助空间 I，在 \(U_S\otimes I_I\) 和 \(M_S\otimes I_I\) 形式的操作下，不同辅助标签给出的所有光学系统输出概率相同。该条件性操作性等价不禁止其他可能的真实耦合，但这些耦合须具有清楚的独立物理预测。

## 5. 计算与边界

本地 NumPy/SciPy 模型实际完成 **49/49 项 Python unittest**。检测项目包括两段脉冲幺正性、模式占据、总激发守恒与光子数不守恒、8维空间对易子、振幅阻尼 Kraus 完备性、参考模式相干传递，以及纯旁观身份标签在光学测量下的不可区分性。

**不应当推出：** 吸收过程已经实验证明原始光子被本体论意义上的“销毁”。“一个历史光子是否继续存在”若缺乏可操作的身份定义，就不是能够由上述占据测量唯一判定的命题。我们能严格陈述的是“某一场模的光子占据降为0，随后另一个场模的单光子占据升为1，激发在系统中保持”。

**仍有的物理缺口：** 本轮模型是封闭、旋波近似、单激发可控过程。更一般的自发辐射需要连续模式、多模发射波包及开放系统方法；本轮没有从规范不变的完整 QED 推导出新的永久身份相互作用。

## 6. 下一步 v0.92

用 Wigner–Weisskopf 多模自发辐射计算原子激发衰减、单光子波包的频谱和发射时间轮廓；把“模式重构与记忆”与“历史永久身份”的声称严格分离。

## 参考

- Harvard *Modern Atomic and Optical Physics II*, Chapter 9, Jaynes–Cummings 理论：https://lukin.physics.harvard.edu/sites/g/files/omnuum6416/files/lukin/files/physics_285b_lecture_notes.pdf
- St Andrews *Quantum Optics* notes：https://www.st-andrews.ac.uk/~jmjk/keeling/teaching/quantum-optics.pdf
- T. Brandes, *Source-field dynamics and counting*，创造/湮灭算符与两能级原子发射：https://www1.itp.tu-berlin.de/brandes/public_html/publications/lancaster_06.article.pdf
