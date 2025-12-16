"""
로컬에 업로드한 이력서와 수집된 채용 공고를 비교 분석하는 스크립트
"""
import json
import sys
import io
from pathlib import Path
from datetime import datetime

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except:
        pass

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.resume_parser import ResumeParser
from app.services.matching import MatchingService
from app.models.job import JobPosting

def load_resume(file_path):
    """이력서 파일 로드 및 파싱"""
    parser = ResumeParser()
    
    if not Path(file_path).exists():
        print(f"[ERROR] 이력서 파일을 찾을 수 없습니다: {file_path}")
        return None
    
    try:
        print(f"[INFO] 이력서 파싱 중: {file_path}")
        import asyncio
        file_id, resume_data = asyncio.run(parser.parse_resume(file_path, Path(file_path).name))
        print(f"[SUCCESS] 이력서 파싱 완료")
        return resume_data
    except Exception as e:
        print(f"[ERROR] 이력서 파싱 오류: {e}")
        import traceback
        traceback.print_exc()
        return None

def load_jobs(jobs_file=None):
    """채용 공고 파일 로드"""
    if jobs_file is None:
        jobs_file = Path(__file__).parent.parent / 'jobs' / 'latest.json'
    else:
        jobs_file = Path(jobs_file)
    
    if not jobs_file.exists():
        print(f"[ERROR] 채용 공고 파일을 찾을 수 없습니다: {jobs_file}")
        print(f"[TIP] 먼저 채용 공고를 수집하세요: python scripts/run_local.py")
        return None
    
    try:
        with open(jobs_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # JSON 데이터를 JobPosting 객체로 변환
        jobs = []
        for job_data in data.get('jobs', []):
            try:
                job = JobPosting(**job_data)
                jobs.append(job)
            except Exception as e:
                print(f"[WARNING] 채용 공고 파싱 오류: {e}")
                continue
        
        print(f"[SUCCESS] {len(jobs)}개의 채용 공고 로드 완료")
        return jobs
    except Exception as e:
        print(f"[ERROR] 채용 공고 파일 읽기 오류: {e}")
        return None

def compare_resume_with_jobs(resume_data, jobs, top_n=10):
    """이력서와 채용 공고 비교"""
    matching_service = MatchingService()
    
    print(f"\n[COMPARING] 이력서와 {len(jobs)}개 채용 공고 비교 중...")
    print("=" * 70)
    
    results = []
    
    import asyncio
    async def compare_all():
        tasks = []
        for job in jobs:
            tasks.append(matching_service.calculate_match(resume_data, job))
        
        match_scores = await asyncio.gather(*tasks)
        return match_scores
    
    match_scores = asyncio.run(compare_all())
    
    # 결과 정리
    for job, score in zip(jobs, match_scores):
        results.append({
            'job': job,
            'score': score,
            'overall_score': score.overall_score
        })
    
    # 점수순으로 정렬
    results.sort(key=lambda x: x['overall_score'], reverse=True)
    
    return results[:top_n]

def display_comparison_results(resume_data, results):
    """비교 결과 출력"""
    print("\n" + "=" * 70)
    print("[RESULTS] 이력서 적합도 분석 결과 (상위 10개)")
    print("=" * 70)
    
    for i, result in enumerate(results, 1):
        job = result['job']
        score = result['score']
        
        print(f"\n[{i}] {job.title}")
        print(f"    회사: {job.company}")
        if job.location:
            print(f"    위치: {job.location}")
        print(f"    출처: {job.source}")
        print(f"    링크: {job.url}")
        print()
        print(f"    [SCORE] 전체 적합도: {score.overall_score}%")
        print(f"    - 스킬 매칭: {score.skills_match}%")
        print(f"    - 경력 매칭: {score.experience_match}%")
        print(f"    - 학력 매칭: {score.education_match}%")
        print(f"    - 설명 매칭: {score.description_match}%")
        print()
        
        if score.matched_keywords:
            print(f"    [MATCHED] 매칭된 키워드:")
            print(f"    {', '.join(score.matched_keywords[:10])}")
            print()
        
        if score.missing_keywords:
            print(f"    [MISSING] 누락된 키워드:")
            print(f"    {', '.join(score.missing_keywords[:5])}")
            print()
        
        if score.recommendations:
            print(f"    [RECOMMENDATIONS] 추천사항:")
            for rec in score.recommendations[:3]:
                print(f"    - {rec}")
        
        print("-" * 70)

def save_comparison_report(resume_data, results, output_file=None):
    """비교 결과를 HTML 리포트로 저장"""
    if output_file is None:
        output_file = Path(__file__).parent.parent / 'jobs' / 'resume_comparison.html'
    
    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>이력서 적합도 분석 리포트</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            margin-bottom: 20px;
        }}
        .resume-info {{
            background: #f0f4ff;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .resume-info h2 {{
            color: #667eea;
            margin-bottom: 10px;
        }}
        .resume-info p {{
            margin: 5px 0;
            color: #666;
        }}
        .job-card {{
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            transition: all 0.3s;
        }}
        .job-card:hover {{
            border-color: #667eea;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        }}
        .job-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 15px;
        }}
        .job-title {{
            font-size: 1.3em;
            font-weight: 600;
            color: #333;
        }}
        .score-circle {{
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }}
        .score-value {{
            font-size: 1.8em;
        }}
        .score-label {{
            font-size: 0.8em;
            opacity: 0.9;
        }}
        .job-company {{
            color: #667eea;
            font-weight: 600;
            margin: 5px 0;
        }}
        .job-meta {{
            color: #666;
            font-size: 0.9em;
            margin: 3px 0;
        }}
        .score-details {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin: 15px 0;
            padding: 15px;
            background: #f9f9f9;
            border-radius: 8px;
        }}
        .score-item {{
            text-align: center;
        }}
        .score-item-label {{
            color: #666;
            font-size: 0.85em;
            margin-bottom: 5px;
        }}
        .score-item-value {{
            color: #667eea;
            font-size: 1.2em;
            font-weight: 600;
        }}
        .keywords {{
            margin: 15px 0;
        }}
        .keywords h3 {{
            color: #333;
            font-size: 0.95em;
            margin-bottom: 8px;
        }}
        .keyword-tag {{
            display: inline-block;
            padding: 4px 10px;
            background: #e8f0fe;
            color: #1967d2;
            border-radius: 12px;
            font-size: 0.85em;
            margin: 3px;
        }}
        .keyword-tag.missing {{
            background: #fce8e6;
            color: #c5221f;
        }}
        .recommendations {{
            margin-top: 15px;
            padding: 15px;
            background: #fff9e6;
            border-radius: 8px;
            border-left: 4px solid #fbbc04;
        }}
        .recommendations h3 {{
            color: #333;
            margin-bottom: 10px;
        }}
        .recommendations ul {{
            margin-left: 20px;
        }}
        .recommendations li {{
            margin: 5px 0;
            color: #666;
        }}
        .job-link {{
            display: inline-block;
            margin-top: 10px;
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }}
        .job-link:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 이력서 적합도 분석 리포트</h1>
        <div class="resume-info">
            <h2>이력서 정보</h2>
            {f'<p><strong>이름:</strong> {resume_data.name}</p>' if resume_data.name else ''}
            {f'<p><strong>이메일:</strong> {resume_data.email}</p>' if resume_data.email else ''}
            {f'<p><strong>전화번호:</strong> {resume_data.phone}</p>' if resume_data.phone else ''}
            {f'<p><strong>보유 스킬:</strong> {", ".join(resume_data.skills[:10])}</p>' if resume_data.skills else ''}
            <p><strong>생성 시간:</strong> {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}</p>
        </div>
"""
    
    for i, result in enumerate(results, 1):
        job = result['job']
        score = result['score']
        
        # 점수에 따른 색상 결정
        score_color = "#4caf50" if score.overall_score >= 70 else "#ff9800" if score.overall_score >= 50 else "#f44336"
        
        html_content += f"""
        <div class="job-card">
            <div class="job-header">
                <div>
                    <div class="job-title">{job.title}</div>
                    <div class="job-company">{job.company}</div>
                    {f'<div class="job-meta">📍 {job.location}</div>' if job.location else ''}
                    <div class="job-meta">출처: {job.source.upper()}</div>
                </div>
                <div class="score-circle" style="background: {score_color};">
                    <div class="score-value">{score.overall_score}%</div>
                    <div class="score-label">적합도</div>
                </div>
            </div>
            
            <div class="score-details">
                <div class="score-item">
                    <div class="score-item-label">스킬 매칭</div>
                    <div class="score-item-value">{score.skills_match}%</div>
                </div>
                <div class="score-item">
                    <div class="score-item-label">경력 매칭</div>
                    <div class="score-item-value">{score.experience_match}%</div>
                </div>
                <div class="score-item">
                    <div class="score-item-label">학력 매칭</div>
                    <div class="score-item-value">{score.education_match}%</div>
                </div>
                <div class="score-item">
                    <div class="score-item-label">설명 매칭</div>
                    <div class="score-item-value">{score.description_match}%</div>
                </div>
            </div>
"""
        
        if score.matched_keywords:
            html_content += f"""
            <div class="keywords">
                <h3>✅ 매칭된 키워드</h3>
                {''.join([f'<span class="keyword-tag">{kw}</span>' for kw in score.matched_keywords[:15]])}
            </div>
"""
        
        if score.missing_keywords:
            html_content += f"""
            <div class="keywords">
                <h3>❌ 누락된 키워드</h3>
                {''.join([f'<span class="keyword-tag missing">{kw}</span>' for kw in score.missing_keywords[:10]])}
            </div>
"""
        
        if score.recommendations:
            html_content += f"""
            <div class="recommendations">
                <h3>💡 추천사항</h3>
                <ul>
                    {''.join([f'<li>{rec}</li>' for rec in score.recommendations])}
                </ul>
            </div>
"""
        
        html_content += f"""
            <a href="{job.url}" target="_blank" class="job-link">채용 공고 자세히 보기 →</a>
        </div>
"""
    
    html_content += """
    </div>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_file

def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description='이력서와 채용 공고 비교 분석')
    parser.add_argument('resume', help='이력서 파일 경로 (PDF, DOCX, TXT)')
    parser.add_argument('--jobs', help='채용 공고 JSON 파일 경로 (기본: jobs/latest.json)')
    parser.add_argument('--top', type=int, default=10, help='상위 N개 결과만 표시 (기본: 10)')
    parser.add_argument('--html', action='store_true', help='HTML 리포트 생성')
    parser.add_argument('--output', help='HTML 리포트 출력 파일 경로')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("[RESUME COMPARISON] 이력서 적합도 분석")
    print("=" * 70)
    
    # 이력서 로드
    resume_data = load_resume(args.resume)
    if not resume_data:
        sys.exit(1)
    
    # 채용 공고 로드
    jobs = load_jobs(args.jobs)
    if not jobs:
        sys.exit(1)
    
    # 비교 분석
    results = compare_resume_with_jobs(resume_data, jobs, args.top)
    
    # 결과 출력
    display_comparison_results(resume_data, results)
    
    # HTML 리포트 생성
    if args.html or args.output:
        html_file = save_comparison_report(resume_data, results, args.output)
        print(f"\n[SUCCESS] HTML 리포트 생성 완료: {html_file}")
        print(f"   브라우저에서 열어서 확인하세요!")

if __name__ == '__main__':
    main()

