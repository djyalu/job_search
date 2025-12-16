import React, { useState } from 'react';
import axios from 'axios';
import './JobSearch.css';

const API_BASE_URL = 'http://localhost:8006';

interface JobSearchProps {
  onJobsFound: (jobs: any[]) => void;
}

const JobSearch: React.FC<JobSearchProps> = ({ onJobsFound }) => {
  const [keyword, setKeyword] = useState('');
  const [location, setLocation] = useState('');
  const [maxResults, setMaxResults] = useState(20);
  const [sources, setSources] = useState(['linkedin', 'indeed']);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/jobs/search`, {
        keyword,
        location: location || undefined,
        max_results: maxResults,
        sources,
      });

      onJobsFound(response.data.jobs);
    } catch (err: any) {
      setError(err.response?.data?.detail || '검색 중 오류가 발생했습니다.');
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleSource = (source: string) => {
    if (sources.includes(source)) {
      setSources(sources.filter(s => s !== source));
    } else {
      setSources([...sources, source]);
    }
  };

  return (
    <div className="job-search">
      <h2>채용 공고 검색</h2>
      <form onSubmit={handleSearch} className="search-form">
        <div className="form-group">
          <label htmlFor="keyword">검색 키워드 *</label>
          <input
            type="text"
            id="keyword"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            placeholder="예: Python Developer, Software Engineer"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="location">지역 (선택사항)</label>
          <input
            type="text"
            id="location"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="예: Seoul, South Korea"
          />
        </div>

        <div className="form-group">
          <label htmlFor="maxResults">최대 결과 수</label>
          <input
            type="number"
            id="maxResults"
            value={maxResults}
            onChange={(e) => setMaxResults(parseInt(e.target.value))}
            min="1"
            max="100"
          />
        </div>

        <div className="form-group">
          <label>검색 플랫폼</label>
          <div className="source-buttons">
            <button
              type="button"
              className={`source-btn ${sources.includes('linkedin') ? 'active' : ''}`}
              onClick={() => toggleSource('linkedin')}
            >
              LinkedIn
            </button>
            <button
              type="button"
              className={`source-btn ${sources.includes('indeed') ? 'active' : ''}`}
              onClick={() => toggleSource('indeed')}
            >
              Indeed
            </button>
          </div>
        </div>

        {error && <div className="error-message">{error}</div>}

        <button type="submit" className="search-btn" disabled={loading || sources.length === 0}>
          {loading ? '검색 중...' : '검색하기'}
        </button>
      </form>
    </div>
  );
};

export default JobSearch;

