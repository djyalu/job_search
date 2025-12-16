"""
로컬에서 수집된 채용 공고 결과를 보기 좋게 출력하는 스크립트
"""
import json
import sys
import io
from pathlib import Path
from datetime import datetime
from collections import Counter

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass

def load_latest_results():
    """최신 결과 파일 로드"""
    jobs_dir = Path(__file__).parent.parent / 'jobs'
    latest_file = jobs_dir / 'latest.json'
    
    if not latest_file.exists():
        print("[ERROR] 최신 결과 파일을 찾을 수 없습니다.")
        print(f"   경로: {latest_file}")
        print("\n[TIP] 먼저 다음 명령어로 채용 공고를 수집하세요:")
        print("   python scripts/daily_job_search.py")
        return None
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] 파일 읽기 오류: {e}")
        return None

def display_summary(data):
    """요약 정보 출력"""
    print("=" * 70)
    print("[SUMMARY] 채용 공고 수집 결과 요약")
    print("=" * 70)
    print(f"[TIME] 수집 시간: {data['timestamp']}")
    print(f"[KEYWORDS] 검색 키워드: {', '.join(data['keywords'])}")
    print(f"[LOCATION] 검색 지역: {data['location']}")
    print(f"[TOTAL] 총 채용 공고: {data['total']}개")
    print("=" * 70)
    print()

def display_statistics(data):
    """통계 정보 출력"""
    jobs = data['jobs']
    
    # 출처별 통계
    sources = Counter(job['source'] for job in jobs)
    print("[STATS] 출처별 통계:")
    for source, count in sources.most_common():
        print(f"   {source.upper()}: {count}개")
    print()
    
    # 회사별 통계 (상위 10개)
    companies = Counter(job['company'] for job in jobs)
    print("[TOP COMPANIES] 상위 10개 회사:")
    for i, (company, count) in enumerate(companies.most_common(10), 1):
        print(f"   {i:2d}. {company}: {count}개")
    print()

def display_jobs(data, limit=20, source=None):
    """채용 공고 목록 출력"""
    jobs = data['jobs']
    
    if source:
        jobs = [job for job in jobs if job['source'] == source]
    
    print(f"[JOBS] 채용 공고 목록 (최대 {limit}개):")
    print("=" * 70)
    
    for i, job in enumerate(jobs[:limit], 1):
        print(f"\n{i}. {job['title']}")
        print(f"   회사: {job['company']}")
        if job.get('location'):
            print(f"   위치: {job['location']}")
        print(f"   출처: {job['source']}")
        if job.get('url'):
            print(f"   링크: {job['url']}")
        if job.get('description'):
            desc = job['description'][:150] + "..." if len(job['description']) > 150 else job['description']
            print(f"   설명: {desc}")
    
    if len(jobs) > limit:
        print(f"\n... 외 {len(jobs) - limit}개의 채용 공고가 더 있습니다.")
    
    print("\n" + "=" * 70)

def save_html_viewer(data, output_file=None):
    """HTML 뷰어 생성"""
    if output_file is None:
        output_file = Path(__file__).parent.parent / 'jobs' / 'viewer.html'
    
    jobs = data['jobs']
    
    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>채용 공고 수집 결과</title>
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
            margin-bottom: 10px;
        }}
        .summary {{
            background: #f0f4ff;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .summary-item {{
            margin: 5px 0;
            color: #666;
        }}
        .filters {{
            margin-bottom: 20px;
            padding: 15px;
            background: #f9f9f9;
            border-radius: 8px;
        }}
        .filters button {{
            margin-right: 10px;
            padding: 8px 16px;
            border: 2px solid #667eea;
            background: white;
            color: #667eea;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
        }}
        .filters button.active {{
            background: #667eea;
            color: white;
        }}
        .jobs-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }}
        .job-card {{
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            transition: all 0.3s;
        }}
        .job-card:hover {{
            border-color: #667eea;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
            transform: translateY(-2px);
        }}
        .job-title {{
            font-size: 1.2em;
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
        }}
        .job-company {{
            color: #667eea;
            font-weight: 600;
            margin-bottom: 5px;
        }}
        .job-meta {{
            color: #666;
            font-size: 0.9em;
            margin: 5px 0;
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
        .job-description {{
            color: #666;
            font-size: 0.9em;
            line-height: 1.5;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📋 채용 공고 수집 결과</h1>
        <div class="summary">
            <div class="summary-item"><strong>수집 시간:</strong> {data['timestamp']}</div>
            <div class="summary-item"><strong>검색 키워드:</strong> {', '.join(data['keywords'])}</div>
            <div class="summary-item"><strong>검색 지역:</strong> {data['location']}</div>
            <div class="summary-item"><strong>총 채용 공고:</strong> {data['total']}개</div>
        </div>
        
        <div class="filters">
            <button onclick="filterJobs('all')" class="active">전체</button>
            <button onclick="filterJobs('linkedin')">LinkedIn</button>
            <button onclick="filterJobs('indeed')">Indeed</button>
        </div>
        
        <div class="jobs-grid" id="jobsGrid">
"""
    
    for job in jobs:
        location = job.get('location', '위치 정보 없음')
        description = job.get('description', '')[:200] + "..." if len(job.get('description', '')) > 200 else job.get('description', '')
        
        html_content += f"""
            <div class="job-card" data-source="{job['source']}">
                <div class="job-title">{job['title']}</div>
                <div class="job-company">{job['company']}</div>
                <div class="job-meta">📍 {location}</div>
                <div class="job-meta">출처: {job['source'].upper()}</div>
                {f'<div class="job-description">{description}</div>' if description else ''}
                <a href="{job['url']}" target="_blank" class="job-link">자세히 보기 →</a>
            </div>
"""
    
    html_content += """
        </div>
    </div>
    
    <script>
        function filterJobs(source) {
            const cards = document.querySelectorAll('.job-card');
            const buttons = document.querySelectorAll('.filters button');
            
            buttons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            cards.forEach(card => {
                if (source === 'all' || card.dataset.source === source) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }
    </script>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_file

def main():
    """메인 함수"""
    if len(sys.argv) > 1 and sys.argv[1] == '--html':
        # HTML 뷰어 생성 모드
        data = load_latest_results()
        if data:
            html_file = save_html_viewer(data)
            print(f"[SUCCESS] HTML 뷰어가 생성되었습니다: {html_file}")
            print(f"   브라우저에서 열어서 확인하세요!")
    else:
        # 일반 출력 모드
        data = load_latest_results()
        if not data:
            sys.exit(1)
        
        display_summary(data)
        display_statistics(data)
        display_jobs(data)
        
        print("\n[TIP] 팁:")
        print("   - HTML 뷰어 생성: python scripts/view_results.py --html")
        print("   - 특정 출처만 보기: python scripts/view_results.py --source linkedin")

if __name__ == '__main__':
    main()

