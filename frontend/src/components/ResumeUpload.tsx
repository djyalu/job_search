import React, { useState } from 'react';
import axios from 'axios';
import './ResumeUpload.css';

const API_BASE_URL = 'http://localhost:8006';

interface ResumeUploadProps {
  onResumeUploaded: (resume: any) => void;
}

const ResumeUpload: React.FC<ResumeUploadProps> = ({ onResumeUploaded }) => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
      setSuccess(null);
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!file) {
      setError('파일을 선택해주세요.');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post(
        `${API_BASE_URL}/api/resume/upload`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      onResumeUploaded(response.data);
      setSuccess('이력서가 성공적으로 업로드되었습니다!');
    } catch (err: any) {
      setError(err.response?.data?.detail || '업로드 중 오류가 발생했습니다.');
      console.error('Upload error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="resume-upload">
      <h2>이력서 업로드</h2>
      <form onSubmit={handleUpload} className="upload-form">
        <div className="form-group">
          <label htmlFor="resume-file">이력서 파일 (PDF, DOCX, TXT)</label>
          <input
            type="file"
            id="resume-file"
            accept=".pdf,.docx,.doc,.txt"
            onChange={handleFileChange}
            className="file-input"
          />
          {file && (
            <div className="file-info">
              선택된 파일: <strong>{file.name}</strong> ({(file.size / 1024).toFixed(2)} KB)
            </div>
          )}
        </div>

        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        <button type="submit" className="upload-btn" disabled={loading || !file}>
          {loading ? '업로드 중...' : '이력서 업로드'}
        </button>
      </form>
    </div>
  );
};

export default ResumeUpload;

