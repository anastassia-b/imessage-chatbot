import React from 'react';
import ReactDOM from 'react-dom';

class Chat extends React.Component {
  constructor(props) {
    super(props);
    this.getMessage = this.getMessage.bind(this);
    this.messageList = this.messageList.bind(this);
    this.scrollDown = this.scrollDown.bind(this);
    this.submitMessage = this.submitMessage.bind(this);
    this.handleChange = this.handleChange.bind(this);

    this.state = { 'messages': [], currentMessage: "" };
  }

  async getMessage() {
    const response = await fetch('http://ec2-52-42-96-48.us-west-2.compute.amazonaws.com/message');
    const message = await response.text();
    const formatMessage = ["ai", message]
    await this.setState((prevState, props) => {
      prevState['messages'].push(formatMessage);
      return { 'messages': prevState['messages']}
    });
  }

  messageList() {
    return this.state.messages.map(message => (
      <li className={message[0]}>{message[1]}</li>
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

  submitMessage(e) {
    e.preventDefault();
    const yourMessage = "You: " + this.state.currentMessage;
    const formatMessage = ["you", yourMessage];
    this.setState((prevState, props) => {
      prevState['messages'].push(formatMessage);
      return { 'messages': prevState['messages'], currentMessage: "" }
    });
    this.getMessage();
  }

  handleChange(e) {
    this.setState({ currentMessage: e.target.value });
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
            <form onSubmit={(e) => this.submitMessage(e)}>
              <label>
                <input
                  type="text"
                  value={this.state.currentMessage}
                  onChange={this.handleChange}>
                </input>
              </label>
            </form>
            <button onClick={this.getMessage}>Chat</button>
          </div>
        </div>
      </main>
  );
  }
}

export default Chat;
