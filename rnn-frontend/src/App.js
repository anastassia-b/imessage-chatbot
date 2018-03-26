import React, { Component } from 'react';
import './stylesheets/app.css';
import Chat from './components/Chat.js';

class App extends Component {
  render() {
    return (
      <div className="app">
        <header className="app-header">
        </header>
        <Chat />
      </div>
    );
  }
}

export default App;
