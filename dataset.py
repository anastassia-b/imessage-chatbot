from config import *
import numpy as np

def to_categorical(i, length):
    one_hot_encoding = np.zeros(length)
    one_hot_encoding[i] = 1
    return one_hot_encoding

with open("./reference/ascii_chats.txt", "r") as chats_text_file:
    chats_text = chats_text_file.read()

    # instead of map, list comprehension
    #instead of just ord, we want a one-hot array.
    chats_int_text = [
        to_categorical(ord(char), NUM_CHARS)
        for char in chats_text
    ]

    length = len(chats_int_text) // NUM_SUBTEXTS # we want an integer instead of a float
    sub_texts = []
    for i in range(NUM_SUBTEXTS):
        sub_texts.append(chats_int_text[(length*i):(length*(i+1))])

    num_batches = length // BATCH_STRING_LENGTH
    batches = []

    for i in range(num_batches):
        batch = []

        for j in range(NUM_SUBTEXTS):
            batch.append(sub_texts[j][(BATCH_STRING_LENGTH*i):(BATCH_STRING_LENGTH*(i+1))])

        batches.append(batch)

    batches = np.array(batches)
    print(batches.shape)

# (148, 32, 64, 256)
