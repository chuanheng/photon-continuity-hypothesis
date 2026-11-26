# v8.72–v8.81 永久身份标签的操作可观测性审计

- [v8.72 静默标签与偏迹](v872_zh.md)
- [v8.73 标签内演化仍不可见](v873_zh.md)
- [v8.74 因子化动力学的操作等价](v874_zh.md)
- [v8.75 可访问耦合使标签可见](v875_zh.md)
- [v8.76 普通内部态的相同膨胀](v876_zh.md)
- [v8.77 置换不变观测与个体编号](v877_zh.md)
- [v8.78 吸收再发射的替换通道](v878_zh.md)
- [v8.79 多时间记忆不是身份专属](v879_zh.md)
- [v8.80 有限控制集的操作等价](v880_zh.md)
- [v8.81 核心假设的最低物理要求](v881_zh.md)

[模型](model.py) · [测试](test_model.py) · [执行笔记本](reproduce.ipynb) · [反方审稿](referee_zh.md) · [修订稿](manuscript_zh.md)

## 原始论文与正式理论

本批按相同粒子置换不变性、量子通道膨胀、超选择和操作等价性核对核心命题。正式出处包括 Witmer & Vinti, *Phys. Rev.* **47**, 538 (1935), DOI [10.1103/PhysRev.47.538](https://doi.org/10.1103/PhysRev.47.538)；Messiah & Greenberg, *Phys. Rev.* **136**, B248 (1964), DOI [10.1103/PhysRev.136.B248](https://doi.org/10.1103/PhysRev.136.B248)；Girardeau, *Phys. Rev.* **139**, B500 (1965), DOI [10.1103/PhysRev.139.B500](https://doi.org/10.1103/PhysRev.139.B500)；Stinespring, *Proc. AMS* **6**, 211 (1955), DOI [10.1090/S0002-9939-1955-0069403-4](https://doi.org/10.1090/S0002-9939-1955-0069403-4)；Wick, Wightman & Wigner, *Phys. Rev.* **88**, 101 (1952), DOI [10.1103/PhysRev.88.101](https://doi.org/10.1103/PhysRev.88.101)；Spekkens, *Phys. Rev. A* **71**, 052108 (2005), DOI [10.1103/PhysRevA.71.052108](https://doi.org/10.1103/PhysRevA.71.052108)。

## 证据等级

所有结论均为有限维解析模型和固定种子数值核对。没有新增真实实验。主要结论是条件性无区分结果：若永久身份标签不耦合可访问操作，它在操作上沉默；若允许耦合，同一输入输出通道可由普通内部态或环境记忆实现。因此仍无身份独有预测。
