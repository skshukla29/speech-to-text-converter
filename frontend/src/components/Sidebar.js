import React from 'react';
import { useTheme } from '../context/ThemeContext';
import './Sidebar.css';

const Sidebar = ({ activeView, setActiveView }) => {
  const { theme, toggleTheme } = useTheme();

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>🎙️ STT</h2>
      </div>
      
      <nav className="sidebar-nav">
        <button
          className={`nav-item ${activeView === 'upload' ? 'active' : ''}`}
          onClick={() => setActiveView('upload')}
        >
          <span className="icon">📁</span>
          Upload Audio
        </button>
        
        <button
          className={`nav-item ${activeView === 'live' ? 'active' : ''}`}
          onClick={() => setActiveView('live')}
        >
          <span className="icon">🎤</span>
          Live Recording
        </button>
      </nav>
      
      <div className="sidebar-footer">
        <button className="theme-toggle" onClick={toggleTheme}>
          {theme === 'light' ? '🌙' : '☀️'}
          <span>{theme === 'light' ? 'Dark Mode' : 'Light Mode'}</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
