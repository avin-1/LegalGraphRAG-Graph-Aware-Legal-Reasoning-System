import React from 'react';
import { LayoutDashboard, FileText, Database, Settings, Menu } from 'lucide-react';

const Sidebar = ({ activeTab, setActiveTab }) => {
  const menuItems = [
    { id: 'research', icon: LayoutDashboard, label: 'Research' },
    { id: 'files', icon: Database, label: 'Knowledge Base' },
    // { id: 'settings', icon: Settings, label: 'Settings' },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="logo-icon">
          <div className="logo-inner" />
        </div>
        <span className="logo-text">DeepResearch</span>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <button
            key={item.id}
            onClick={() => setActiveTab(item.id)}
            className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
          >
            <item.icon size={20} />
            <span className="nav-label">{item.label}</span>
            {activeTab === item.id && <div className="active-indicator" />}
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        <button className="nav-item">
          <Settings size={20} />
          <span className="nav-label">Settings</span>
        </button>
      </div>

      <style>{`
        .sidebar {
          width: 260px;
          height: 100vh;
          background: var(--bg-sidebar);
          border-right: 1px solid var(--border-subtle);
          display: flex;
          flex-direction: column;
          padding: 24px 16px;
        }

        .sidebar-header {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 40px;
          padding: 0 12px;
        }

        .logo-icon {
          width: 32px;
          height: 32px;
          background: var(--accent-blue);
          border-radius: 8px;
          display: flex;
          align-items: center;
          justify-content: center;
          box-shadow: 0 0 15px var(--primary-glow);
        }
        
        .logo-inner {
            width: 12px; 
            height: 12px; 
            background: white; 
            border-radius: 2px;
            opacity: 0.9;
        }

        .logo-text {
          font-weight: 700;
          font-size: 18px;
          color: var(--text-primary);
          letter-spacing: -0.02em;
        }

        .sidebar-nav {
          display: flex;
          flex-direction: column;
          gap: 4px;
          flex: 1;
        }

        .nav-item {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 12px;
          background: transparent;
          border: none;
          color: var(--text-secondary);
          border-radius: var(--radius-sm);
          font-family: inherit;
          font-size: 14px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s;
          position: relative;
          text-align: left;
          width: 100%;
        }

        .nav-item:hover {
          color: var(--text-primary);
          background: rgba(255, 255, 255, 0.03);
        }

        .nav-item.active {
          color: var(--accent-blue);
          background: rgba(59, 130, 246, 0.1);
        }

        .active-indicator {
          position: absolute;
          right: 0;
          top: 50%;
          transform: translateY(-50%);
          width: 3px;
          height: 20px;
          background: var(--accent-blue);
          border-radius: 4px 0 0 4px;
        }
        
        .sidebar-footer {
            border-top: 1px solid var(--border-subtle);
            padding-top: 16px;
        }
      `}</style>
    </aside>
  );
};

export default Sidebar;
