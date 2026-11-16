# v0.78 — 损耗、退相干与统计可辨识性

**研究结论：** 如果“永久身份模型”和“普通环境量子记忆模型”给出完全相同的可观测概率分布，即使增加无限次独立重复测量也无法区分。只有额外引入独立可测动力学，才会出现可检验偏差；可测偏差本身并不能证明历史上的同一个光子一直存在。

## 模型

在 |vac>, |a>, |b> 三维空间定义

\[
\rho=(1-\eta)|vac\rangle\langle vac|+
\frac{\eta}{2}\big(|a\rangle\langle a|+|b\rangle\langle b|
+Ve^{i\phi}|a\rangle\langle b|+Ve^{-i\phi}|b\rangle\langle a|\big),
\]

其中 \(\eta\in[0,1]\) 是光学存活率，\(V\in[0,1]\) 是简化相干可见度。测量损失、正端口、负端口得到

\[
P_{\rm loss}=1-\eta,\quad
P_+=\frac{\eta}{2}(1+V\cos\phi),\quad
P_-=\frac{\eta}{2}(1-V\cos\phi).
\]

该密度矩阵半正定、迹为 1。它是开放量子系统的有效态模型，不是由完整 QED 或之前 v0.76 EFT 推导的吸收机理。

## 操作等价的统计学 no-go

若恒等地有 \(P_I=P_M\)，则 \(D_{\rm TV}(P_I,P_M)=D_{\rm KL}(P_I\Vert P_M)=0\)，对任意独立试验次数 \(N\) 都有 \(P_I^{\otimes N}=P_M^{\otimes N}\)。增加样本量不能区分两个只是内部标签解释不同的模型。这是**在允许观测集合内的条件性结论**，不是所有 PCH-A 理论被禁止的一般定理。

## 一个可检验但并非身份专有的相位偏移

令 \(H_0:P(\eta,V,\phi)\)、\(H_1:P(\eta,V,\phi+\delta)\)，参数取
\(\eta=0.65,V=0.8,\phi=\pi/2,\delta=0.2\) rad、\(N=1000\)：

| 结果 | H0 | H1 |
| --- | ---: | ---: |
| Loss | 0.3500000000000000 | 0.3500000000000000 |
| Plus | 0.32499999999999996 | 0.2733459739932841 |
| Minus | 0.32499999999999996 | 0.3766540260067158 |

计算：\(D_{\rm KL}(P_1\Vert P_0)=0.008244573973433422\) nats/attempt，\(\mathbb E_{H_1}[2\log\Lambda]=2ND_{\rm KL}=16.489147946866844\)。固定随机种子 77 的单次模拟计数为 [345,276,379]。

这不是实验测量，也不能把 16.49 直接解释成“4σ”或其他发现显著性：上述模型是已知参数的简单假设对简单假设；未知 nuisance 参数、系统误差和相位搜索需独立校准。

## Fisher 信息

若 \(\eta,V\) 已知且概率正，\(\mathcal I_\phi=\sum_j(\partial_\phi P_j)^2/P_j\)。在 \(\phi=\pi/2\)，
\[
\mathcal I_\phi=\eta V^2=0.416 \text{ per attempt},\quad
\mathcal I_{1000}=416.
\]
Cramér–Rao 下界只适用于相应正则条件下的无偏估计器，不包含探测暗计数与实验漂移。

## 理论含义与限制

1. 纯身份重标记与普通记忆模型严格等价，即使无限数据也无法区分。
2. 真实的相位偏移可检测，但普通材料量子相干、谱模式、干涉仪漂移也可以产生，因此**相位偏移不是永久身份专属证据**。
3. 本模型忽略暗计数、设备漂移、未知效率、非独立试验、模式失配与完整 QED 动力学。
4. 下一轮 v0.79：引入未知相位/可见度、暗计数等 nuisance 参数，检查 Fisher 信息矩阵的秩、profile likelihood 和身份参数的结构性不可辨识。

## 复现

需 Python 3.10+、numpy。本地 \`python -m unittest discover -s tests -v\` 运行 **27 个测试全部通过**（0.008 秒）。见 \`models/loss_dephasing_v078.py\`、\`tests/test_loss_dephasing_v078.py\`、\`experiments/run_v078.py\`、\`results/loss_dephasing_v078.json\`。

## 参考

Helstrom, *Quantum Detection and Estimation Theory* (1976);
Nielsen & Chuang, *Quantum Computation and Quantum Information* (2010);
Cover & Thomas, *Elements of Information Theory* (2006);
Heshami et al., *Quantum memories* (2016), https://pmc.ncbi.nlm.nih.gov/articles/PMC5020357/ .
