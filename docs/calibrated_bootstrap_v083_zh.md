# v0.83：独立 AR(1) 噪声校准与参数化 Bootstrap 的重新拟合

## 摘要

本版本承接 v0.82 的原始光学 Poisson 探测计数模型。此前将潜在环境漂移的 AR(1) 超参数 \(\rho,\sigma\) 视为已知。本轮新增**独立相位传感器记录**，用 Kalman innovations 似然估计 \(\rho,\sigma\)，并且在参数化 Bootstrap 的**每一次复制**中，生成新的传感器数据、重新估计超参数、重新生成 Poisson 计数、分别重新拟合 \(\delta=0\) 及允许 \(\delta\ne0\) 的惩罚化 MAP 模型。

此处的 \(\delta\) 仅为假设的额外相位，不是 QED 推导的永久光子身份相位。全部数据均为计算机模拟，不属于实验发现。

## 1. 数学模型

假设传感器记录 \(c_t=u_t+\epsilon_t\)，潜在相位满足平稳 AR(1)：
\[
u_t=\rho u_{t-1}+\xi_t,\quad
\xi_t\sim\mathcal N(0,\sigma^2),\quad
\epsilon_t\sim\mathcal N(0,\tau^2).
\]
初态 \(u_0\sim\mathcal N(0,\sigma^2/(1-\rho^2))\)，传感器读出噪声 \(\tau=.03\) rad 是**已知参数**。

采用 Kalman 一步预测均值 \(m_t\) 和方差 \(P_t\)，创新方差 \(S_t=P_t+\tau^2\)、残差 \(e_t=c_t-m_t\)。最小化：
\[
-\log L(\rho,\sigma)=\frac12\sum_t[\log(2\pi S_t)+e_t^2/S_t].
\]
更新 \(K_t=P_t/S_t\)，再经过 AR(1) 状态预测。

另有光学试验，采用与传感器**分布参数相同、但具体轨迹独立**的 AR(1) 漂移 \(v_t\)。两路探测的泊松平均数为
\[
\mu_{t,z,\pm}=\frac{N\eta}{2}
\bigl[1\pm V\cos(x_t+\beta+v_t+z\delta)\bigr]+d.
\]
其中 \(z=0\) 为 calibration，\(z=1\) 为 test。光学潜在态使用高斯 AR(1) 二次惩罚进行 MAP 拟合，而未做严格的完整边缘积分。

## 2. 全流程 Bootstrap

1. 在独立传感器记录上估计 \((\hat\rho,\hat\sigma)\)。
2. 把该估计代入 Poisson 模型，拟合 \(H_0:\delta=0\) 和 \(H_1:\delta\ne0\)，得统计量 \(T=2(Q_0-Q_1)\)，Q 为含潜在态惩罚的负对数目标。
3. 从 \(H_0\) 拟合参数生成新的独立传感器记录，**重新估计**其 \(\rho,\sigma\)。
4. 从 \(H_0\) 生成一条新的潜在环境漂移，并生成两组 Poisson 计数及暗帧，分别重新拟合 \(H_0,H_1\)。
5. 在 B 次复制后用加一修正 \(p=(1+\#\{T_b\ge T_{\rm obs}\})/(B+1)\)。

这只是**已知传感器读出噪声、独立共享分布参数、惩罚化 MAP 统计量**下的全流程复制，尚非所有未知参数的完整联合层次模型。

## 3. 实际模拟结果

采用独立相位记录长度 120，光学扫描时间点 10；真值 \(\rho=.8,\sigma=.12\)，每条件 Poisson 平均曝光 \(N=80\)。固定随机种子，B=24：

| 指标 | 计算结果 |
| --- | ---: |
| Kalman 估计 \(\hat\rho\) | 0.8613197598 |
| Kalman 估计 \(\hat\sigma\) | 0.1160137401 |
| 无额外相位数据 \(T_{\rm obs}\) | 0.1159040230 |
| Bootstrap 第 95 百分位 | 6.2856378132 |
| 加一修正经验 p 值 | 0.680000 |
| 超参数重新拟合 | 24/24 成功 |
| H0 与 H1 成对拟合 | 24/24 收敛 |
| 另一个独立含 \(\delta=.18\) 数据的 T | 6.2858668926 |
| 一个非平稳随机游走+普通 test 偏置例子的 T | 2.4961335665 |
| 本地实际单元测试 | 26/26 通过 |

**重要：** 两个独立数据集的统计量不能直接共享一个 p 值。仅 B=24 次，经验 p 值精度粗糙，不能据此宣称任何高显著性发现。错设模型例子只是单个构造，不能解释为总体误报率。

## 4. 数学结论：根本不可辨识性仍在

如果 ordinary-memory 模型可以产生一个普通 test 组偏置 b，则可测概率中的 test 相位取决于 b+δ。任何 δ 都可以被 b' = b+δ 吸收：
\[
p_{\rm memory}(b+\delta)=p_{\rm identity}(b,\delta).
\]
无论有多少 Bootstrap，凡是只允许观测该总相位的实验，都无法单独验证永久光子身份。

这是一条关于指定实验模型的**操作性等价**结论，不是关于所有可能隐藏身份物理理论的绝对 no-go。

## 5. 局限与下一步

- 传感器误差标准差 τ 仍固定且已知；
- 传感器与光学漂移共享 AR(1) 超参数，这需要真实标定；
- 非平稳 random walk、1/f 漂移、组别独立偏差会造成模型错设；
- 使用隐状态 MAP 而非完全积分的统计量，尚缺乏已验证的频率学覆盖率分析；
- B=24 仅验证算法，不足以衡量 5% 型一错误；
- 标准 QED 之外的独立光子身份相互作用仍未构造，未产生独有实验预测。

**v0.84：** 用大量外层模拟评估所选统计检验在正确定义与错设噪声模型下的实际型一错误率，允许非平稳漂移和普通组间相位偏置，预注册两理论公平比较及停止条件。

## 6. 复现及文件

依赖 Python 3.10+、NumPy、SciPy。从 GitHub 仓库根目录运行：

\`\`\`bash
python -m unittest discover -s tests -p 'test_calibrated_bootstrap_v083.py' -v
python -m experiments.run_v083
\`\`\`

- 依赖前一版本：\`models/count_hierarchy_v082.py\`，当前研究分支已存在；
- 新模型：\`models/calibrated_bootstrap_v083.py\`；
- 单元测试：\`tests/test_calibrated_bootstrap_v083.py\`；
- 实验入口：\`experiments/run_v083.py\`；
- 数值摘要：\`results/calibrated_bootstrap_v083.json\`。

参考：Durbin & Koopman, *Time Series Analysis by State Space Methods*, 2nd ed.; Davison & Hinkley, *Bootstrap Methods and Their Application*; Rothenberg, T.J. (1971), *Identification in Parametric Models*, https://doi.org/10.2307/1913267 .
