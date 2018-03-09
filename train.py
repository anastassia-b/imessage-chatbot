from model import build_graph
import numpy as np
import tensorflow as tf
from config import *
from dataset import batches

session = tf.InteractiveSession()

graph = build_graph(BATCH_STRING_LENGTH)

init = tf.global_variables_initializer() # returns operation
session.run(init)

# run through text multiple times, and run through batches itself.

def run_batch(initial_state1, initial_state2, initial_char, text):
    result = session.run({
                #will evaluate the operations or the values of the tensors
                "_": graph["train_step"],
                "total_ce": graph["total_ce"],
                "total_accuracy": graph["total_accuracy"],
                "final_state1": graph["final_state1"],
                "final_state2": graph["final_state2"],
                },
                feed_dict={
                    #key is the tensor, value is the numbers to set the tensor to
                    graph["initial_state1"]: initial_state1,
                    graph["initial_state2"]: initial_state2,
                    graph["initial_char"]: initial_char,
                    graph["text"]: text})
    # now we get out the numpy arrays for the tensors in result
    return result

def run_epoch(epoch_idx):
    initial_state1 = np.zeros([NUM_SUBTEXTS, NUM_STATE1_UNITS])
    initial_state2 = np.zeros([NUM_SUBTEXTS, NUM_STATE2_UNITS])
    initial_char = np.zeros([NUM_SUBTEXTS, NUM_CHARS])

    for (batch_idx, batch) in enumerate(batches):
        result = run_batch(initial_state1, initial_state2, initial_char, batch)
        initial_state1 = result["final_state1"]
        initial_state2 = result["final_state2"]
        initial_char = batch[:, -1, :]
        print(f'loss: {result["total_ce"]}')
        print(f'accuracy: {result["total_accuracy"]}')
        print(f'batch: {batch_idx}, epoch: {epoch_idx}')

saver = tf.train.Saver()

for i in range(100):
    run_epoch(i)
    #save the model
    saver.save(session, "./checkpoints/model", global_step=i)
