import React, { useState, useRef } from 'react';
import { Upload, FileIcon, X, CheckCircle, AlertCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const KnowledgeBaseModule = () => {
    const [dragActive, setDragActive] = useState(false);
    const [files, setFiles] = useState([]);
    const [uploadStatus, setUploadStatus] = useState(null); // 'uploading', 'success', 'error'
    const inputRef = useRef(null);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFiles(Array.from(e.dataTransfer.files));
        }
    };

    const handleChange = (e) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            handleFiles(Array.from(e.target.files));
        }
    };

    const handleFiles = (newFiles) => {
        setFiles((prev) => [...prev, ...newFiles]);
        setUploadStatus(null);
    };

    const removeFile = (index) => {
        setFiles((prev) => prev.filter((_, i) => i !== index));
    };

    const uploadFiles = async () => {
        if (files.length === 0) return;

        setUploadStatus('uploading');
        const formData = new FormData();
        files.forEach(file => {
            formData.append('file', file);
        });

        try {
            // Updated to point to localhost:8000
            const response = await fetch('http://127.0.0.1:8000/uploadFiles', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                setUploadStatus('success');
                setTimeout(() => {
                    setFiles([]);
                    setUploadStatus(null);
                }, 3000);
            } else {
                setUploadStatus('error');
            }
        } catch (error) {
            setUploadStatus('error');
            console.error(error);
        }
    };

    return (
        <div className="kb-container">
            <div className="kb-header">
                <h1>Knowledge Base</h1>
                <p>Upload documents to contextualize the AI research.</p>
            </div>

            <div className="upload-section">
                <form
                    className={`upload-zone ${dragActive ? 'active' : ''}`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                    onClick={() => inputRef.current.click()}
                >
                    <input
                        ref={inputRef}
                        type="file"
                        multiple
                        className="hidden-input"
                        onChange={handleChange}
                    />
                    <div className="upload-content">
                        <div className="icon-circle">
                            <Upload size={24} className="text-accent" />
                        </div>
                        <h3>Click to upload or drag and drop</h3>
                        <p>PDF, TXT, DOCX (Max 16MB)</p>
                    </div>
                </form>
            </div>

            <AnimatePresence>
                {files.length > 0 && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0 }}
                        className="file-list"
                    >
                        <h3>Selected Files ({files.length})</h3>
                        <div className="files-grid">
                            {files.map((file, idx) => (
                                <div key={idx} className="file-item card">
                                    <FileIcon size={20} className="file-icon" />
                                    <span className="file-name">{file.name}</span>
                                    <button onClick={(e) => { e.stopPropagation(); removeFile(idx); }} className="remove-btn">
                                        <X size={16} />
                                    </button>
                                </div>
                            ))}
                        </div>

                        <div className="actions">
                            <button
                                className="btn btn-primary"
                                onClick={uploadFiles}
                                disabled={uploadStatus === 'uploading'}
                            >
                                {uploadStatus === 'uploading' ? 'Uploading...' : 'Upload All Files'}
                            </button>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            {uploadStatus === 'success' && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="status-msg success">
                    <CheckCircle size={20} />
                    Files uploaded successfully!
                </motion.div>
            )}

            {uploadStatus === 'error' && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="status-msg error">
                    <AlertCircle size={20} />
                    Upload failed. Please try again.
                </motion.div>
            )}

            <style>{`
        .kb-container {
          padding: 40px;
          max-width: 1000px;
          margin: 0 auto;
        }

        .kb-header h1 {
          font-size: 32px;
          margin-bottom: 8px;
          font-weight: 700;
        }
        
        .kb-header p {
            color: var(--text-secondary);
            margin-bottom: 32px;
        }

        .upload-zone {
          border: 2px dashed var(--border-subtle);
          border-radius: var(--radius-lg);
          padding: 48px;
          text-align: center;
          cursor: pointer;
          transition: all 0.2s;
          background: rgba(30, 35, 46, 0.3);
        }

        .upload-zone:hover, .upload-zone.active {
          border-color: var(--accent-blue);
          background: rgba(59, 130, 246, 0.05);
        }

        .hidden-input {
          display: none;
        }
        
        .upload-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
        }
        
        .icon-circle {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: var(--bg-card);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 8px;
            border: 1px solid var(--border-subtle);
        }
        
        .text-accent { color: var(--accent-blue); }

        .file-list {
            margin-top: 32px;
        }
        
        .files-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 16px;
            margin-top: 16px;
            margin-bottom: 24px;
        }
        
        .file-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            position: relative;
        }
        
        .file-name {
            font-size: 14px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            flex: 1;
        }
        
        .file-icon { color: var(--text-secondary); }
        
        .remove-btn {
            background: none;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            padding: 4px;
            border-radius: 4px;
        }
        
        .remove-btn:hover {
            background: rgba(255,255,255,0.1);
            color: #ef4444;
        }
        
        .status-msg {
            margin-top: 24px;
            padding: 16px;
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .status-msg.success {
            background: rgba(34, 197, 94, 0.1);
            color: #22c55e;
            border: 1px solid rgba(34, 197, 94, 0.2);
        }
        
        .status-msg.error {
            background: rgba(239, 68, 68, 0.1);
            color: #ef4444;
            border: 1px solid rgba(239, 68, 68, 0.2);
        }

      `}</style>
        </div>
    );
};

export default KnowledgeBaseModule;
