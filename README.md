## TextCNN文本情感分类任务

### 一、数据集介绍

数据集为IMDB情感分析数据集（英文，二分类），其中训练集和测试集各有25000个样本，每个样本为一个文件。标签为积极和消极的样本数相同，均为12500个，每一个样本为一段影评。

结构如下：

```python
aclImdb
├── test
│   ├── neg
│   └── pos
└── train
    ├── neg
    └── pos
```



### 二、TextCNN模型

**输入层**：也称embedding层，TextCNN的输入序列是一个固定长度的句子：图示中是由11个词组成一条句子（context_size=11），每个词用6维词向量表示(embedding_dim=6),即输入通道数in_channels=6。因此输入序列shape=(11,6)，加上Batch这个维度，则是shape=(batch_size,context_size,embedding_dim)=(B,11,6)
**CNN层**:也称卷积层，由一维卷积核（Conv1d）组成，左边的一维卷积核大小为2（kernel_size=2），输出通道数分别设为4；右边的一维卷积核大小为4（kernel_size=4），输出通道数分别设为5；卷积步长stride=1；因此，一维卷积计算后，左边一维卷积输出宽度=11−2+1=10，右边边一维卷积输出宽度11−4+1=8。输出通道数分别自行设置。（一般有几个卷积核就有几个输出通道）
**池化层**:将CNN层的输出的9个通道经过时序最大池化（max_pool1d），并将池化输出cat连结成一个9维向量。
**分类层**:也是输出层，由简单的全连接层组成；对于简单二分类，其输出维度2，即正面情感和负面情感的预测（概率）。



补充：

1、嵌入层：使用了预训练词向量Glove。

2、CNN常用于计算机视觉领域，图像是二维的。而词却只能用一维表示，虽然长文本可以当作二维的，但在卷积时应采用一维卷积核进行操作（因为在词向量的维度表示上，多维卷积核没有意义，所以只需改变卷积核的宽度）

3、TextCNN采用时序最大池化，提取时序数据中最重要的特征（在构建词向量时对于较短的句子通常使用0向量补全，使用最大池化可以过滤掉这些补0的数据）

4、数据经过池化处理后，作为输入送入全连接层，全连接层起到将学到的特征表示映射到样本标记空间的作用。在实际应用中为了防止过拟合，通常在全连接层加dropout来提升模型的泛化能力。

5、全连接层的输出是0到1之间的概率值，要解决分类问题需要使用softmax函数来将这些概率转化为离散的0或1类标。

6、对于模型中的嵌入层有：冻结层、非冻结层，一个是固定权重，主要是为了获取词向量，另一个是可训练权重。
