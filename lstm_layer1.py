import tensorflow as tf
from config import *

weights1 = tf.Variable(tf.truncated_normal(
    [(NUM_CHARS + NUM_STATE1_UNITS), NUM_STATE1_UNITS],
    stddev=np.sqrt(2.0 / (NUM_CHARS + NUM_STATE1_UNITS + NUM_STATE1_UNITS))))
biases1 = tf.Variable(tf.zeros(NUM_STATE1_UNITS))

def apply(prev_state1, prev_char):
    input1 = tf.concat([prev_state1, prev_char], axis=1) #32 * (256 + 128 = 384)
    new_state1 = tf.matmul(input1, weights1) + biases1
    new_state1 = tf.nn.relu(new_state1, name="new_state1")
    return new_state1
