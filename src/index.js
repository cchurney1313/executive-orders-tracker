import React from 'react';
import ReactDOM from 'react-dom';
import './index.css'; // Optional, if you have CSS
import App from './App'; // Ensure App.js exists in the same directory

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root') // Ensure your public/index.html has a <div id="root"></div>
);