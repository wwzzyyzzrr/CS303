#   SVM
##  11610634    汪至圆

### 关于提交内容:
提交内容包括一份报告, 一份要求的SVM.py代码, 以及SMO与Gradient Descent各一份训练代码以及一份测试代码分别为SMO.py, SVM_GD.py;测试代码则是在名字后加有_test后缀, 还有自己写的一个测试程序autoTest.py, Sakai上提供的train_data, 以及自己在训练过程中将原始数据分割成的训练数据与测试数据test以及test0, 还有训练产生的模型smoModel和GDModel. 提交的SVM.py文件是采用了梯度下降算法

### 关于验证:
**对于pdf要求的验证方法可以直接运行SVM.py进行验证.**

需要手动验证时,可以直接运行autoTest.py, 可以自行设定原始数据来源(默认为sakai上的训练数据), 设定训练数据占据原始数据的比例(range(0,1), 默认值为0.9), 设定运行的算法(梯度下降输入GD, smo则输入其他的任意字符即可, 默认值是梯度下降算法), 设定运行次数(默认为5次)

如果需要单独运行训练数据与测试数据, 直接调用训练代码与测试代码即可, 按照提示输入路径.

### 关于梯度下降算法
在梯度下降算法中, 我使用loss值作为标记, 根据当前loss值与初始loss值的比例关系进行比较来确定当前的下降步长(learningRate), 但是目前这个对应关系只是在sakai上那个数据中测试过, 还未在其他数据集中测试过, 不能保证这个对应关系是否稳定. 如果出现较大偏差, 建议将SVM_GD.py的40-47行删去即可.