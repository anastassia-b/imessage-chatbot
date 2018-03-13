import React, { Component } from 'react';
import './App.css';
import Chat from './components/Chat.js';

class App extends Component {
  render() {
    return (
      <div className="app">
        <header className="app-header">
          <h1 className="app-title">Welcome</h1>
        </header>
        <Chat />
      </div>
    );
  }
}

export default App;
