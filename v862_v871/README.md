# v8.62–v8.71 相关标定、交换与漂移协议

- [v8.62 标定协方差的正交模式](v862_zh.md)
- [v8.63 固定边际误差的最坏相关](v863_zh.md)
- [v8.64 主效应标定为何不足](v864_zh.md)
- [v8.65 匹配参考恢复参数秩](v865_zh.md)
- [v8.66 稳定交换分离候选与普通响应](v866_zh.md)
- [v8.67 随位置变号的普通反例](v867_zh.md)
- [v8.68 ABBA 时序与二次漂移](v868_zh.md)
- [v8.69 配对参考的协方差收益](v869_zh.md)
- [v8.70 功效与曝光预算](v870_zh.md)
- [v8.71 最小满秩实验协议](v871_zh.md)

[模型](model.py) · [测试](test_model.py) · [执行笔记本](reproduce.ipynb) · [反方审稿](referee_zh.md) · [修订稿](manuscript_zh.md)

## 已知理论与正式出处

本批使用的是标准线性模型、广义最小二乘、协方差传播、配对差分和 Neyman–Pearson 功效设计，不把这些数学结果包装为新物理。主要正式出处为 A. C. Aitken, *On Least Squares and Linear Combination of Observations*, Proceedings of the Royal Society of Edinburgh **55** (1935), 42–48, DOI: [10.1017/S0370164600014346](https://doi.org/10.1017/S0370164600014346)；J. Neyman and E. S. Pearson, *On the Problem of the Most Efficient Tests of Statistical Hypotheses*, Philosophical Transactions A **231** (1933), 289–337, DOI: [10.1098/rsta.1933.0009](https://doi.org/10.1098/rsta.1933.0009)；D. W. Allan, *Statistics of Atomic Frequency Standards*, Proceedings of the IEEE **54** (1966), 221–230, DOI: [10.1109/PROC.1966.4634](https://doi.org/10.1109/PROC.1966.4634)。原四格中心量仍来自项目此前核对的公开图上点，不能替代逐事件数据。

## 证据等级

v8.62–v8.71 全部是解析恒等式或固定输入的合成数值验证；没有新增真实实验、没有外部同行评审，也没有发现永久身份独有预测。可证伪结论均以参考匹配、交换变换律和漂移模型成立为条件。
