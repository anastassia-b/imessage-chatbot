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

def run_batch(initial_state1, initial_char, text):
    result = session.run({
                #will evaluate the operations or the values of the tensors
                "_": graph["train_step"],
                "total_ce": graph["total_ce"],
                "final_state": graph["final_state"]
                },
                feed_dict={
                    #key is the tensor, value is the numbers to set the tensor to
                    graph["initial_state1"]: initial_state1,
                    graph["initial_char"]: initial_char,
                    graph["text"]: text})
    # now we get out the numpy arrays for the tensors in result
    return result

def run_epoch():
    initial_state1 = np.zeros([NUM_SUBTEXTS, NUM_STATE1_UNITS])
    initial_char = np.zeros([NUM_SUBTEXTS, NUM_CHARS])

    for batch in batches:
        result = run_batch(initial_state1, initial_char, batch)
        initial_state1 = result["final_state"]
        initial_char = batch[:, -1, :]
        print(result["total_ce"])


for i in range(100):
    run_epoch()
