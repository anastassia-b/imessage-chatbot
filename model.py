import numpy as np
import tensorflow as tf
from config import *
import pdb

# softmax ensures that numbers get distributed 0-1 and sum to 1.
# old state + prev char -> new state
# new state generates new char probabilities
# it needs a previous character. 'teacher forcing'. so we'll tell it 'A' when we train.
# when we generate, it will sample.
# for internal states, we'll use relu. (new state)
# for probs (softmax)
# to evaluate prob distribution, use cross entropy.
# CE(probs1, char1 ('A')) + CE(probs2, char2 ('_')) + CE(probs3, char3 ('i'))...
# minimize this^ since this is our loss.

# when we generate, it will be 1, but 32 when we train
def build_graph(batch_string_length):
    #None for batchsize
    text = tf.placeholder(tf.float32, shape=[
    None, BATCH_STRING_LENGTH, NUM_CHARS])
    initial_char = tf.placeholder(tf.float32, shape=[
    None, NUM_CHARS])

    # LAYER 1
    initial_state1 = tf.placeholder(tf.float32, shape=[
        None, NUM_STATE1_UNITS], name="initial_state1")

    #define variables
    # weights will be 384 * 256.
    # For calculating new state
    weights1 = tf.Variable(tf.truncated_normal(
        [(NUM_CHARS + NUM_STATE1_UNITS), NUM_STATE1_UNITS],
        stddev=np.sqrt(2.0 / (NUM_CHARS + NUM_STATE1_UNITS + NUM_STATE1_UNITS))))
    biases1 = tf.Variable(tf.zeros(NUM_STATE1_UNITS))

    # LAYER 2
    initial_state2 = tf.placeholder(tf.float32, shape=[
        None, NUM_STATE2_UNITS], name="initial_state2s")
    weights2 = tf.Variable(tf.truncated_normal(
        [(NUM_STATE1_UNITS + NUM_STATE2_UNITS), NUM_STATE2_UNITS],
        stddev=np.sqrt(2.0 / (NUM_STATE1_UNITS + NUM_STATE2_UNITS + NUM_STATE2_UNITS))))
    biases2 = tf.Variable(tf.zeros(NUM_STATE2_UNITS))

    # For emission probs.
    emission_weights = tf.Variable(tf.truncated_normal(
        [NUM_STATE2_UNITS, NUM_CHARS],
        stddev=np.sqrt(2.0 / (NUM_STATE2_UNITS + NUM_CHARS))))
    emission_biases = tf.Variable(tf.zeros(NUM_CHARS))

    prev_state1 = initial_state1 # 32 * 256
    prev_state2 = initial_state2 # 32 * 256
    prev_char = initial_char # 32 * 128

    total_accuracy = 0
    total_ce = 0 #loss

    for i in range(batch_string_length):
        #Concatenate prev state and prev char
        input1 = tf.concat([prev_state1, prev_char], axis=1) #32 * (256 + 128 = 384)
        new_state1 = tf.matmul(input1, weights1) + biases1
        new_state1 = tf.nn.relu(new_state1, name="new_state1")

        input2 = tf.concat([prev_state2, new_state1], axis=1)
        new_state2 = tf.matmul(input2, weights2) + biases2
        new_state2 = tf.nn.relu(new_state2, name="new_state2")

        # what goes into the softmax? a logit.
        logits = tf.matmul(new_state2, emission_weights) + emission_biases
        probabilities = tf.nn.softmax(logits, name="probabilities")

        prev_state1 = new_state1
        prev_state2 = new_state2

        prev_char = text[:, i, :] #(32, 128)

        cross_entropies = tf.nn.softmax_cross_entropy_with_logits(
            labels=prev_char, #correct answer
            logits=logits
        )

        #pick the highest logit, compare to real.
        #logits shape (32, 128)
        predicted_char = tf.argmax(logits, axis=1)
        actual_char = tf.argmax(prev_char, axis=1)

        char_matches = tf.equal(predicted_char, actual_char)
        # pdb.set_trace()
        char_matches = tf.cast(char_matches, dtype=tf.float32)

        total_accuracy += tf.reduce_mean(char_matches)
        #instead of reduce_sum, do mean, (per subtext)
        total_ce += tf.reduce_mean(cross_entropies)


    total_ce = total_ce / BATCH_STRING_LENGTH
    total_accuracy = total_accuracy / BATCH_STRING_LENGTH

    optimizer = tf.train.AdamOptimizer(
        learning_rate=LEARNING_RATE,
    )

    train_step = optimizer.minimize(total_ce)
    final_probabilities = probabilities
    final_state1 = prev_state1
    final_state2 = prev_state2
    # build graph will return hashmap. keys will be names and values are tensor objects.
    return {
        "initial_state1": initial_state1,
        "initial_state2": initial_state2,
        "initial_char": initial_char,
        "text": text,
        "train_step": train_step,
        "final_state1": final_state1,
        "final_state2": final_state2,
        "total_ce": total_ce,
        "total_accuracy": total_accuracy,
        "final_probabilities": final_probabilities
    }


# for each batch, run training step and evaluate the final state,
# to feed it in next time as the initial state placeholder.
