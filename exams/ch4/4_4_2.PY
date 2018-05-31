import tensorflow as tf
# 5个卷积部分的输出通道数
filter_depth = [64, 128, 256, 512] 
VGG16_NUM_HIDDEN_1, VGG16_NUM_HIDDEN_2 = 4096, 1000

def submodel(x, iters, k_width, in_depth, out_depth):
  for i in range(iters):
    cur_in_depth = in_depth if i == 0 else out_depth
    w = tf.Variable(tf.truncated_normal([k_width, k_width, cur_in_depth, out_depth], stddev=0.01))
    b = tf.Variable(tf.zeros([out_depth]))
    x = tf.nn.relu(tf.nn.conv2d(x, w, [1,1,1,1], padding='SAME') + b)
    #filter就是卷积核（这里要求用Tensor来表示卷积核，并且Tensor（一个4维的Tensor，要求类型与input相同）
    #shape为[filter_height, filter_width, in_channels, out_channels]具体含义[卷积核高度，卷积核宽度，图像通道数，卷积核个数]
    x = tf.nn.max_pool(x, [1, 2, 2, 1], [1, 2, 2, 1], padding='SAME')
  return x

def fc(x, in_size, out_size):
  w = tf.Variable(tf.truncated_normal([in_size, out_size]))
  b = tf.Variable(tf.constant(0.0, shape=[out_size]))
  out = tf.matmul(x, w) + b
  return tf.nn.relu(out)
  
def vgg16(x, filter_depth, hidden1, hidden2, img_height, img_width, img_depth, num_labels):
  out = x
  k_w = 3
  # 1st part
  k_d1 = filter_depth[0]
  out = submodel(out, 2, k_w, img_depth, k_d1)
  # 2nd part
  k_d2 = filter_depth[1]
  out = submodel(out, 2, k_w, k_d1, k_d2)
  # 3rd part
  k_d3 = filter_depth[2]
  out = submodel(out, 3, k_w, k_d2, k_d3)
  # 4th part
  k_d4 = filter_depth[3]
  out = submodel(out, 3, k_w, k_d3, k_d4)
  # 5th part
  out = submodel(out, 3, k_w, k_d4, k_d4)
  
  element_num = ((img_height // (2 ** 5)) * (img_width // (2 ** 5)) * k_d4)
  out = tf.reshape(out, [-1, element_num])
  
  # fully connected part
  out = fc(out, element_num, VGG16_NUM_HIDDEN_1)
  out = tf.nn.dropout(out, 0.5)
  out = fc(out, VGG16_NUM_HIDDEN_1, VGG16_NUM_HIDDEN_2)
  out = tf.nn.dropout(out, 0.5)
  
  return fc(out, VGG16_NUM_HIDDEN_2, num_labels)