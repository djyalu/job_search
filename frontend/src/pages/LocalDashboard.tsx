import React, { useState, useEffect } from 'react';
import './LocalDashboard.css';

const API_BASE_URL = 'http://localhost:8006';

interface JobFile {
  name: string;
  size: number;
  modified: string;
}

interface ResumeFile {
  name: string;
  size: number;
  modified: string;
  path: string;
}

const LocalDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'search' | 'results' | 'compare'>('search');
  const [jobFiles, setJobFiles] = useState<JobFile[]>([]);
  const [resumeFiles, setResumeFiles] = useState<ResumeFile[]>([]);
  const [selectedJobFile, setSelectedJobFile] = useState<string>('latest.json');
  const [selectedResume, setSelectedResume] = useState<string>('');
  const [searchKeyword, setSearchKeyword] = useState('');
  const [searchLocation, setSearchLocation] = useState('Seoul, South Korea');
  const [searching, setSearching] = useState(false);
  const [comparing, setComparing] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);

  useEffect(() => {
    loadJobFiles();
    loadResumeFiles();
  }, []);

  const loadJobFiles = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/local/jobs/list`);
      const data = await response.json();
      setJobFiles(data.files || []);
    } catch (error) {
      console.error('Failed to load job files:', error);
    }
  };

  const loadResumeFiles = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/local/uploads/list`);
      const data = await response.json();
      setResumeFiles(data.files || []);
    } catch (error) {
      console.error('Failed to load resume files:', error);
    }
  };

  const handleSearch = async () => {
    if (!searchKeyword.trim()) {
      setMessage({ type: 'error', text: '검색 키워드를 입력하세요' });
      return;
    }

    setSearching(true);
    setMessage(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/local/jobs/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          keyword: searchKeyword,
          location: searchLocation,
          max_results: 30,
        }),
      });

      const data = await response.json();

      if (data.success) {
        setMessage({ type: 'success', text: '채용 공고 검색이 완료되었습니다!' });
        loadJobFiles();
        setTimeout(() => setActiveTab('results'), 1000);
      } else {
        setMessage({ type: 'error', text: data.message || '검색 중 오류가 발생했습니다' });
      }
    } catch (error: any) {
      setMessage({ type: 'error', text: `오류: ${error.message}` });
    } finally {
      setSearching(false);
    }
  };

  const handleCompare = async () => {
    if (!selectedResume) {
      setMessage({ type: 'error', text: '이력서를 선택하세요' });
      return;
    }

    setComparing(true);
    setMessage(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/local/resume/compare`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          resume_path: selectedResume,
          jobs_file: selectedJobFile,
          top_n: 10,
        }),
      });

      const data = await response.json();

      if (data.success) {
        setMessage({ type: 'success', text: '비교 분석이 완료되었습니다!' });
        // 리포트 열기
        window.open(`${API_BASE_URL}/api/local/reports/comparison`, '_blank');
      } else {
        setMessage({ type: 'error', text: data.message || '비교 중 오류가 발생했습니다' });
      }
    } catch (error: any) {
      setMessage({ type: 'error', text: `오류: ${error.message}` });
    } finally {
      setComparing(false);
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_BASE_URL}/api/local/resume/upload`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (data.success) {
        setMessage({ type: 'success', text: '이력서가 업로드되었습니다!' });
        loadResumeFiles();
      } else {
        setMessage({ type: 'error', text: data.message || '업로드 중 오류가 발생했습니다' });
      }
    } catch (error: any) {
      setMessage({ type: 'error', text: `오류: ${error.message}` });
    }
  };

  const viewJobResults = (filename: string) => {
    window.open(`${API_BASE_URL}/api/local/jobs/${filename}`, '_blank');
  };

  return (
    <div className="local-dashboard">
      <header className="dashboard-header">
        <h1>🔍 Job Search & Resume Matching - Local Dashboard</h1>
        <p>로컬에서 채용 공고를 검색하고 이력서를 비교하세요</p>
      </header>

      {message && (
        <div className={`message ${message.type}`}>
          {message.text}
          <button onClick={() => setMessage(null)}>×</button>
        </div>
      )}

      <div className="tabs">
        <button
          className={activeTab === 'search' ? 'active' : ''}
          onClick={() => setActiveTab('search')}
        >
          채용 공고 검색
        </button>
        <button
          className={activeTab === 'results' ? 'active' : ''}
          onClick={() => setActiveTab('results')}
        >
          결과 확인
        </button>
        <button
          className={activeTab === 'compare' ? 'active' : ''}
          onClick={() => setActiveTab('compare')}
        >
          이력서 비교
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'search' && (
          <div className="search-panel">
            <h2>채용 공고 검색</h2>
            <div className="form-group">
              <label>검색 키워드 *</label>
              <input
                type="text"
                value={searchKeyword}
                onChange={(e) => setSearchKeyword(e.target.value)}
                placeholder="예: Python Developer, Software Engineer"
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              />
            </div>
            <div className="form-group">
              <label>검색 지역</label>
              <input
                type="text"
                value={searchLocation}
                onChange={(e) => setSearchLocation(e.target.value)}
                placeholder="예: Seoul, South Korea"
              />
            </div>
            <button
              className="primary-button"
              onClick={handleSearch}
              disabled={searching}
            >
              {searching ? '검색 중...' : '검색 시작'}
            </button>
            {searching && (
              <div className="loading">
                <p>채용 공고를 수집하고 있습니다. 몇 분 정도 걸릴 수 있습니다...</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'results' && (
          <div className="results-panel">
            <h2>수집된 채용 공고</h2>
            <div className="file-list">
              {jobFiles.length === 0 ? (
                <p className="empty">수집된 채용 공고가 없습니다. 먼저 검색을 실행하세요.</p>
              ) : (
                jobFiles.map((file) => (
                  <div key={file.name} className="file-item">
                    <div className="file-info">
                      <h3>{file.name}</h3>
                      <p>
                        크기: {(file.size / 1024).toFixed(2)} KB | 
                        수정: {new Date(file.modified).toLocaleString('ko-KR')}
                      </p>
                    </div>
                    <button
                      className="secondary-button"
                      onClick={() => viewJobResults(file.name)}
                    >
                      JSON 보기
                    </button>
                  </div>
                ))
              )}
            </div>
          </div>
        )}

        {activeTab === 'compare' && (
          <div className="compare-panel">
            <h2>이력서와 채용 공고 비교</h2>
            
            <div className="form-section">
              <h3>1. 이력서 업로드</h3>
              <div className="upload-area">
                <input
                  type="file"
                  id="resume-upload"
                  accept=".pdf,.docx,.doc,.txt"
                  onChange={handleFileUpload}
                  style={{ display: 'none' }}
                />
                <label htmlFor="resume-upload" className="upload-button">
                  📄 이력서 파일 선택 (PDF, DOCX, TXT)
                </label>
              </div>
              
              {resumeFiles.length > 0 && (
                <div className="resume-list">
                  <h4>업로드된 이력서:</h4>
                  {resumeFiles.map((file) => (
                    <label key={file.path} className="resume-item">
                      <input
                        type="radio"
                        name="resume"
                        value={file.path}
                        checked={selectedResume === file.path}
                        onChange={(e) => setSelectedResume(e.target.value)}
                      />
                      <span>{file.name}</span>
                      <small>{(file.size / 1024).toFixed(2)} KB</small>
                    </label>
                  ))}
                </div>
              )}
            </div>

            <div className="form-section">
              <h3>2. 채용 공고 선택</h3>
              <select
                value={selectedJobFile}
                onChange={(e) => setSelectedJobFile(e.target.value)}
                className="select-input"
              >
                {jobFiles.map((file) => (
                  <option key={file.name} value={file.name}>
                    {file.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-section">
              <button
                className="primary-button"
                onClick={handleCompare}
                disabled={comparing || !selectedResume || jobFiles.length === 0}
              >
                {comparing ? '비교 중...' : '비교 분석 시작'}
              </button>
              {comparing && (
                <div className="loading">
                  <p>이력서와 채용 공고를 비교하고 있습니다...</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default LocalDashboard;

