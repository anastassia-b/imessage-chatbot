import numpy as np
import tensorflow as tf
from config import *
import pdb
import lstm_layer1
import lstm_layer2

def build_graph(batch_string_length):
    #None for batchsize
    text = tf.placeholder(tf.float32, shape=[
    None, BATCH_STRING_LENGTH, NUM_CHARS], name="text")
    initial_char = tf.placeholder(tf.float32, shape=[
    None, NUM_CHARS], name="initial_char")

    # LAYER 1
    initial_state1 = tf.placeholder(tf.float32, shape=[
        None, NUM_STATE1_UNITS], name="initial_state1")

    initial_output1 = tf.placeholder(tf.float32, shape=[
        None, NUM_STATE1_UNITS], name="initial_output1")

    # LAYER 2
    initial_state2 = tf.placeholder(tf.float32, shape=[
        None, NUM_STATE2_UNITS], name="initial_state2s")

    initial_output2 = tf.placeholder(tf.float32, shape=[
        None, NUM_STATE1_UNITS], name="initial_output2")

    # For emission probs.
    emission_weights = tf.Variable(tf.truncated_normal(
        [NUM_STATE2_UNITS, NUM_CHARS],
        stddev=np.sqrt(2.0 / (NUM_STATE2_UNITS + NUM_CHARS))))
    emission_biases = tf.Variable(tf.zeros(NUM_CHARS))

    prev_state1 = initial_state1 # 32 * 256
    prev_output1 = initial_output1
    prev_state2 = initial_state2 # 32 * 256
    prev_output2 = initial_output2
    prev_char = initial_char # 32 * 128

    total_accuracy = 0
    total_ce = 0 #loss

    for i in range(batch_string_length):
        next_state1, next_output1 = lstm_layer1.apply(prev_state1, prev_output1, prev_char)
        next_state2, next_output2 = lstm_layer2.apply(prev_state2, prev_output2, next_output1)

        logits = tf.matmul(next_output2, emission_weights) + emission_biases
        probabilities = tf.nn.softmax(logits, name="probabilities")

        prev_state1 = next_state1
        prev_output1 = next_output1
        prev_state2 = next_state2
        prev_output2 = next_output2

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
    final_output1 = prev_output1
    final_state2 = prev_state2
    final_output2 = prev_output2
    # build graph will return hashmap. keys will be names and values are tensor objects.
    return {
        "initial_state1": initial_state1,
        "initial_output1": initial_output1,
        "initial_state2": initial_state2,
        "initial_output2": initial_output2,
        "initial_char": initial_char,
        "text": text,
        "train_step": train_step,
        "final_state1": final_state1,
        "final_output1": final_output1,
        "final_state2": final_state2,
        "final_output2": final_output2,
        "total_ce": total_ce,
        "total_accuracy": total_accuracy,
        "final_probabilities": final_probabilities
    }


# for each batch, run training step and evaluate the final state,
# to feed it in next time as the initial state placeholder.
