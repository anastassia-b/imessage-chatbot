from model import build_graph
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
saver.restore(session, "./checkpoints/model-9")

text = ""
initial_state1 = np.zeros([1, NUM_STATE1_UNITS])
initial_state2 = np.zeros([1, NUM_STATE2_UNITS])
initial_char = np.zeros([1, NUM_CHARS])

def not_generate_char(prev_char):
    global initial_state1, initial_state2
    #probably feed in as variables later. Refactor!

    result = session.run({
                "final_state1": graph["final_state1"],
                "final_state2": graph["final_state2"]
                },
                feed_dict={
                    graph["initial_state1"]: initial_state1,
                    graph["initial_state2"]: initial_state2,
                    graph["initial_char"]: prev_char})

    initial_state1 = result["final_state1"]
    initial_state2 = result["final_state2"]


if os.path.isfile('./results/mixed_state1.npy'):
    print("Loading mixed state...")
    #load state from mixed files.
    initial_state1 = np.load('./results/mixed_state1.npy')
    initial_state2 = np.load('./results/mixed_state2.npy')
else:
    print("Generating mixed state...")
    for char in chats_int_text:
        char = np.expand_dims(char, axis=0)
        not_generate_char(char)

        np.save('./results/mixed_state1.npy', initial_state1)
        np.save('./results/mixed_state2.npy', initial_state2)


#now the initial states have been mixed! ready to generate!

def generate_char():
    global initial_state1, initial_state2, initial_char, text

    result = session.run({
                "final_state1": graph["final_state1"],
                "final_state2": graph["final_state2"],
                "final_probabilities": graph["final_probabilities"]
                },
                feed_dict={
                    graph["initial_state1"]: initial_state1,
                    graph["initial_state2"]: initial_state2,
                    graph["initial_char"]: initial_char})

    initial_state1 = result["final_state1"]
    initial_state2 = result["final_state2"]
    # selected_char = chr(np.argmax(result["final_probabilities"]))
    selected_char = chr(np.random.choice(NUM_CHARS, p=(result["final_probabilities"])[0, :]))
    initial_char = np.zeros([1, NUM_CHARS])
    initial_char[0, ord(selected_char)] = 1
    text += selected_char

print("Generating characters...")

for i in range(1024*4):
    generate_char()

dt = datetime.datetime.now()
dt_s = dt.strftime('%Y%m%d-%H:%M:%S')

with open(f"./results/generated_text_2layers_{dt_s}.txt", "w") as generated_file:
    generated_file.write(text)

print(text)
