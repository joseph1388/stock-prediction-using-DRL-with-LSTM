import tensorflow as tf

add_arg_scope = tf.contrib.framework.add_arg_scope
arg_scope = tf.contrib.framework.arg_scope


@add_arg_scope
def func1(*args, **kwargs):
    return (args, kwargs)

with arg_scope((func1,), a=1, b=None, c=[1]):
    args, kwargs = func1(0)
    print args
    print kwargs