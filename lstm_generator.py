from lstm_model import build_graph
import numpy as np
import tensorflow as tf
from config import *
from dataset import chats_int_text
import datetime
import os.path

session = tf.InteractiveSession()
#need to build the graph before you restore the variables so they have a home

graph = build_graph(1)

# Lets restore the model
saver = tf.train.Saver()
saver.restore(session, "./lstm_checkpoints/model-46")

initial_state1 = np.zeros([1, NUM_STATE1_UNITS])
initial_output1 = np.zeros([1, NUM_STATE1_UNITS])
initial_state2 = np.zeros([1, NUM_STATE2_UNITS])
initial_output2 = np.zeros([1, NUM_STATE2_UNITS])

def not_generate_char(prev_char):
    global initial_state1, initial_output1, initial_state2, initial_output2
    #probably feed in as variables later. Refactor!

    result = session.run({
                "final_state1": graph["final_state1"],
                "final_output1": graph["final_output1"],
                "final_state2": graph["final_state2"],
                "final_output2": graph["final_output2"],
                },
                feed_dict={
                    graph["initial_state1"]: initial_state1,
                    graph["initial_output1"]: initial_output1,
                    graph["initial_state2"]: initial_state2,
                    graph["initial_output2"]: initial_output2,
                    graph["initial_char"]: prev_char
                    })

    initial_state1 = result["final_state1"]
    initial_output1 = result["final_output1"]
    initial_state2 = result["final_state2"]
    initial_output2 = result["final_output2"]


if os.path.isfile('./results/lstm_mixed_state1.npy'):
    print("Loading mixed state...")
    #load state from mixed files.
    initial_state1 = np.load('./results/lstm_mixed_state1.npy')
    initial_output1 = np.load('./results/lstm_mixed_output1.npy')
    initial_state2 = np.load('./results/lstm_mixed_state2.npy')
    initial_output2 = np.load('./results/lstm_mixed_output2.npy')
else:
    print("Generating mixed state...")
    for char in chats_int_text:
        char = np.expand_dims(char, axis=0)
        not_generate_char(char)

    np.save('./results/lstm_mixed_state1.npy', initial_state1)
    np.save('./results/lstm_mixed_output1.npy', initial_output1)
    np.save('./results/lstm_mixed_state2.npy', initial_state2)
    np.save('./results/lstm_mixed_output2.npy', initial_output2)


#now the initial states have been mixed! ready to generate!

def select_probabilities(probs):
    #get the max prob indices
    prob_indices = np.argsort(probs)[-PROB_CHARS:]
    new_probs = np.zeros(NUM_CHARS)
    # for idx in prob_indices:
    #     new_probs[idx] = probs[idx]
    new_probs[prob_indices] = probs[prob_indices]
    #this will give selected indices as array! this is awesome.
    new_probs = new_probs / np.sum(new_probs)
    return new_probs

def generate_char(initial_char):
    global initial_state1, initial_output1, initial_state2, initial_output2

    result = session.run({
                "final_state1": graph["final_state1"],
                "final_output1": graph["final_output1"],
                "final_state2": graph["final_state2"],
                "final_output2": graph["final_output2"],
                "final_probabilities": graph["final_probabilities"]
                },
                feed_dict={
                    graph["initial_state1"]: initial_state1,
                    graph["initial_output1"]: initial_output1,
                    graph["initial_state2"]: initial_state2,
                    graph["initial_output2"]: initial_output2,
                    graph["initial_char"]: initial_char,
                    })

    initial_state1 = result["final_state1"]
    initial_output1 = result["final_output1"]
    initial_state2 = result["final_state2"]
    initial_output2 = result["final_output2"]
    # selected_char = chr(np.argmax(result["final_probabilities"]))

    # selected_char = chr(np.random.choice(NUM_CHARS, p=(result["final_probabilities"])[0, :]))
    selected_probs = select_probabilities(result["final_probabilities"][0, :])
    selected_char = chr(np.random.choice(NUM_CHARS, p=selected_probs))
    return selected_char

def generate_message(length):
    prev_char = np.zeros([1, NUM_CHARS])
    message = ""
    for i in range(length):
        message += generate_char(prev_char)
        prev_char = np.zeros([1, NUM_CHARS])
        prev_char[0, ord(message[-1])] = 1
    return message


def run():
    print("Generating message...")
    text = generate_message(1000)

    dt = datetime.datetime.now()
    dt_s = dt.strftime('%Y%m%d-%H:%M:%S')

    with open(f"./results/lstm_generated_texts_{dt_s}.txt", "w") as generated_file:
        generated_file.write(text)

        print(text)

if __name__ == '__main__':
    run()
