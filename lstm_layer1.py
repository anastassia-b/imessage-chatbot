import tensorflow as tf
from config import *
import numpy as np

# 1. Forget Layer
forget_weights = tf.Variable(tf.truncated_normal(
    [(NUM_CHARS + NUM_STATE1_UNITS), NUM_STATE1_UNITS],
    stddev=np.sqrt(2.0 / (NUM_CHARS + NUM_STATE1_UNITS + NUM_STATE1_UNITS))))
forget_biases = tf.Variable(tf.ones(NUM_STATE1_UNITS))
# we want non-zero forget biases such that information can continue down the LSTM.
# this way there is a positive value to the layer.

# 2. Write
write_weights = tf.Variable(tf.truncated_normal(
    [(NUM_CHARS + NUM_STATE1_UNITS), NUM_STATE1_UNITS],
    stddev=np.sqrt(2.0 / (NUM_CHARS + NUM_STATE1_UNITS + NUM_STATE1_UNITS))))
write_biases = tf.Variable(tf.zeros(NUM_STATE1_UNITS))

# 3. Update
update_weights = tf.Variable(tf.truncated_normal(
    [(NUM_CHARS + NUM_STATE1_UNITS), NUM_STATE1_UNITS],
    stddev=np.sqrt(2.0 / (NUM_CHARS + NUM_STATE1_UNITS + NUM_STATE1_UNITS))))
update_biases = tf.Variable(tf.zeros(NUM_STATE1_UNITS))

# 4. Read
read_weights = tf.Variable(tf.truncated_normal(
    [(NUM_CHARS + NUM_STATE1_UNITS), NUM_STATE1_UNITS],
    stddev=np.sqrt(2.0 / (NUM_CHARS + NUM_STATE1_UNITS + NUM_STATE1_UNITS))))
read_biases = tf.Variable(tf.zeros(NUM_STATE1_UNITS))


def apply(prev_state1, prev_output1, prev_char):
    concat_input = tf.concat([prev_output1, prev_char], axis=1)

    forget_multipliers = tf.matmul(concat_input, forget_weights) + forget_biases
    forget_multipliers = tf.nn.sigmoid(forget_multipliers, name="forget_multipliers")

    write_multipliers = tf.matmul(concat_input, write_weights) + write_biases
    write_multipliers = tf.nn.sigmoid(write_multipliers, name="write_multipliers")

    update_values = tf.matmul(concat_input, update_weights) + update_biases
    update_values = tf.nn.tanh(update_values, name="update_values")

    read_multipliers = tf.matmul(concat_input, read_weights) + read_biases
    read_multipliers = tf.nn.sigmoid(read_multipliers, name="read_multipliers")

    # Combine with previous state
    next_state1 = prev_state1 * forget_multipliers
    next_state1 = next_state1 + (write_multipliers * update_values)
    next_output1 = tf.nn.tanh(next_state1) * read_multipliers

    return next_state1, next_output1
