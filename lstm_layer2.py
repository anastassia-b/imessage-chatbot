import tensorflow as tf
from config import *

weights2 = tf.Variable(tf.truncated_normal(
    [(NUM_STATE1_UNITS + NUM_STATE2_UNITS), NUM_STATE2_UNITS],
    stddev=np.sqrt(2.0 / (NUM_STATE1_UNITS + NUM_STATE2_UNITS + NUM_STATE2_UNITS))))
biases2 = tf.Variable(tf.zeros(NUM_STATE2_UNITS))

def apply(prev_state2, new_state1):
    input2 = tf.concat([prev_state2, new_state1], axis=1)
    new_state2 = tf.matmul(input2, weights2) + biases2
    new_state2 = tf.nn.relu(new_state2, name="new_state2")
    return new_state2
