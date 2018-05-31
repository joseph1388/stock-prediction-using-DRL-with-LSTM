import tensorflow as tf
a = tf.Variable(1, name='a')
g = tf.get_default_graph()
print g.get_operations()