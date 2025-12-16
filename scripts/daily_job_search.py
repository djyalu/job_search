"""
GitHub Actions에서 실행되는 일일 채용 공고 검색 스크립트
"""
import os
import sys
import json
from datetime import datetime
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.job_search import JobSearchService
from app.models.job import JobSearchRequest

def main():
    """메인 실행 함수"""
    # 검색 키워드 설정 (환경 변수 또는 기본값)
    keywords = os.getenv('SEARCH_KEYWORDS', 'Python Developer,Software Engineer').split(',')
    location = os.getenv('SEARCH_LOCATION', 'Seoul, South Korea')
    
    # 결과 저장 디렉토리
    jobs_dir = Path(__file__).parent.parent / 'jobs'
    jobs_dir.mkdir(exist_ok=True)
    
    all_jobs = []
    search_service = JobSearchService()
    
    print(f"🔍 채용 공고 검색 시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 비동기 실행을 위한 래퍼
    import asyncio
    
    async def search_all_keywords():
        """모든 키워드로 비동기 검색"""
        tasks = []
        for keyword in keywords:
            keyword = keyword.strip()
            if not keyword:
                continue
                
            print(f"\n📌 검색 키워드: {keyword}")
            
            request = JobSearchRequest(
                keyword=keyword,
                location=location,
                max_results=30,
                sources=['linkedin', 'indeed']
            )
            
            tasks.append(search_service.search_jobs(request))
        
        # 모든 검색을 병렬로 실행
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        jobs_list = []
        for idx, result in enumerate(results):
            if isinstance(result, list):
                print(f"✅ {len(result)}개의 채용 공고 발견")
                jobs_list.extend(result)
            elif isinstance(result, Exception):
                print(f"❌ 검색 오류: {result}")
        
        return jobs_list
    
    all_jobs = asyncio.run(search_all_keywords())
    
    # 중복 제거 (URL 기준)
    seen_urls = set()
    unique_jobs = []
    for job in all_jobs:
        if job.url not in seen_urls:
            seen_urls.add(job.url)
            unique_jobs.append(job)
    
    print(f"\n📊 총 {len(unique_jobs)}개의 고유한 채용 공고 발견")
    
    # 결과를 JSON 파일로 저장
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = jobs_dir / f'jobs_{timestamp}.json'
    
    # Pydantic 모델을 dict로 변환
    jobs_data = [job.model_dump() for job in unique_jobs]
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total': len(unique_jobs),
            'keywords': keywords,
            'location': location,
            'jobs': jobs_data
        }, f, ensure_ascii=False, indent=2)
    
    print(f"💾 결과 저장: {output_file}")
    
    # 최신 결과를 latest.json으로도 저장
    latest_file = jobs_dir / 'latest.json'
    with open(latest_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total': len(unique_jobs),
            'keywords': keywords,
            'location': location,
            'jobs': jobs_data
        }, f, ensure_ascii=False, indent=2)
    
    print(f"💾 최신 결과 저장: {latest_file}")
    
    # README 업데이트
    update_readme(unique_jobs, keywords, location)
    
    print("\n✅ 작업 완료!")
    print(f"\n💡 결과 확인 방법:")
    print(f"   1. JSON 파일: {latest_file}")
    print(f"   2. 콘솔 출력: python scripts/view_results.py")
    print(f"   3. HTML 뷰어: python scripts/view_results.py --html")

def update_readme(jobs, keywords, location):
    """README 파일에 최신 채용 공고 정보 업데이트"""
    readme_path = Path(__file__).parent.parent / 'README.md'
    
    if not readme_path.exists():
        return
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    # 최신 채용 공고 섹션 생성
    timestamp = datetime.now().strftime('%Y년 %m월 %d일 %H:%M')
    
    jobs_section = f"""
## 📋 최신 채용 공고 (마지막 업데이트: {timestamp})

**검색 키워드**: {', '.join(keywords)}  
**지역**: {location}  
**총 {len(jobs)}개의 채용 공고**

### 상위 10개 채용 공고

"""
    
    for idx, job in enumerate(jobs[:10], 1):
        jobs_section += f"""
{idx}. **{job.title}** - {job.company}
   - 📍 {job.location or '위치 정보 없음'}
   - 🔗 [자세히 보기]({job.url})
   - 출처: {job.source}
   
"""
    
    if len(jobs) > 10:
        jobs_section += f"\n*그 외 {len(jobs) - 10}개의 채용 공고가 더 있습니다. [전체 목록 보기](jobs/latest.json)*\n"
    
    # 기존 최신 채용 공고 섹션 찾아서 교체
    import re
    pattern = r'## 📋 최신 채용 공고.*?(?=\n## |\Z)'
    
    if re.search(pattern, readme_content, re.DOTALL):
        readme_content = re.sub(pattern, jobs_section.strip(), readme_content, flags=re.DOTALL)
    else:
        # 섹션이 없으면 설치 및 실행 섹션 앞에 추가
        install_pattern = r'(## 설치 및 실행)'
        if re.search(install_pattern, readme_content):
            readme_content = re.sub(
                install_pattern,
                jobs_section.strip() + '\n\n' + r'\1',
                readme_content
            )
        else:
            # 끝에 추가
            readme_content += '\n\n' + jobs_section
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("📝 README 업데이트 완료")

if __name__ == '__main__':
    main()

