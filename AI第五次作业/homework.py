import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split

"""
利用正态分布的随机数(高斯噪声)生成基于某个直线附近的若干个点
y= wx + b
weight直线权值
bias直线偏置
size点的个数
"""


def random_point_nearby_line(weight, bias, size=10):
    # 根据np.linespace来产生-1，1之间size个等距点的数组-> x_point
    x_point = np.linspace(-1, 1, size)
    # 使用np.random.normal来产生符合正态分布的，和x_point同型的数组 -> noise
    noise = np.random.normal(0, 0.3, size)
    # 使用传进来的参数weight, bias和上一步产生的noise和x_point来生成y值 -> y_point
    # y = wx+b + noise
    y_point = np.zeros(size)
    y_point = x_point * weight + bias + noise
    x_point_2 = x_point.reshape(size,1)
    y_point_2 = y_point.reshape(size,1)
    # 把x_point和y_point拼起来 -> input_arr （size行两列）  
    input_arr = np.hstack((x_point_2, y_point_2))
    # 返回input_arr
    return input_arr


# 实参
real_weight = 1
real_bias = 3
real_size = 100
# 生成输入数据
input_point = random_point_nearby_line(real_weight, real_bias, size=real_size)

# 数据点(x,y) y0 = wx+b
# (y - y0) > 0 ? 1 : -1
# 利用np.sign给数据打标签，在直线上还是直线下，above = 1 /below = -1 -> label (size行1列)
# 提示: 提取input_point的y列和通过直线计算出来的y对比
label = np.sign(input_point[:, 1] - (input_point[:, 0] * real_weight + real_bias))

"""
step2
拆分训练集，测试集
"""
test_size = 15
# 利用train_test_split来划分数据集
# x_train, x_test, y_train, y_test = train_test_split(自己查接口，补全参数列表)

x_train, x_test, y_train, y_test = train_test_split(input_point, label, test_size = test_size, random_state=42)
train_size = real_size - test_size
"""
step3
绘制初始点，直线
"""
# 此处不用补全
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
for i in range(y_train.size):
    if y_train[i] == 1:
        ax.scatter(x_train[i][0], x_train[i][1], color='r')
    else:
        ax.scatter(x_train[i][0], x_train[i][1], color='b')
plt.show()

"""
step4
训练
"""
Weight = np.zeros((2, 1))
Bias = 0


def train(x_train, y_train, x_test, y_test, test_size, input_num,
          train_num, learning_rate=1):
    global Weight, Bias
    x = x_train
    y = y_train
    for rounds in range(train_num):
        # print("round= ",rounds)
        # print("weight =",Weight, "bias =",Bias)
        for i in range(input_num):
            x1, x2 = x[i]
            # 利用np.sign函数和三个参数来计算当前输入下的预测标签值 -> prediction
            prediction = np.sign(Weight[0] * x1 + Weight[1] * x2 + Bias)
            # 如果预测的标签不等于实际标签
            if y[i] != prediction:
                # 更新三个参数
                Weight[0] = Weight[0] + learning_rate * (y[i] - prediction) * x1
                Weight[1] = Weight[1] + learning_rate * (y[i] - prediction) * x2
                Bias = Bias + learning_rate * (y[i] - prediction)

        if rounds % 10 == 0:
            accuracy = compute_accuracy(x_test, y_test, test_size, Weight, Bias)
            print("round: %d, accuracy = %f" % (rounds, accuracy))

# 以下不用补全
def compute_accuracy(x_test, y_test, test_size, weight, bias):
    x1, x2 = (np.reshape(x_test[:, 0], (test_size, 1)),
              np.reshape(x_test[:, 1], (test_size, 1)))
    prediction = np.sign(x1 * weight[0] + x2 * weight[1] + bias)
    count = 0
    for i in range(prediction.size):
        if prediction[i] * y_test[i] > 0:
            count += 1
    return count / test_size


train(x_train, y_train, x_test, y_test, test_size, 85, train_num=100, learning_rate=1)
