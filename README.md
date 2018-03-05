# imessage-rnn

In-progress project: Building a neural network to learn an individual's style of speaking, and respond in their manner.

### Technologies

* Training messages obtained with **SQL**
* Recurrent Neural Network (RNN) built with **TensorFlow**
* **Flask** app responds with generated messages to a **Twilio SMS** webhook
* **AWS EC2**: Trained RNN on p2.xlarge instance, message generator deployed through t2.micro instance

### Implementation


#### 1. Data Extraction

Data was extracted from the iMessage sqlite3 database, located in `/Library/Messages/chat.db`.

Getting all messages from yourself:
```sql
SELECT text FROM message WHERE is_from_me = 1;
```

Getting all messages from another person:
```sql
-- get their handle_id
SELECT * FROM handle WHERE id="(their_phone_number)";
-- use it to extract their messages
SELECT text FROM message WHERE handle_id = "(handle_id)" AND is_from_me = 0;
```

Save the ascii messages to a .txt file and format it (ie; deal with emojis).

#### 2. Data Processing

With `dataset.py`, process the text data with parameters from `config.py` into _batches_. The input shape for the recurrent neural network is: (None, 32, 62, 256).

### Next Steps

- [x] In progress: Build web app version with **React**
- [x] In progress: Increase training data
- [ ] Improve RNN performance with LSTM cells
- [ ] Set up automated testing / continuous integration
- [ ] Natural Language Processing (NLP)
