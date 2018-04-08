import React, { Component } from 'react';
import './stylesheets/app.css';
import Chat from './components/Chat.js';

class App extends Component {
  render() {
    return (
      <div className="app">
        <header className="app-side">
        </header>
        <main className="app-main">
          <Chat />
        </main>
      </div>
    );
  }
}

export default App;
