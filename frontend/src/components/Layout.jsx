import React from 'react';
import Sidebar from './Sidebar';

const Layout = ({ children, activeTab, setActiveTab }) => {
    return (
        <div className="app-layout">
            <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
            <main className="main-content">
                {children}
            </main>

            <style>{`
        .app-layout {
          display: flex;
          width: 100vw;
          height: 100vh;
          overflow: hidden;
          background: var(--bg-app);
        }

        .main-content {
          flex: 1;
          height: 100%;
          overflow-y: auto;
          position: relative;
        }
      `}</style>
        </div>
    );
};

export default Layout;
