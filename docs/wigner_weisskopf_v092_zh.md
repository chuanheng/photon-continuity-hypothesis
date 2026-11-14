# v0.92：Wigner–Weisskopf 多模自发辐射与光子波包

**科学定位：** 标准量子光学的解析近似与离散连续谱数值验证，并非新的 QED 理论，也没有证明光子历史个体的永久身份。

## 1. 单激发态与记忆核

初态为原子激发、场真空 \(|e,\mathrm{vac}\rangle\)，由旋波近似的单激发 Hamiltonian 演化：

\[
|\Psi(t)\rangle=c_e(t)|e,0\rangle+\sum_kc_k(t)|g,1_k\rangle,\quad
H/\hbar=\sum_k\Delta_k|g,1_k\rangle\langle g,1_k|+
\sum_k[g_k|e,0\rangle\langle g,1_k|+\mathrm{h.c.}].
\]

消去场模后，原子振幅服从非局域记忆核：
\[
\dot c_e(t)=-\int_0^t K(t-s)c_e(s)\,ds,\qquad
K(\tau)=\sum_k|g_k|^2e^{-i\Delta_k\tau}.
\]

对连续宽带平坦谱密度采取 Markov/弱耦合近似，\(\Gamma\) 为**激发态概率衰减率**：
\[
c_e(t)\simeq e^{-\Gamma t/2},\quad P_e=e^{-\Gamma t},
\quad P_{\rm emitted}=1-e^{-\Gamma t}.
\]

封闭原子—场联合演化幺正；原子激发转移到场模，并不是联合态消失。

## 2. 理想单通道发射波包

在无限宽带近似中，归一化单光子时间模式为
\[
\xi(t)=\sqrt\Gamma e^{-\Gamma t/2}e^{-i\omega_0t}\Theta(t),
\quad p(t)=|\xi(t)|^2=\Gamma e^{-\Gamma t}\Theta(t).
\]

\(\langle t\rangle=1/\Gamma\)。以**角频率偏移** \(\Delta=\omega-\omega_0\) 表示：
\[
S(\Delta)=\frac{\Gamma/(2\pi)}{\Delta^2+(\Gamma/2)^2},\quad
\int_{-\infty}^\infty S(\Delta)\,d\Delta=1,
\]
全高半宽 FWHM=\(\Gamma\)（角频率单位）。该单通道包络近似不含发射方向、偏振、真实正频率下界及探测器效率。

## 3. 实际算出的 401 模式 Hermitian 演化

数值模型不预设指数衰减，而对 **1个原子激发态+401个场模**的稀疏 Hermitian 星形矩阵求幺正传播。令 \(\Gamma=1\)，频率偏移 \(\Delta_k\in[-12,12]\)，模式间距 \(0.06\)，耦合 \(g_k=\sqrt{\Gamma\,0.06/(2\pi)}\)。

联合态最大归一化误差 \(2.5313\times10^{-14}\)。抽样：

| t | Markov 原子 P_e | 401 模式原子 P_e | 401 模式场中 P |
|---:|---:|---:|---:|
| 0 | 1 | 1 | 0 |
| 0.5 | 0.606531 | 0.627784 | 0.372216 |
| 1 | 0.367879 | 0.375935 | 0.624065 |
| 2 | 0.135335 | 0.134416 | 0.865584 |
| 4 | 0.018316 | 0.017194 | 0.982806 |
| 8 | 0.00033546 | 0.00029479 | 0.99970521 |

在 \(t\ge0.5\) 内 Markov 与有限模型原子人口差的最大值约0.02462。有限谱的早期行为为
\[
P_e(t)=1-\left(\sum_k|g_k|^2\right)t^2+O(t^3),\quad
\sum_k|g_k|^2\approx3.82927.
\]
因此封闭有限带宽系统起始斜率为零，而指数 Markov 近似起始斜率为\(-1\)。离散模式在足够长时间可产生回归；不可声称它始终不可逆。

## 4. 波包模式可辨识性不等于“个体身份”

两个同时起始的理想指数波包，线宽 \(\Gamma_1,\Gamma_2\) 且中心角频率差 \(\delta\omega\)，其重叠概率为
\[
|\langle\xi_1|\xi_2\rangle|^2=
\frac{4\Gamma_1\Gamma_2}{(\Gamma_1+\Gamma_2)^2+4(\delta\omega)^2}.
\]

同波包重叠=1；同线宽、频移=一倍线宽时重叠=0.5；线宽比1:2且无频移时重叠=8/9；同波包时移一倍寿命时重叠 \(e^{-1}\)。

这些量可用于量子干涉和波包区分。它们测量的是模式和频率、时间结构，并不为单个历史光子提供独立身份编号。

## 5. 对“原始光子永久存在”假说的限制

本轮标准模型使用原子—场单激发态已解释原子衰减、自由光场模式占据、发射谱与时间波包。若额外的“永久身份”标签不改变任何操作的概率，则它无独立实验证据。若声称身份发生物理耦合，就必须提出符合玻色对称、规范结构及相对论约束且普通 QED+环境模型不能复现的动力学预测。

**这不构成在本体论上证明原始光子被“摧毁”的结论。** 更准确的表述是：原子激发转移为分布于光场多模式的单光子激发；可测模式信息的连续传递与历史个体身份属于不同命题。

## 6. 计算与下一轮

本地精确源码运行 **46/46 项 Python unittest**；涉及时间概率归一化、Lorentzian 频谱积分、FWHM、指数波包重叠、短时二次概率、有限维 Hermitian 幺正性和宽带拟合。完整 Python 源码、数值曲线、PNG 与 SHA-256 在 \`photon_v092_complete.zip\`。GitHub 版本是按相同数学接口独立整理的代码；未经远程 CI 验证，不宣称和本地源码逐字节相同。

v0.93 建议研究单光子时间模式变化引起的 HOM 可见度与普通光谱环境记忆，继续检查历史标签能否提供不属于现有量子光场模式的预测。

## 文献

1. University of Arizona, *Wigner-Weisskopf Theory of Spontaneous Decay*, 2021: https://wp.optics.arizona.edu/opti544/wp-content/uploads/sites/54/2021/04/OPTI-544-Lecture-Posted-Friday-04302021.pdf
2. *Quantum Mechanics*, Ch. 60, Wigner–Weisskopf: https://mochizuki-tus.github.io/QM_Textbook_EN/ch60_photons_phonons.html
3. *Spontaneous Decay, Unitarity, and the Weisskopf–Wigner Approximation*, 2010: https://www.sciencedirect.com/science/article/abs/pii/S1049250X10590050
