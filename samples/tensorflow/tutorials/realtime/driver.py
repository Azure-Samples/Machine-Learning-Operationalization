import json
import tensorflow as tf
import numpy

def init():

    global sess
    sess = tf.Session()

    new_saver = tf.train.import_meta_graph('mnist_model.meta')
    new_saver.restore(sess, './mnist_model')

    global prediction
    prediction = tf.get_collection('prediction')[0]
    global x
    x = tf.get_collection('x')[0]


def run(input_string):

    try:
        input_list = json.loads(input_string)
    except ValueError:
        return "Bad input: Expecting a json encoded list of lists."

    input_array = numpy.array(input_list)
    if (input_array.shape != (1,784)
        or (input_array.dtype != numpy.dtype('float32') and input_array.dtype != numpy.dtype('float64'))):
        return "Bad input: Expecting a json encoded list of lists with float values."

    return sess.run(prediction, feed_dict={x: input_array})[0]