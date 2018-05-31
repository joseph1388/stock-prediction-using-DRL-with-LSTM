import tensorflow as tf
# 网络参数
n_hidden_1 = 256 # 第1层网络神经元数量
n_hidden_2 = 256 # 第2层网络神经元数量
n_input = 784 # 数据输入维度
n_classes = 10 # 数据输出维度

# placeholder
X = tf.placeholder("float", [None, n_input])
Y = tf.placeholder("float", [None, n_classes])

# 模型中的参数定义
weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}

def multilayer_perceptron(x):
    # 第一层全连接层和非线性层，下同
    layer_1 = tf.nn.relu(tf.add(tf.matmul(x, weights['h1']), biases['b1']))
    layer_2 = tf.nn.relu(tf.add(tf.matmul(layer_1, weights['h2']), biases['b2']))
    out = tf.matmul(layer_2, weights['out']) + biases['out']
    return out