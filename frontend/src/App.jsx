import React, { useState } from 'react';
import Layout from './components/Layout';
import ResearchModule from './modules/Research/ResearchModule';
import KnowledgeBaseModule from './modules/KnowledgeBase/KnowledgeBaseModule';

function App() {
  const [activeTab, setActiveTab] = useState('research');

  const renderContent = () => {
    switch (activeTab) {
      case 'research':
        return <ResearchModule />;
      case 'files':
        return <KnowledgeBaseModule />;
      case 'audit':
        return (
          <div className="flex-center" style={{ height: '100%', color: 'var(--text-secondary)' }}>
            Audit logs are integrated into the Research view.
          </div>
        );
      default:
        return <ResearchModule />;
    }
  };

  return (
    <Layout activeTab={activeTab} setActiveTab={setActiveTab}>
      {renderContent()}
    </Layout>
  );
}

export default App;
