# v8.82–v8.91 显式标签哈密顿量审计

- [v8.82 守恒色散标签耦合](v882_zh.md)
- [v8.83 定粒子数输入不可见](v883_zh.md)
- [v8.84 Ramsey 相位可见性](v884_zh.md)
- [v8.85 普通失谐精确重拟合](v885_zh.md)
- [v8.86 固定标签等价于参数](v886_zh.md)
- [v8.87 置换对称约束](v887_zh.md)
- [v8.88 局域幺正与无信号](v888_zh.md)
- [v8.89 守恒交换耦合](v889_zh.md)
- [v8.90 普通退相干通道](v890_zh.md)
- [v8.91 条件性无区分结论](v891_zh.md)

[模型](model.py) · [测试](test_model.py) · [执行笔记本](reproduce.ipynb) · [反方审稿](referee_zh.md) · [修订稿](manuscript_zh.md)

## 正式理论对照

本批使用标准量子光学和开放系统模型：Jaynes & Cummings, *Proc. IEEE* **51**, 89 (1963), DOI [10.1109/PROC.1963.1664](https://doi.org/10.1109/PROC.1963.1664)；Gorini, Kossakowski & Sudarshan, *J. Math. Phys.* **17**, 821 (1976), DOI [10.1063/1.522979](https://doi.org/10.1063/1.522979)；Lindblad, *Commun. Math. Phys.* **48**, 119 (1976), DOI [10.1007/BF01608499](https://doi.org/10.1007/BF01608499)；以及上一批列出的 Stinespring 和相同粒子置换对称文献。

## 证据状态

结果是固定种子有限维解析/数值验证，不是真实实验。一个守恒的标签色散耦合在 Ramsey 输入上可见，但与普通频率失谐完全等价；守恒交换耦合也正是普通二模交换。未得到身份独有预测。
