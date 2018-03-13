import React from 'react';
import ReactDOM from 'react-dom';

class Chat extends React.Component {
  constructor(props) {
    super(props);
    this.getMessage = this.getMessage.bind(this);
    this.messageList = this.messageList.bind(this);
    this.scrollDown = this.scrollDown.bind(this);

    this.state = { 'messages': [] };
  }

  async getMessage() {
    const response = await fetch('http://ec2-52-42-96-48.us-west-2.compute.amazonaws.com/message');
    const message = await response.text();
    await this.setState((prevState, props) => {
      prevState['messages'].push(message);
      return { 'messages': prevState['messages']}
    });
  }

  messageList() {
    return this.state.messages.map(message => (
      <li className="message-item">{message}</li>
    ))
  }

  scrollDown() {
    // https://stackoverflow.com/questions/37620694/how-to-scroll-to-bottom-in-react
    const messagesContainer = ReactDOM.findDOMNode(this.messagesContainer);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  componentDidUpdate() {
    this.scrollDown();
  }

  render() {
    return (
      <main className="app-main">
        <div className="app-container">
          <div className="chat-main">
            <h4>chatbot</h4>
            <div className="message-list-container" ref={(el) => {this.messagesContainer = el;}}>
              <ul id="message-list">
                {this.messageList()}
              </ul>
            </div>
          </div>
          <div className="chat-bottom">
            <label>
              <input type="text">

              </input>
            </label>
            <button onClick={this.getMessage}>Chat</button>
          </div>
        </div>
      </main>
  );
  }
}

export default Chat;
