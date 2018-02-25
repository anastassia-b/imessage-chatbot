# imessage-rnn

1. SQL the chat.db
2. Format the messages
3. The rest

Improvements:
* Add a second layer
* Currently all of the initial states are zeroes. So we can give this model time to moved to a "mixed" state. Since generate takes in S1, S2, and prev_char, we can first go through the entire text, update S1 and S2. And instead of taking whatever character would be generated, we feed the actual previous character in.
* Take the probability distribution, take the top number of characters we wish to sample from. Set the rest of the probabilities to zero and divide by sum to scale up.

Twilio!


Notes:

Port 22 would be to ssh to login.

nc www.google.com 80
GET / HTTP/1.1
Host: www.google.com
