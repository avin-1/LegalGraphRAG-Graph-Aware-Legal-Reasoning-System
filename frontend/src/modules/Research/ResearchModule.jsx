import React, { useState, useEffect, useRef } from 'react';
import { Send, Loader2, PlayCircle, CheckCircle2, ChevronRight, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const ResearchModule = () => {
    const [query, setQuery] = useState('');
    const [status, setStatus] = useState('idle'); // idle, thinking, completed, error
    const [taskId, setTaskId] = useState(null);
    const [auditLogs, setAuditLogs] = useState([]);
    const [result, setResult] = useState(null);

    const bottomRef = useRef(null);
    const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!query.trim()) return;

        setStatus('thinking');
        setAuditLogs([]);
        setResult(null);

        const formData = new FormData();
        formData.append('queryText', query);

        try {
            const res = await fetch(`${API_URL}/uploadQuery`, {
                method: 'POST',
                body: formData,
            });
            const data = await res.json();
            if (data.task_id) {
                setTaskId(data.task_id);
            } else {
                setStatus('error');
            }
        } catch (err) {
            console.error(err);
            setStatus('error');
        }
    };

    // Polling logic
    useEffect(() => {
        if (!taskId || status === 'completed' || status === 'error') return;

        const pollInterval = setInterval(async () => {
            try {
                // Fetch Audit Logs
                const auditRes = await fetch(`${API_URL}/v1/research/audit/${taskId}`);
                if (auditRes.ok) {
                    const auditData = await auditRes.json();
                    // Assuming backend returns simple list of strings or dicts. 
                    // Adjust based on actual backend format.
                    if (auditData.audit_trail) {
                        setAuditLogs(auditData.audit_trail);
                    }
                }

                // Fetch Final Result
                const resultRes = await fetch(`${API_URL}/result/${taskId}`);
                if (resultRes.ok) {
                    const resultData = await resultRes.json();

                    if (resultData.status !== 'processing' && resultData.result) {
                        // Need to parse if it's a JSON string, but we fixed backend to send JSON object
                        // Just in case it's double serialized or something:
                        let finalRes = resultData.result;

                        // Extract the 'final_answer' from the state dict
                        if (typeof finalRes === 'object' && finalRes.final_answer) {
                            setResult(finalRes.final_answer);
                            setStatus('completed');
                            clearInterval(pollInterval);
                        }
                    }
                }
            } catch (err) {
                console.error("Polling error", err);
            }
        }, 2000);

        return () => clearInterval(pollInterval);
    }, [taskId, status]);

    // Auto-scroll to bottom of logs
    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [auditLogs, result]);

    return (
        <div className="research-container">
            <div className="research-content">

                {/* Welcome / Empty State */}
                {status === 'idle' && (
                    <div className="welcome-hero">
                        <div className="hero-icon">
                            <Sparkles size={48} className="text-accent" />
                        </div>
                        <h1>Deep Research Assistant</h1>
                        <p>Ask complex questions. I'll read your documents, plan a research strategy, and verify facts.</p>
                    </div>
                )}

                {/* Audit Trail */}
                {(status === 'thinking' || status === 'completed') && (
                    <div className="audit-trail">
                        <h3>Research Progress</h3>
                        <div className="logs-container">
                            {auditLogs.map((log, idx) => (
                                <motion.div
                                    initial={{ opacity: 0, x: -10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    key={idx}
                                    className="log-item"
                                >
                                    <div className="log-line"></div>
                                    <div className="log-icon-wrapper">
                                        {idx === auditLogs.length - 1 && status === 'thinking' ? (
                                            <Loader2 size={16} className="animate-spin text-accent" />
                                        ) : (
                                            <CheckCircle2 size={16} className="text-success" />
                                        )}
                                    </div>

                                    <span className="log-text">
                                        {typeof log === 'string' ? log : JSON.stringify(log)}
                                    </span>
                                </motion.div>
                            ))}
                            {status === 'thinking' && (
                                <div className="thinking-pulse">
                                    <span className="pulse-dot"></span>
                                    Thinking...
                                </div>
                            )}
                            <div ref={bottomRef} />
                        </div>
                    </div>
                )}

                {/* Final Result */}
                {status === 'completed' && result && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="result-card glass-panel"
                    >
                        <div className="result-header">
                            <Sparkles size={20} className="text-accent" />
                            <h2>Research Conclusion</h2>
                        </div>
                        <div className="markdown-content">
                            <ReactMarkdown remarkPlugins={[remarkGfm]}>{result}</ReactMarkdown>
                        </div>
                    </motion.div>
                )}

            </div>

            {/* Input Area */}
            <div className="input-area-wrapper">
                <div className="input-container glass-panel">
                    <form onSubmit={handleSubmit} className="input-form">
                        <input
                            type="text"
                            className="main-input"
                            placeholder="Ask a research question..."
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            disabled={status === 'thinking'}
                        />
                        <button
                            type="submit"
                            className={`send-btn ${status === 'thinking' ? 'disabled' : ''}`}
                            disabled={status === 'thinking'}
                        >
                            {status === 'thinking' ? <Loader2 className="animate-spin" /> : <Send size={20} />}
                        </button>
                    </form>
                </div>
            </div>

            <style>{`
        .research-container {
          display: flex;
          flex-direction: column;
          height: 100%;
          position: relative;
        }

        .research-content {
          flex: 1;
          padding: 40px;
          padding-bottom: 120px; /* Space for fixed input */
          max-width: 900px;
          margin: 0 auto;
          width: 100%;
          overflow-y: auto;
        }

        .welcome-hero {
          text-align: center;
          margin-top: 100px;
          color: var(--text-secondary);
        }
        
        .welcome-hero h1 {
            color: var(--text-primary);
            font-size: 36px;
            margin: 24px 0 12px;
        }
        
        .hero-icon {
            width: 80px;
            height: 80px;
            border-radius: 20px;
            background: rgba(59, 130, 246, 0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
            border: 1px solid rgba(59, 130, 246, 0.2);
        }

        .input-area-wrapper {
          position: fixed; /* For simplicity in this layout */
          bottom: 24px;
          left: 260px; /* Sidebar width */
          right: 0;
          display: flex;
          justify-content: center;
          padding: 0 40px;
          pointer-events: none; /* Let clicks pass through outside form */
        }

        .input-container {
          width: 100%;
          max-width: 800px;
          border-radius: 16px;
          padding: 8px;
          pointer-events: auto;
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }

        .input-form {
          display: flex;
          gap: 12px;
          align-items: center;
        }

        .main-input {
          flex: 1;
          background: transparent;
          border: none;
          color: var(--text-primary);
          font-size: 16px;
          padding: 12px 16px;
          outline: none;
        }

        .send-btn {
          width: 40px;
          height: 40px;
          border-radius: 10px;
          border: none;
          background: var(--accent-blue);
          color: white;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          transition: all 0.2s;
        }

        .send-btn:hover:not(.disabled) {
          background: #2563eb;
        }
        
        .send-btn.disabled {
            opacity: 0.7;
            cursor: not-allowed;
        }
        
        /* Audit Styles */
        .audit-trail {
            margin-bottom: 40px;
        }
        
        .audit-trail h3 {
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
            margin-bottom: 16px;
            padding-left: 28px;
        }
        
        .logs-container {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        
        .log-item {
            display: flex;
            gap: 12px;
            position: relative;
        }
        
        .log-line {
            position: absolute;
            left: 11px;
            top: 24px;
            bottom: -20px;
            width: 2px;
            background: var(--border-subtle);
            z-index: 0;
        }
        
        .log-item:last-child .log-line {
            display: none;
        }
        
        .log-icon-wrapper {
            position: relative;
            z-index: 1;
            background: var(--bg-app);
            padding: 4px;
        }
        
        .log-text {
            padding-top: 2px;
            color: var(--text-secondary);
            font-size: 14px;
        }
        
        .thinking-pulse {
            margin-left: 36px;
            margin-top: 8px;
            color: var(--text-secondary);
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 8px;
            opacity: 0.7;
        }
        
        .pulse-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--accent-blue);
            animation: pulse-glow 2s infinite;
        }
        
        /* Result Styles */
        .result-card {
            padding: 32px;
            border-radius: var(--radius-lg);
            background: rgba(30, 35, 46, 0.5);
            border: 1px solid var(--accent-blue);
        }
        
        .result-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border-subtle);
        }
        
        .result-header h2 {
            font-size: 18px;
            color: var(--text-primary);
        }
        
        .markdown-content {
            color: #d1d5db;
            line-height: 1.7;
        }
        
        .markdown-content h1, .markdown-content h2, .markdown-content h3 {
            color: var(--text-primary);
            margin-top: 24px;
            margin-bottom: 12px;
        }
        
        .markdown-content p {
            margin-bottom: 16px;
        }
        
        .markdown-content ul {
            padding-left: 20px;
            margin-bottom: 16px;
        }
        
        .markdown-content li {
            margin-bottom: 8px;
        }
        
        .text-accent { color: var(--accent-blue); }
        .text-success { color: var(--accent-green); }

      `}</style>
        </div>
    );
};

export default ResearchModule;
