# v4.62–v4.71 场耦合与普通光学响应

| 轮次 | 报告 | 结果 |
|---|---|---|
| v4.62 | [规范一致性](v462_zh.md) | 附加局域矢势源必须守恒或有补偿 |
| v4.63 | [偏振旋转](v463_zh.md) | 正距离依赖独立偏置校准 |
| v4.64 | [开放腔](v464_zh.md) | 普通内部端口可承载缺失激发 |
| v4.65 | [反旋波项](v465_zh.md) | 指定强耦合下，标准模型与旋波解最大差 .114 |
| v4.66 | [Bell 阈值](v466_zh.md) | 退相干和白噪声决定标准 CHSH 阈值 |
| v4.67 | [环境条件干涉](v467_zh.md) | 环境误码限制条件可见度，未条件化边缘不变 |
| v4.68 | [群时延](v468_zh.md) | 普通全通散射平坦光强可伴随相位延迟 |
| v4.69 | [有限相位参考](v469_zh.md) | 有界参考的最优对比为 cos[π/(L+1)] |
| v4.70 | [联合校准界](v470_zh.md) | 联合普通机制距离可从 .156 放宽至零 |
| v4.71 | [预注册留出](v471_zh.md) | 独立标定的保守门槛控制一类错误，小效应检验功效下降 |

```bash
python -m v462_v471.model
python -m unittest -v v462_v471.test_model v452_v461.test_model v442_v451.test_model v432_v441.test_model
PYTHONPATH=. python -Xfrozen_modules=off tools/execute_research_notebook.py v462_v471/reproduce.ipynb
```

[修订稿](manuscript_zh.md) · [内部反方审稿](review_zh.md) · [复现笔记本](reproduce.ipynb) · [输出](results.json) · [验证记录](verification.json)
