with open("./reference/all_the_chats.txt", "r") as chat_file:
    chat_text = chat_file.read()
    # utf8_chat_text = chat_text.decode("utf-8")
    ascii_bytes = chat_text.encode("ascii","ignore")
    ascii_text = ascii_bytes.decode()

with open("./reference/ascii_chats.txt", "w") as ascii_file:
    ascii_file.write(ascii_text)
