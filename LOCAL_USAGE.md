# 로컬 사용 가이드

로컬 컴퓨터에서 채용 공고를 수집하고 확인하는 방법을 안내합니다.

## 🚀 빠른 시작

### 1단계: 채용 공고 수집

```bash
python scripts/run_local.py
```

실행하면 다음과 같이 진행됩니다:
1. 검색 키워드 입력 요청 (Enter 시 기본값 사용)
2. 검색 지역 입력 요청 (Enter 시 기본값 사용)
3. LinkedIn과 Indeed에서 채용 공고 검색
4. 결과를 `jobs/latest.json`에 저장

### 2단계: 결과 확인

**방법 A: 콘솔 출력 (간단)**
```bash
python scripts/view_results.py
```

출력 내용:
- 수집 시간, 키워드, 지역, 총 개수
- 출처별 통계 (LinkedIn, Indeed)
- 상위 10개 회사
- 채용 공고 목록 (최대 20개)

**방법 B: HTML 뷰어 (추천)**
```bash
python scripts/view_results.py --html
```

생성된 `jobs/viewer.html` 파일을 브라우저에서 열면:
- 깔끔한 카드 형식으로 채용 공고 표시
- 출처별 필터링 (전체/LinkedIn/Indeed)
- 각 채용 공고의 상세 정보 확인
- 링크 클릭으로 원본 페이지 이동

## 📋 상세 사용법

### 환경 변수로 설정하기

Windows (PowerShell):
```powershell
$env:SEARCH_KEYWORDS = "Python Developer,Software Engineer,Data Scientist"
$env:SEARCH_LOCATION = "Seoul, South Korea"
python scripts/daily_job_search.py
```

Windows (CMD):
```cmd
set SEARCH_KEYWORDS=Python Developer,Software Engineer
set SEARCH_LOCATION=Seoul, South Korea
python scripts/daily_job_search.py
```

Linux/Mac:
```bash
export SEARCH_KEYWORDS="Python Developer,Software Engineer"
export SEARCH_LOCATION="Seoul, South Korea"
python scripts/daily_job_search.py
```

### 결과 파일 구조

```
jobs/
├── latest.json              # 항상 최신 결과
├── jobs_20250115_090000.json  # 타임스탬프별 결과
├── jobs_20250115_210000.json
└── viewer.html              # HTML 뷰어 (생성 시)
```

### JSON 파일 직접 확인

Python으로 읽기:
```python
import json

with open('jobs/latest.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"총 {data['total']}개의 채용 공고")
for job in data['jobs'][:5]:
    print(f"- {job['title']} @ {job['company']}")
```

jq로 읽기 (Linux/Mac):
```bash
# 총 개수
jq '.total' jobs/latest.json

# 첫 번째 채용 공고
jq '.jobs[0]' jobs/latest.json

# 제목만 추출
jq '.jobs[].title' jobs/latest.json
```

## 🎨 HTML 뷰어 사용법

### 생성

```bash
python scripts/view_results.py --html
```

### 열기

**Windows:**
```bash
start jobs/viewer.html
# 또는
jobs/viewer.html
```

**Linux:**
```bash
xdg-open jobs/viewer.html
```

**Mac:**
```bash
open jobs/viewer.html
```

### 기능

- **필터링**: 상단 버튼으로 출처별 필터링
  - 전체: 모든 채용 공고 표시
  - LinkedIn: LinkedIn 채용 공고만
  - Indeed: Indeed 채용 공고만

- **카드 정보**: 각 카드에 다음 정보 표시
  - 제목
  - 회사명
  - 위치
  - 출처
  - 설명 (일부)
  - 원본 링크

## 🔧 고급 사용법

### 여러 키워드로 검색

```bash
python scripts/run_local.py
# 키워드 입력: Python Developer,Software Engineer,Data Scientist,Backend Developer
```

### 특정 지역으로 검색

```bash
python scripts/run_local.py
# 지역 입력: San Francisco, CA
```

### 스크립트 직접 실행

```python
# scripts/daily_job_search.py 직접 실행
import os
os.environ['SEARCH_KEYWORDS'] = 'Python Developer'
os.environ['SEARCH_LOCATION'] = 'Seoul, South Korea'

from scripts.daily_job_search import main
main()
```

## 📊 결과 분석

### 통계 확인

`view_results.py`를 실행하면 자동으로 다음 통계를 보여줍니다:
- 출처별 채용 공고 개수
- 상위 10개 회사

### 커스텀 분석 스크립트

```python
import json
from collections import Counter

with open('jobs/latest.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 기술 스택 키워드 분석
tech_keywords = ['Python', 'JavaScript', 'React', 'AWS', 'Docker']
for keyword in tech_keywords:
    count = sum(1 for job in data['jobs'] 
                if keyword.lower() in job['description'].lower())
    print(f"{keyword}: {count}개")

# 급여 정보가 있는 채용 공고
with_salary = [job for job in data['jobs'] if job.get('salary')]
print(f"\n급여 정보가 있는 채용 공고: {len(with_salary)}개")
```

## ⚠️ 주의사항

### ChromeDriver 필요

로컬에서 실행하려면 ChromeDriver가 필요합니다:
1. Chrome 브라우저 버전 확인
2. 해당 버전의 ChromeDriver 다운로드: https://chromedriver.chromium.org/
3. PATH에 추가하거나 프로젝트 루트에 배치

### 스크래핑 제한

- LinkedIn과 Indeed는 봇 차단을 할 수 있습니다
- 너무 자주 실행하면 IP가 차단될 수 있습니다
- 실제 사용 시에는 공식 API 사용을 권장합니다

### 실행 시간

- 검색 키워드 수에 따라 5-15분 정도 소요될 수 있습니다
- 네트워크 상태에 따라 더 오래 걸릴 수 있습니다

## 💡 팁

1. **정기 실행**: 스케줄러(cron, Task Scheduler)로 자동 실행 설정
2. **결과 비교**: 타임스탬프별 파일로 시간에 따른 변화 추적
3. **필터링**: JSON 파일을 다운로드하여 원하는 조건으로 필터링
4. **알림 설정**: 스크립트 실행 후 이메일/슬랙 알림 추가 가능

## 🐛 문제 해결

### "ChromeDriver를 찾을 수 없습니다" 오류

- ChromeDriver가 PATH에 있는지 확인
- 또는 프로젝트 루트에 chromedriver.exe 배치

### "검색 결과가 없습니다"

- 네트워크 연결 확인
- 키워드나 지역을 변경해보기
- LinkedIn/Indeed 사이트 접근 가능한지 확인

### "Import 오류"

```bash
pip install -r requirements.txt
```

### HTML 뷰어가 열리지 않음

- 파일 경로 확인: `jobs/viewer.html`
- 브라우저에서 직접 파일 열기
- 파일 인코딩이 UTF-8인지 확인

