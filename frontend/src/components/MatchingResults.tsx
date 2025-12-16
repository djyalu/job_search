import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './MatchingResults.css';

const API_BASE_URL = 'http://localhost:8006';

interface MatchingResultsProps {
  resume: any;
  job: any;
  onResult: (result: any) => void;
}

const MatchingResults: React.FC<MatchingResultsProps> = ({ resume, job, onResult }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const analyzeMatch = async () => {
      // 먼저 채용 공고를 저장소에 저장
      try {
        await axios.post(`${API_BASE_URL}/api/matching/store-job`, job);
      } catch (err) {
        console.error('Failed to store job:', err);
      }

      // 적합도 분석 요청
      setLoading(true);
      setError(null);

      try {
        const response = await axios.post(`${API_BASE_URL}/api/matching/analyze`, {
          resume_id: resume.file_id,
          job_id: job.id,
        });

        onResult(response.data);
      } catch (err: any) {
        setError(err.response?.data?.detail || '분석 중 오류가 발생했습니다.');
        console.error('Matching error:', err);
      } finally {
        setLoading(false);
      }
    };

    if (resume && job) {
      analyzeMatch();
    }
  }, [resume, job, onResult]);

  if (loading) {
    return (
      <div className="matching-results">
        <h2>적합도 분석 중...</h2>
        <div className="loading-spinner">⏳</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="matching-results">
        <div className="error-message">{error}</div>
      </div>
    );
  }

  return null;
};

export default MatchingResults;

