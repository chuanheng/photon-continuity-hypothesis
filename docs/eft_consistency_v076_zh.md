# v0.76：身份载体场的规范一致性与 Noether 荷

## 结论
存在可以同时满足局域 Lorentz 对称性、电磁规范不变性以及额外全局 U(1) 对称性的**扩展场论**；但其中守恒的荷属于新场，不等于“原始光子的永久身份”。本报告不是 QED 的替代理论，也不声称证明光子在吸收后个体身份延续。

## 1. 一个候选有效场论
采用四维自然单位与度规 (+---)。引入电磁中性复标量 S：

\[
\mathcal L=-\frac14 F_{\mu\nu}F^{\mu\nu}
+(\partial_\mu S)^*(\partial^\mu S)
-m_S^2|S|^2-\lambda|S|^4
+\frac{c_6}{\Lambda^2}|S|^2 F_{\mu\nu}F^{\mu\nu}.
\]

该 Lagrangian 在电磁规范变换 \(A_\mu\to A_\mu+\partial_\mu\alpha\) 下不变，因为 F 不变。在 \(S\to e^{i\beta}S\)（常数 β）下也不变。相应的守恒 Noether 流可取

\[
j^\mu_I=i(S^*\partial^\mu S-S\partial^\mu S^*),
\qquad \partial_\mu j^\mu_I=0
\]

（在运动方程成立时；不同变换符号约定可以使 j 整体反号）。对 \(S=Ae^{-i\omega t}\)，此约定 \(j^0_I=2\omega|A|^2\)。

四维下 [S]=1、[F]=2、[|S|²F²]=6，因此该相互作用是用 \(\Lambda^{-2}\) 抑制的维六 EFT 算符。线性 \(SF^2\) 虽维数为五，却违反上述 S 的全局 U(1) 对称性。物理结论仅是存在一个额外守恒场：这不是光子的历史身份。

## 2. 经典电磁规范与 Lorentz 检查

用 \(F_{\mu\nu}=k_\mu\epsilon_\nu-k_\nu\epsilon_\mu\) 作矩阵测试。改变极化 \(\epsilon\to\epsilon+\xi k\) 不改变 F。对 z 方向 Lorentz boost，收缩 \(F_{\mu\nu}F^{\mu\nu}\) 不变。本次实数样例在变换前后为 -0.910400（双精度误差量级）。

这是经典张量代数验证，不是量子 QED 完整 Ward–Takahashi 恒等式或环图幺正性证明。完整 QED 检验还需场量子化、规范固定、loop renormalization、物理态及 S 矩阵。

## 3. 独立的有限模式量子 toy model

设截断 photon 模式 a 与额外荷载体 b；选择

\[
H=\omega N_a+mN_b+g(a+a^\dagger)N_b,\quad Q_I=N_b.
\]

严格有 \([H,Q_I]=0\)，而 \(g\ne0\) 时通常 \([H,N_a]\ne0\)。示例参数 \(d_a=4,d_b=3,\omega=1,m=1.3,g=0.2\) 给出

\[
\Vert[H,Q_I]\Vert_F=0,\qquad
\Vert[H,N_a]\Vert_F=1.5491933384829673.
\]

它只说明额外载体荷守恒可以与 photon mode number 的非守恒并存。**线性 \(a+a^\dagger\) 相互作用本身不是已实现电磁规范不变性的 QED 相互作用；该 toy model 与上一节 EFT 是两项分开的数学检验。** 另外有限模式截断不满足无限维精确正则对易关系。

## 4. 吸收与永久身份的剩余缺口

如果 Q_I 守恒、photon 被吸收，它最多意味着额外载体的荷延续，而非“刚才那一个 photon 仍在”。必须具体写出含 photonic / carrier / absorber 模式的散射振幅，证明哪个可测可守恒量能实现一一对应的历史追踪，并排除普通环境记忆、偏振、谱模式或 ancilla 扩张的等价解释。

即使出现可测光学效应，普通新粒子 EFT \(|S|^2F^2\) 也可解释该效应，无法单凭它证明原始光子身份存在。

## 5. 结果与复现

本地在 Python+numpy 下运行 **27 项 unittest：全部通过**。计算结果：
- carrier_charge_commutator=0
- photon_number_commutator=1.5491933384829673
- f2=-0.9104000000000001
- f2_boosted=-0.9103999999999979
- carrier_current_density_at_A1_w2=4
- operator_dimension=6

见 models/eft_identity_v076.py、tests/test_eft_identity_v076.py、results/eft_identity_v076.json。若无 CI，GitHub 文件提交成功不代表 GitHub 服务器已独立运行测试。

## 6. v0.77 方向

用同一套约束构造 photon–matter–carrier 吸收与再发射过程；从完整有效 Lagrangian 推出可检验振幅，与普通 QED+环境记忆的实验预测逐项比较。如果观测完全等价，则将“永久身份”定位为解释性标签而非新理论。

## 参考
- Gelis, *Problems in Quantum Field Theory*, Cambridge excerpt (Ward–Takahashi): https://assets.cambridge.org/97811088/38801/excerpt/9781108838801_excerpt.pdf
- UT Austin, *Ward–Takahashi Identities*: https://web2.ph.utexas.edu/~vadim/Classes/2025f/WTI.pdf
- UMD, *Quantum Electrodynamics*: https://www.physics.umd.edu/grt/taj/624b/WeigandQFT.pdf
