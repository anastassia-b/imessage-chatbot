import React, { Component } from 'react';
import './App.css';
import Chat from './components/Chat.js';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Welcome</h1>
        </header>
        <main>
          <Chat />
        </main>
      </div>
    );
  }
}

export default App;
