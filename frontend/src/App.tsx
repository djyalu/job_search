import React, { useState } from 'react';
import './App.css';
import JobSearch from './components/JobSearch';
import ResumeUpload from './components/ResumeUpload';
import MatchingResults from './components/MatchingResults';
import LocalDashboard from './pages/LocalDashboard';

interface Job {
  id: string;
  title: string;
  company: string;
  location: string | null;
  description: string;
  url: string;
  source: string;
}

interface ResumeData {
  file_id: string;
  filename: string;
  resume_data: any;
}

function App() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [resume, setResume] = useState<ResumeData | null>(null);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [matchingResult, setMatchingResult] = useState<any>(null);
  const [viewMode, setViewMode] = useState<'api' | 'local'>('local');

  // 로컬 대시보드 모드
  if (viewMode === 'local') {
    return <LocalDashboard />;
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>🔍 Job Search & Resume Matching</h1>
        <p>LinkedIn과 Indeed에서 채용 공고를 검색하고 이력서 적합도를 분석하세요</p>
      </header>

      <main className="App-main">
        <div className="container">
          <section className="search-section">
            <JobSearch onJobsFound={setJobs} />
          </section>

          <section className="upload-section">
            <ResumeUpload onResumeUploaded={setResume} />
          </section>

          {jobs.length > 0 && (
            <section className="jobs-section">
              <h2>검색 결과 ({jobs.length}개)</h2>
              <div className="jobs-grid">
                {jobs.map((job) => (
                  <div
                    key={job.id}
                    className={`job-card ${selectedJob?.id === job.id ? 'selected' : ''}`}
                    onClick={() => setSelectedJob(job)}
                  >
                    <h3>{job.title}</h3>
                    <p className="company">{job.company}</p>
                    {job.location && <p className="location">📍 {job.location}</p>}
                    <p className="source">출처: {job.source}</p>
                    <p className="description">{job.description.substring(0, 150)}...</p>
                    <a href={job.url} target="_blank" rel="noopener noreferrer" className="job-link">
                      자세히 보기 →
                    </a>
                  </div>
                ))}
              </div>
            </section>
          )}

          {resume && selectedJob && (
            <section className="matching-section">
              <MatchingResults
                resume={resume}
                job={selectedJob}
                onResult={setMatchingResult}
              />
            </section>
          )}

          {matchingResult && (
            <section className="result-section">
              <h2>적합도 분석 결과</h2>
              <div className="match-score">
                <div className="score-circle">
                  <span className="score-value">{matchingResult.match_score.overall_score}%</span>
                  <span className="score-label">전체 적합도</span>
                </div>
                <div className="score-details">
                  <div className="score-item">
                    <span>스킬 매칭</span>
                    <span>{matchingResult.match_score.skills_match}%</span>
                  </div>
                  <div className="score-item">
                    <span>경력 매칭</span>
                    <span>{matchingResult.match_score.experience_match}%</span>
                  </div>
                  <div className="score-item">
                    <span>학력 매칭</span>
                    <span>{matchingResult.match_score.education_match}%</span>
                  </div>
                  <div className="score-item">
                    <span>설명 매칭</span>
                    <span>{matchingResult.match_score.description_match}%</span>
                  </div>
                </div>
              </div>
              <div className="analysis">
                <h3>상세 분석</h3>
                <pre>{matchingResult.analysis}</pre>
              </div>
            </section>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;

