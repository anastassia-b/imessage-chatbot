# imessage-rnn

In-progress project: Building a neural network to learn an individual's style of speaking, and respond to texts accordingly!

### Technologies

* Training messages obtained with **SQL**
* Recurrent Neural Network (RNN) built with **TensorFlow**
* **Flask** app responds with generated messages
* **Twilio SMS** webhook
* Deployed through **AWS**.

### Implementation

Data was extracted from the iMessage sqlite3 database, located in `/Library/Messages/chat.db`. Saved ascii text to file.

Getting all messages from yourself:
```sql
SELECT text FROM message WHERE is_from_me = 1 LIMIT 100;
```

Getting all messages from another person:
```sql
-- gives their handle_id
SELECT * FROM handle WHERE id="(their_phone_number)";
-- use it to extract messages;
SELECT text FROM message WHERE handle_id = "(handle_id)" AND is_from_me = 0;
```

### Next Steps

* Increase training data
* Improve RNN performance with LSTM cells
* Automated Testing, Continuous Integration
* Build web app version as well
* Natural Language Processing (NLP)
