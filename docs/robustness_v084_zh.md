# v0.84：噪声模型错设、经验型一错误率与光子身份假说

**研究性质：** 计算机模拟与统计可辨识性研究，不是 QED 模型，也不是“原始光子永久存在”的实验证据。

## 研究问题

在没有身份效应的情况下，普通环境漂移是否能产生错误的新物理信号？沿用 v0.83 的独立校准与参数 Bootstrap 思路，但为了做外层误报率评估，改为从**原始 Poisson 计数提取相位，再做 Gaussian-approximate GLS**。它与上一版本的完整 Poisson 潜在态 MAP 统计量**不是同一个检验**。

## 1. 测量模型

每个时间点 t 有 calibration 与 test 两组、两个正交相位设置 x=0 和 π/2，以及每个设置正、负两端口，总共八个独立 Poisson 计数：

\[
Y_{t,g,q,\pm}\sim\mathrm{Poisson}\left(
\frac{N\eta}{2}[1\pm V\cos(\beta+x_q+g(u_t+b))]+d
\right).
\]

其中 g=0 是 calibration，g=1 是 test；u_t 是**实验组相对校准组的差分漂移**（不是两组共享并自动抵消的共模漂移），b 是普通组间相位偏置。

令端口对比度 \(C_{t,g,q}=Y_{+}-Y_{-}\)，得到
\[
\hat\phi_{t,g}=\mathrm{atan2}(-C_{t,g,\pi/2},C_{t,g,0}),\quad
r_t=\mathrm{wrap}(\hat\phi_{t,1}-\hat\phi_{t,0}).
\]

独立传感器的平稳 AR(1) 记录用于通过方差去噪的 Yule–Walker 矩估计来拟合 rho 和 sigma（不是 v0.83 的 Kalman MLE）。随后对 r_t 用 Toeplitz GLS 检验其非零均值。拟合协方差：

\[
\Sigma_{ij}=\frac{\sigma^2}{1-\rho^2}\rho^{|i-j|}
+\delta_{ij}\frac{2(N\eta+2d)}{(N\eta V)^2}.
\]

每个内层 Bootstrap 生成新的独立相位传感器序列、重新估计 rho 和 sigma，生成新的 Poisson 计数，从计数重新提取相位和 GLS 检验统计量。加一修正经验 p 值为
\[
p=(1+\#\{T_b\ge T_{\rm obs}\})/(B+1).
\]

注意：本轮未在每次复制中重新估计探测效率、可见度或暗计数，也未执行完整 Poisson latent-state likelihood 积分。

## 2. 三种无身份效应的数据生成机制

1. **stationary**：u_t 为平稳 AR(1)，普通偏置 b=0，符合受检零模型。
2. **random_walk**：u_t 是步长 SD=0.075 rad 的随机游走，b=0；违反平稳 AR(1)。
3. **ordinary_group_bias**：u_t 为平稳 AR(1)，b=0.22 rad；普通实验组偏置被受检模型遗漏。

这三种情况下，真实“永久身份”效应均设为零。

## 3. 已执行的数值结果

N=700，eta=0.72，V=0.8，d=0.8，beta=0.18 rad；真实 rho=0.78，创新 sigma=0.065 rad，独立传感器噪声 SD=0.025 rad。光学实验24时间点，传感器100时间点。每场景120组外层模拟、每组79次 Bootstrap，随机种子 8401。

| 生成情景 | 拒绝/外层组数 | 比例 | 蒙特卡洛标准误 |
|---|---:|---:|---:|
| 平稳 AR(1) | 4/120 | **3.33%** | 1.64个百分点 |
| 非平稳随机游走 | 69/120 | **57.50%** | 4.51个百分点 |
| 普通组间偏置 | 108/120 | **90.00%** | 2.74个百分点 |

固定模拟条件下，噪声模型正确时拒绝率接近标称5%；噪声模型不覆盖普通机制时，可能频繁拒绝受检零模型。**后两项不应严格称为完整物理零假设下的型一错误率**：因为生成数据的真实普通机制被排除在受检零模型之外，所以拒绝意味着模型错设，而非身份假说被支持。

B=79 次内层复制意味着 p 值分辨率为 1/80，120 次外层模拟仍有明显蒙特卡洛误差。因此该实验不能验证任意物理系统的精确检验水平。

## 4. 不可辨识性和停止条件

如果“永久身份”参数 delta 和普通实验组偏置 b 只以 b+delta 进入概率，则
\[
P_{\rm identity}(\delta,b)=P_{\rm ordinary}(0,b+\delta).
\]
任何统计精度和 Bootstrap 程序都不能破解此结构性不可辨识性，除非引入新的物理可观测量或独立限制。

下一轮 v0.85：将平稳 AR(1)、随机游走和普通组间偏置都纳入公平的普通记忆复合零模型；进一步对 eta/V/d 进行独立校准和不确定度传播；建立预注册证伪标准。若“身份效应”始终被普通偏置重参数化吸收，应停止将其称为新物理预测，而可保留为数学等价性研究。

## 5. 复现

Python 3.10+、NumPy、SciPy；在研究根目录运行：

\`\`\`bash
python -m unittest discover -s tests -p 'test_robustness_v084.py' -v
python -m experiments.run_v084
\`\`\`

真实本地执行 **29 项单元测试全部通过（0.582s）**。完整模拟 p 值序列和测试日志保存在用户下载的 \`photon_v084_complete.zip\` 中。

## 6. 参考文献

- Rothenberg (1971), *Identification in Parametric Models*, https://doi.org/10.2307/1913267 .
- *Parametric bootstrap under model mis-specification* (2012), https://doi.org/10.1016/j.csda.2012.01.018 .
- *Testing for correlation between two time series using a parametric bootstrap*, https://pmc.ncbi.nlm.nih.gov/articles/PMC9041796/ .
