# v0.81 时间相关环境漂移、参数化 Bootstrap 与光子身份误报风险

## 总结

对“原始光子永久存在”假说进行条件性统计检验：若普通环境相位漂移具有时间相关性，错误地把测量当作独立同分布，会显著低估标准误并制造虚假的新物理显著性。**本工作是明确参数下的玩具统计模型，未推导 QED 新效应。**

## 数学模型

从 test 与 calibration 相位拟合的差得到残差
\[
r_t=\delta+u_t+\epsilon_t,\quad u_t=\rho u_{t-1}+\xi_t,
\]
其中 \(\xi_t\sim N(0,\sigma_u^2)\)、\(\epsilon_t\sim N(0,\sigma_r^2)\)，假定独立且 AR(1) 平稳初始化。这里 \(u_t\) 是两组实验之间**未能通过校准消掉的差分环境漂移**，而 \(\delta\) 是待检验的额外相位。

\[
\Sigma_{ij}=\frac{\sigma_u^2}{1-\rho^2}\rho^{|i-j|}+\sigma_r^2\delta_{ij}.
\]

GLS 估计量：
\[
\hat\delta=\frac{\mathbf1^T\Sigma^{-1}r}{\mathbf1^T\Sigma^{-1}\mathbf1},
\quad \mathrm{SE}(\hat\delta)=(\mathbf1^T\Sigma^{-1}\mathbf1)^{-1/2}.
\]

## 参数与实际运行结果

设 \(n=80,\rho=.92,\sigma_u=.09\mathrm{rad},\sigma_r=.05\mathrm{rad}\)。注意 \(\sigma_u\) 是 AR(1) 创新项标准差，平稳差分漂移的 SD 约为 .2296 rad。

在固定随机种子的 **400 组**模拟数据集里，名义双侧 5% 的检测结果：

| 情况 | 错误地忽略相关性 | 正确按已知协方差计算 |
|---|---:|---:|
| \(\delta=0\)：模拟误报率 | **94.25%** | **5.25%** |
| \(\delta=.15\)：模拟拒绝率（功效） | 97.00% | 29.00% |

独立误差标准误 .00559017 rad；GLS 标准误 **.11120794 rad**。独立近似忽略了差分环境漂移，所以它不是有效的标准误。由 1600 个零假设模拟得到参数化 Bootstrap 95% 截止值 **3.8426865**，与 \(\chi_1^2\) 截止值 **3.8414588** 接近。

这不是宣称 Bootstrap 消除了未知参数问题：**本轮协方差 \(\Sigma\) 是事先给定的**，没有从数据估计 \(\rho\)、方差参数，也没有每轮重新拟合；属于 *known-covariance parametric bootstrap*。

## 数学可辨识性仍然存在根本障碍

普通模型的组间未知固定偏置 \(b\) 与身份相位 \(\delta\) 只通过 \(\delta+b\) 进入概率时，即便完全知道 AR(1) 协方差，也无法单独识别 \(\delta\)。即 \(b\rightarrow b+c,\delta\rightarrow\delta-c\) 维持同样分布。

因此，调整显著性不构成对永久光子身份的证据；即使实验中看到异常相位，也须排除普通材料相干、时间相关漂移、设备系统误差及已知模式自由度。

## 本轮边界与 v0.82

- 使用拟合相位的高斯近似，而非原始光电探测 Poisson/multinomial 计数。
- 假设时间平稳 AR(1)，真实器件可能包含 1/f 噪声、随机游走和突变。
- covariance 已知，未评估由同一实验拟合 noise parameters 所带来的检验失真。
- 下一轮 v0.82 应模拟原始光子计数，对未知噪声参数进行独立校准与 fit-and-refit Bootstrap，并做噪声模型错设鲁棒性分析。

## 可复现文件

- \`models/correlated_drift_v081.py\`: AR1 covariance、GLS、Bootstrap、模拟。
- \`tests/test_correlated_drift_v081.py\`: 27 项单元测试（本地运行全部通过，0.027 秒）。
- \`experiments/run_v081.py\`: 复现指标。
- \`results/correlated_drift_v081.json\`: 数值结果。
- \`results/test_results_v081.txt\`: 实际本地测试输出摘要。

依赖 Python 3.10+、NumPy、SciPy。

## 参考

Box & Jenkins, *Time Series Analysis: Forecasting and Control*；Davison & Hinkley, *Bootstrap Methods and Their Application*；Rothenberg, *Identification in Parametric Models*, https://doi.org/10.2307/1913267 。
