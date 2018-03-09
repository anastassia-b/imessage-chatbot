import React from 'react';

class Chat extends React.Component {
  constructor(props) {
    super(props);
    this.getMessage = this.getMessage.bind(this);
    this.messageList = this.messageList.bind(this);
    this.state = { 'messages': [] };
  }

  async getMessage() {
    const response = await fetch('https://ec2-52-42-96-48.us-west-2.compute.amazonaws.com/message');
    const message = await response.text();
    await this.setState((prevState, props) => {
      prevState['messages'].push(message);
      return { 'messages': prevState['messages']}
    });
  }

  messageList() {
    return this.state.messages.map(message => (
      <li>{message}</li>
    ))
  }

  render() {
    return (
      <div className="Chat">
        <h2>Chat Log goes here</h2>
        <button onClick={this.getMessage}>Click to get a message</button>
        <ul>
          {this.messageList()}
        </ul>
      </div>
  );
  }
}

export default Chat;
