import React, { Component } from 'react';
import './stylesheets/app.css';
import Chat from './components/Chat.js';
import Side from './components/Side.js';

class App extends Component {
  render() {
    return (
      <div className="app">
        <header className="app-side">
          <Side />
        </header>
        <main className="app-main">
          <Chat />
        </main>
      </div>
    );
  }
}

export default App;
