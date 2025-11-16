import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE_URL = 'http://localhost:8000';
const USER_ID = 1; // Placeholder user ID

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [extractedText, setExtractedText] = useState('');
  const [fileName, setFileName] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [savedFiles, setSavedFiles] = useState([]);
  const [isLoadingFiles, setIsLoadingFiles] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  // Load saved files on component mount
  useEffect(() => {
    loadFiles();
  }, []);

  const loadFiles = async () => {
    setIsLoadingFiles(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/files/${USER_ID}`);
      if (response.data.success) {
        setSavedFiles(response.data.files);
      }
    } catch (error) {
      showMessage('error', 'Failed to load saved files');
      console.error('Error loading files:', error);
    } finally {
      setIsLoadingFiles(false);
    }
  };

  const showMessage = (type, text) => {
    setMessage({ type, text });
    setTimeout(() => setMessage({ type: '', text: '' }), 5000);
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (!file.type.startsWith('image/')) {
        showMessage('error', 'Please select an image file');
        return;
      }
      setSelectedFile(file);
      setExtractedText('');
      setFileName('');
    }
  };

  const handleProcess = async () => {
    if (!selectedFile) {
      showMessage('error', 'Please select an image file first');
      return;
    }

    setIsProcessing(true);
    setMessage({ type: '', text: '' });

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('user_id', USER_ID);

      const response = await axios.post(
        `${API_BASE_URL}/process-image`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      if (response.data.success) {
        setExtractedText(response.data.text);
        showMessage('success', `Text extracted successfully! (${response.data.word_count} words)`);
      } else {
        showMessage('error', 'Failed to extract text from image');
      }
    } catch (error) {
      showMessage('error', error.response?.data?.detail || 'Error processing image');
      console.error('Error processing image:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleSave = async () => {
    if (!extractedText.trim()) {
      showMessage('error', 'No text to save. Please process an image first.');
      return;
    }

    if (!fileName.trim()) {
      showMessage('error', 'Please enter a file name');
      return;
    }

    setIsSaving(true);
    setMessage({ type: '', text: '' });

    try {
      const formData = new FormData();
      formData.append('file_name', fileName.trim());
      formData.append('text_content', extractedText);
      formData.append('user_id', USER_ID);

      const response = await axios.post(
        `${API_BASE_URL}/save-text`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      if (response.data.success) {
        showMessage('success', 'File saved successfully!');
        setFileName('');
        setExtractedText('');
        setSelectedFile(null);
        // Reset file input
        document.getElementById('file-input').value = '';
        // Reload files list
        loadFiles();
      } else {
        showMessage('error', 'Failed to save file');
      }
    } catch (error) {
      showMessage('error', error.response?.data?.detail || 'Error saving file');
      console.error('Error saving file:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleDownload = async (fileId, fileName) => {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/download/${fileId}`,
        {
          responseType: 'blob',
        }
      );

      // Create a blob URL and trigger download
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', fileName);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      showMessage('success', 'File downloaded successfully!');
    } catch (error) {
      showMessage('error', 'Error downloading file');
      console.error('Error downloading file:', error);
    }
  };

  const handleDelete = async (fileId) => {
    if (!window.confirm('Are you sure you want to delete this file?')) {
      return;
    }

    try {
      const response = await axios.delete(`${API_BASE_URL}/files/${fileId}`);
      if (response.data.success) {
        showMessage('success', 'File deleted successfully!');
        loadFiles();
      }
    } catch (error) {
      showMessage('error', 'Error deleting file');
      console.error('Error deleting file:', error);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>📄 OCR Dashboard</h1>
          <p>Extract text from images and manage your files</p>
        </header>

        {message.text && (
          <div className={`message message-${message.type}`}>
            {message.text}
          </div>
        )}

        <div className="main-content">
          {/* Upload and Process Section */}
          <div className="card upload-section">
            <h2>Upload & Process Image</h2>
            <div className="upload-area">
              <input
                type="file"
                id="file-input"
                accept="image/*"
                onChange={handleFileChange}
                className="file-input"
              />
              <label htmlFor="file-input" className="file-label">
                {selectedFile ? selectedFile.name : 'Choose Image File'}
              </label>
              <button
                onClick={handleProcess}
                disabled={!selectedFile || isProcessing}
                className="btn btn-primary"
              >
                {isProcessing ? 'Processing...' : 'Process Image'}
              </button>
            </div>
          </div>

          {/* Text Preview Section */}
          {extractedText && (
            <div className="card preview-section">
              <h2>Extracted Text Preview</h2>
              <div className="text-preview">
                <pre>{extractedText || 'No text extracted yet...'}</pre>
              </div>
              <div className="save-section">
                <input
                  type="text"
                  placeholder="Enter file name (e.g., invoice_001)"
                  value={fileName}
                  onChange={(e) => setFileName(e.target.value)}
                  className="file-name-input"
                />
                <button
                  onClick={handleSave}
                  disabled={!extractedText || !fileName.trim() || isSaving}
                  className="btn btn-success"
                >
                  {isSaving ? 'Saving...' : 'Save to Database'}
                </button>
              </div>
            </div>
          )}

          {/* Saved Files Section */}
          <div className="card files-section">
            <div className="section-header">
              <h2>Saved Files</h2>
              <button onClick={loadFiles} className="btn btn-secondary" disabled={isLoadingFiles}>
                {isLoadingFiles ? 'Loading...' : 'Refresh'}
              </button>
            </div>
            {isLoadingFiles ? (
              <div className="loading">Loading files...</div>
            ) : savedFiles.length === 0 ? (
              <div className="empty-state">No files saved yet. Process and save an image to get started!</div>
            ) : (
              <div className="files-table">
                <table>
                  <thead>
                    <tr>
                      <th>File Name</th>
                      <th>Created Date</th>
                      <th>Size</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {savedFiles.map((file) => (
                      <tr key={file.id}>
                        <td>{file.file_name}</td>
                        <td>{formatDate(file.created_at)}</td>
                        <td>{file.content_length} chars</td>
                        <td>
                          <button
                            onClick={() => handleDownload(file.id, file.file_name)}
                            className="btn btn-small btn-primary"
                          >
                            Download
                          </button>
                          <button
                            onClick={() => handleDelete(file.id)}
                            className="btn btn-small btn-danger"
                          >
                            Delete
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

