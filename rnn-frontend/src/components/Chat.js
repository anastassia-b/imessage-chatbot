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
    this.addMessage = this.addMessage.bind(this);
    this.loading = this.loading.bind(this);

    this.state = { 'messages': [], currentMessage: "", loading: false };
  }

  handleChange(e) {
    this.setState({ currentMessage: e.target.value });
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
    this.addMessage(formatMessage);
    this.getMessage();
  }

  async getMessage() {
    // const response = await fetch('http://ec2-52-42-96-48.us-west-2.compute.amazonaws.com/message');
    this.setState({ loading: true })
    const response = await fetch('http://127.0.0.1:5000/message');
    const message = await response.text();
    const messageList = message.split("\n").slice(1, -1);
    let formatMessage;

    messageList.forEach((msg, idx) => {
      if (msg === "") { return; }
      formatMessage = ["ai", msg];
      this.addMessage(formatMessage);
    })
  }

  addMessage(formatMessage) {
    this.setState((prevState, props) => {
      prevState['messages'].push(formatMessage);
      return { 'messages': prevState['messages'], currentMessage: "", loading: false }
    });
  }

  loading() {
    if (this.state.loading) {
      return <li id="ai-loading">. . .</li>
    }
  }

  render() {
    return (
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
          <div className="loading">
            {this.loading()}
          </div>
          <div className="input-area">
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
      </div>
    );
  }
}

export default Chat;
