# v0.82：泊松原始计数、时间相关潜在漂移与重新拟合 Bootstrap

**科学定位：** 用于研究光子连续存在假说（PCH-A）的统计可辨识性，不是量子电动力学（QED）的新动力学理论，更没有提供“原始光子永远存在”的独立证据。

## 摘要

v0.81 使用从实验中拟合的高斯相位残差。本轮进一步使用**原始探测器计数**，将校准组与实验组、两路干涉输出、独立暗帧以及时间相关环境漂移纳入一个联合模型。拟合两种假设时，重新优化探测效率、可见度、暗计数、公共相位，以及各时间点的隐状态。对零假设模型进行参数化 Bootstrap 时，每个新模拟数据集都分别重新拟合零假设与备择假设。

## 生成模型

每组实验在时间点 t 产生两个独立的泊松计数：

\[
Y_{t,z,\pm}\sim\mathrm{Poisson}(\mu_{t,z,\pm}),\quad
\mu_{t,z,\pm}=\frac{N\eta}{2}\left[1\pm V\cos(x_t+\beta+u_t+z\delta)\right]+d,
\]

其中 z=0 为校准组、z=1 为实验组；在每个 t 还采集两个独立暗帧 \(D_{t,k}\sim\mathrm{Poisson}(d)\)。这里的 N 是已知的平均入射光子曝光量；泊松光源假设与固定入射试验次数下的二项/多项分布不同。

时间相关环境漂移满足平稳 AR(1) 模型：

\[
u_t=\rho u_{t-1}+\xi_t,\quad \xi_t\sim\mathcal N(0,\sigma^2),\quad
\operatorname{Cov}(u_t,u_s)=\frac{\sigma^2}{1-\rho^2}\rho^{|t-s|}.
\]

待拟合 \(\eta,V,d,\beta,\delta,u_1,\ldots,u_T\)，为降低潜在漂移过拟合，以 \(\frac12u^\mathsf{T}\Sigma^{-1}u\) 作为高斯先验的二次惩罚。取 \(H_0:\delta=0\) 和 \(H_1:\delta\in[-0.7,0.7]\)，最小化带先验惩罚的泊松负对数似然。

**统计术语注意：** 此时的两倍目标函数差是*惩罚化 profile/MAP 比较统计量*，而不是对隐变量完全边缘积分的标准似然比。因此不能直接用 \(\chi^2\) 阈值判断显著性；本轮采用模型内参数化 Bootstrap 取得经验阈值。

## 数值实验

固定随机种子，10 个时间点，平均入射曝光 N=80，真值为 \(\eta=0.72,V=0.75,d=0.8,\beta=0.21,\rho=0.8,\sigma=0.12\)。另外生成一组设有 \(\delta=0.18\) 的模拟数据。

| 数值 | 结果 |
| --- | ---: |
| 零效应数据集惩罚化两倍差统计量 | 2.1025493621 |
| 信号数据集惩罚化两倍差统计量 | 3.7593430178 |
| 零效应参数化 Bootstrap 次数 | 60 |
| Bootstrap 95% 分位阈值 | 3.1844867862 |
| 零效应数据集加一修正经验 p 值 | 0.1803278689 |
| 两模型都报告优化收敛的重复数 | 60 / 60 |
| 本地 unittest | 29 / 29 通过 |

本例并非真实实验；60 次 Bootstrap 分辨率有限，p 值的最小正分辨率是 1/61，而且不适合宣称稳健的实际 5% 误报率。表中“含信号”模拟的统计量不能直接拿零数据集的 p 值进行判断，应对对应数据集另做 Bootstrap。

## 永久身份与普通记忆的根本退化

假若普通量子记忆模型允许一个实验组特有的额外偏置 b，则在所有实验数据中身份效应与它都以 \(b+\delta\) 进入测量概率。允许 b 自由拟合时，任何 \(\delta\) 都可通过 \(b'=b+\delta\) 被普通模型吸收。因此，在没有独立物理原理禁止普通组别偏置时，**即使拟合程序、噪声模型和 Bootstrap 都完美，身份参数仍存在结构性不可辨识。**

## 主要限制

1. 仅使用单个平稳 AR(1) 潜在漂移；实际器件可能存在 1/f 噪声、突变、非平稳随机游走。
2. 漂移的 \(\rho\)、\(\sigma\) 在本轮视为通过独立实验已知，并未在 Bootstrap 中重新估计；这是需要后续消除的重要限制。
3. 光源被建模为泊松化曝光，忽略死时间、漏脉冲、后脉冲、非均匀暗计数和探测器饱和。
4. 对漂移采用联合 MAP 而非完全积分，未建立严格渐近理论。
5. 60 次 Bootstrap 只能演示复现机制，不能用于高置信显著性声明。
6. 额外相位本身不是永久光子身份的独特预言；普通材料记忆和未知仪器相位可给出相同概率。

## 下一轮 v0.83

进行独立噪声校准并在每次 Bootstrap 中重新估计 \(\rho,\sigma\)；引入非平稳漂移对模型错误的鲁棒性检验，增加重复次数，考虑普通模型的组别漂移，并将模型选择限制写成预注册证伪规则。

## 复现

依赖 Python 3.10+、NumPy、SciPy；从 GitHub 仓库根目录运行：

\`\`\`bash
python -m unittest discover -s tests -p 'test_count_hierarchy_v082.py' -v
python -m experiments.run_v082
\`\`\`

研究代码：models/count_hierarchy_v082.py。测试：tests/test_count_hierarchy_v082.py。GitHub 测试未在 CI 独立运行；本地原始文件跑过 29 项，模型与测试已同步可复现。

## 方法参考

- Cox & Hinkley, *Theoretical Statistics* (1974).
- Davison & Hinkley, *Bootstrap Methods and Their Application* (1997).
- Durbin & Koopman, *Time Series Analysis by State Space Methods* (2012).
- Rothenberg, *Identification in Parametric Models* (1971), https://doi.org/10.2307/1913267 .
