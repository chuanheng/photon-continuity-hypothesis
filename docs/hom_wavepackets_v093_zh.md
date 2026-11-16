# v0.93：Wigner–Weisskopf 单光子波包与 HOM 干涉、相关环境扰动

**科学定位**：标准量子光学数学推导和有限数值研究，不是独立的永久历史光子身份预测。本报告 GitHub 版本为本地完整 ZIP 中详细报告的精简归档。

## 1. 解析模式重叠

单光子的因果指数波包为

\[
\xi_i(t)=\sqrt{\Gamma_i}\Theta(t-t_i)
\exp[-(\Gamma_i/2+i\omega_i)(t-t_i)].
\]

令 \(\tau=t_2-t_1,\ \Delta=\omega_2-\omega_1\)。对模式直接求内积：

\[
M=|\langle\xi_1|\xi_2\rangle|^2
=\frac{4\Gamma_1\Gamma_2}{(\Gamma_1+\Gamma_2)^2+4\Delta^2}
\exp[-\Gamma_1\max(\tau,0)+\Gamma_2\min(\tau,0)].
\]

理想双单光子各进入一个输入端口，50:50 分束器后每次实验的无条件双端口符合概率为

\[
P_{\rm coincidence}=\frac{1-M}{2}.
\]

注意有些资料把完全可区分光子的基线归一化成1，使用 \(R=1-M\)，不应将它和这里的无条件计数概率混同。

## 2. 数值结果

| 情景 | M | P_coincidence |
|---|---:|---:|
| 完全相同模式 | 1 | 0 |
| 频率差一个线宽 | 0.5 | 0.25 |
| 线宽比 1:2 | 0.888889 | 0.055556 |
| 相对起始时间差一个寿命 | 0.367879 | 0.316060 |

独立数值积分对不同宽度、频移、正负时延的重叠进行了核对。

## 3. 两个发射源的普通相关噪声

每个发射源有高斯时间抖动 \(T_i\) 和高斯中心频率抖动 \(W_i\)。对应的源间相关系数为 \(r_t,r_\omega\)。相对噪声标准差：

\[
\sigma_{\Delta t}=\sqrt{2(1-r_t)}\sigma_t,\qquad
\sigma_{\Delta\omega}=\sqrt{2(1-r_\omega)}\sigma_\omega.
\]

若时间和频率**相对波动彼此独立**且两个发射波包具有同一 \(\Gamma\)，则

\[
\overline M=A_t A_\omega,\quad
A_t=\mathrm{erfcx}(\Gamma\sigma_{\Delta t}/\sqrt2),\quad
A_\omega=\sqrt{\frac\pi2}\frac{\Gamma}{\sigma_{\Delta\omega}}
\mathrm{erfcx}\left(\frac{\Gamma}{\sqrt2\sigma_{\Delta\omega}}\right).
\]

当 \(\sigma_{\Delta\omega}=0\) 时连续定义 \(A_\omega=1\)。取 \(\Gamma=1,\sigma_t=.2,\sigma_\omega=.3\)：

| 相关性 | 平均 M | P_coincidence |
|---|---:|---:|
| 完全共模，r=1 | 1 | 0 |
| 部分相关，r=.8 | 0.876943 | 0.061529 |
| 独立，r=0 | 0.708102 | 0.145949 |
| 独立、更大噪声(.4,.5) | 0.508371 | 0.245814 |

在独立情景下 Monte Carlo 100,000 次：\(M=0.70853537\)，标准误 \(0.00049423\)，符合解析值。可观测的是两个波包的**相对差异**，不是某个假想原始光子的个体识别号。

## 4. 重要的物理区分

若光子确实有可测偏振或其他真实内部模式 \(|\chi_i\rangle\)，HOM 重叠乘上 \(|\langle\chi_1|\chi_2\rangle|^2\)。正交的可区分内部态会消除 HOM 抑制。因此不能一概宣称所有隐藏标签都不会影响 HOM；**真正参与玻色交换振幅的内部量子态有物理影响**。

如果声称的永久身份只是未进入光子空间、完全不参与可访问动力学的旁观辅助标签，HOM 则不能单凭模式干涉区分它。即使观测到额外内部态，也还须证明为何它是跨吸收/再发射的同一个历史个体，而非普通模式自由度。

本轮使用的额外随机背景概率 \(P_{\mathrm obs}=(1-q)P_{\mathrm ideal}+q/2\) 只是现象学示例，不能取代真实探测器效率、暗计数、多光子分量与时间门宽的联合模型。

## 5. 结论

HOM 的符合数据可以测量模式不可区分度；波包线宽、中心频率、时延、环境噪声相关性及真实内部量子态足以改变干涉结果，**未出现只属于永久历史光子身份的实验预测**。

本地完整研究包进行了40项 Python 单元测试全部通过，生成两张 PNG、121 点延迟曲线、81 点相关性扫描以及100,000次随机验证。GitHub 版本为独立整理的代码，不声明与本地已执行文件逐字节相同，也不声称远程 CI 通过。

## 6. 参考文献

- NIST (2023), *Single-Photon Sources and Detectors Dictionary*, §2.5.3 https://nvlpubs.nist.gov/nistpubs/ir/2023/NIST.IR.8486.pdf
- Drago and Brańczyk (2024), *Hong–Ou–Mandel interference: a spectral–temporal analysis*, https://doi.org/10.1139/cjp-2023-0312
- *Hong–Ou–Mandel Interference with Imperfect Single Photon Sources*, PRL 126, 063602, https://doi.org/10.1103/PhysRevLett.126.063602

**v0.94** 建议转向公平混合态和真实探测联合模型，并审计模式纯度与探测背景的统计可辨识性。
