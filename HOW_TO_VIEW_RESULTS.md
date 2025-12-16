# 채용 공고 수집 결과 확인 가이드

GitHub Actions로 자동 수집된 채용 공고 결과를 확인하는 다양한 방법을 안내합니다.

## 🚀 빠른 확인 방법

### 1. README.md에서 확인 (가장 간단)

1. GitHub 저장소 메인 페이지로 이동: https://github.com/djyalu/job_search
2. README.md 파일을 스크롤하여 **"📋 최신 채용 공고"** 섹션 확인
3. 상위 10개 채용 공고가 자동으로 표시됩니다
4. 각 채용 공고의 제목, 회사명, 위치, 링크를 확인할 수 있습니다

**장점**: 별도 클릭 없이 바로 확인 가능

---

### 2. JSON 파일에서 확인 (상세 정보)

1. 저장소에서 **`jobs/`** 디렉토리 클릭
2. **`latest.json`** 파일 클릭
3. "Raw" 버튼을 클릭하여 원본 JSON 확인
4. 또는 GitHub에서 직접 JSON 형식으로 확인

**장점**: 모든 채용 공고의 상세 정보 확인 가능

---

### 3. GitHub Actions 로그 확인 (실행 상태)

1. 저장소의 **Actions** 탭 클릭
2. 왼쪽 사이드바에서 **"Daily Job Search"** 워크플로우 선택
3. 최근 실행된 워크플로우 클릭
4. **"Run job search"** 단계를 펼쳐서 로그 확인

**로그에서 확인할 수 있는 정보:**
- 검색 키워드
- 수집된 채용 공고 개수
- 오류 발생 여부
- 실행 시간

**장점**: 실행 과정과 문제 발생 시 디버깅 가능

---

## 📂 파일 구조 이해하기

### jobs/ 디렉토리 구조

```
jobs/
├── latest.json                    # 항상 최신 결과
├── jobs_20250115_090000.json      # 오전 9시 수집 결과
├── jobs_20250115_210000.json      # 오후 9시 수집 결과
└── jobs_20250116_090000.json      # 다음날 오전 9시 수집 결과
```

- **latest.json**: 항상 최신 수집 결과를 가리킵니다
- **jobs_YYYYMMDD_HHMMSS.json**: 특정 시간에 수집된 결과를 보관합니다

---

## 💻 로컬에서 확인하기

### 저장소 클론

```bash
git clone https://github.com/djyalu/job_search.git
cd job_search
```

### JSON 파일 읽기

**방법 1: cat 명령어 (간단)**
```bash
# Windows (PowerShell)
Get-Content jobs/latest.json

# Linux/Mac
cat jobs/latest.json
```

**방법 2: Python 스크립트 (구조화된 출력)**
```bash
python -c "
import json
with open('jobs/latest.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    
print(f'📊 수집 시간: {data[\"timestamp\"]}')
print(f'🔍 검색 키워드: {\", \".join(data[\"keywords\"])}')
print(f'📍 검색 지역: {data[\"location\"]}')
print(f'📋 총 {data[\"total\"]}개의 채용 공고\n')

print('=' * 60)
for i, job in enumerate(data['jobs'][:10], 1):
    print(f'{i}. {job[\"title\"]}')
    print(f'   회사: {job[\"company\"]}')
    print(f'   위치: {job.get(\"location\", \"정보 없음\")}')
    print(f'   출처: {job[\"source\"]}')
    print(f'   링크: {job[\"url\"]}')
    print()
"
```

**방법 3: jq 사용 (JSON 파서)**
```bash
# jq 설치 필요: https://stedolan.github.io/jq/download/
jq '.total' jobs/latest.json  # 총 개수
jq '.jobs[0]' jobs/latest.json  # 첫 번째 채용 공고
jq '.jobs[] | {title, company, location}' jobs/latest.json  # 요약 정보
```

---

## 📊 결과 데이터 구조

### JSON 파일 예시

```json
{
  "timestamp": "2025-01-15T09:00:00",
  "total": 25,
  "keywords": ["Python Developer", "Software Engineer"],
  "location": "Seoul, South Korea",
  "jobs": [
    {
      "id": "linkedin_0",
      "title": "Senior Python Developer",
      "company": "Tech Company Inc.",
      "location": "Seoul, South Korea",
      "description": "We are looking for an experienced Python developer...",
      "url": "https://www.linkedin.com/jobs/view/123456",
      "source": "linkedin",
      "posted_date": "2025-01-15T08:30:00",
      "salary": null,
      "job_type": null
    }
  ]
}
```

### 각 필드 설명

- **timestamp**: 수집 시간 (ISO 8601 형식)
- **total**: 수집된 총 채용 공고 개수
- **keywords**: 검색에 사용된 키워드 목록
- **location**: 검색 지역
- **jobs**: 채용 공고 배열
  - **id**: 고유 식별자
  - **title**: 채용 공고 제목
  - **company**: 회사명
  - **location**: 근무지
  - **description**: 채용 공고 설명
  - **url**: 원본 링크
  - **source**: 출처 (linkedin 또는 indeed)
  - **posted_date**: 게시일
  - **salary**: 급여 정보 (있는 경우)
  - **job_type**: 고용 형태 (있는 경우)

---

## 🔔 알림 설정 (선택사항)

### GitHub 알림 설정

1. 저장소 우측 상단의 **Watch** 버튼 클릭
2. **Custom** 선택
3. **Actions** 체크박스 선택
4. 워크플로우 실행 시 이메일 알림 받기

### 커밋 알림

- 매 실행마다 자동 커밋이 생성되므로 커밋 알림을 받을 수 있습니다

---

## ❓ 문제 해결

### 결과가 없는 경우

1. **Actions 탭 확인**: 워크플로우가 실행되었는지 확인
2. **로그 확인**: 오류 메시지가 있는지 확인
3. **스케줄 확인**: 아직 실행 시간이 되지 않았을 수 있습니다

### JSON 파일이 보이지 않는 경우

1. **최신 커밋 확인**: 워크플로우가 완료되어 커밋되었는지 확인
2. **브랜치 확인**: 올바른 브랜치(main)에 있는지 확인
3. **권한 확인**: 저장소 접근 권한이 있는지 확인

### 데이터가 오래된 경우

- 워크플로우는 하루에 2번만 실행됩니다
- 수동 실행: Actions 탭 → "Run workflow"

---

## 📈 통계 확인

### 수집된 채용 공고 통계

Python 스크립트로 통계를 확인할 수 있습니다:

```python
import json
from collections import Counter
from datetime import datetime

with open('jobs/latest.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"📊 수집 통계")
print(f"총 채용 공고: {data['total']}개")
print(f"수집 시간: {data['timestamp']}")

# 출처별 통계
sources = Counter(job['source'] for job in data['jobs'])
print(f"\n출처별 통계:")
for source, count in sources.items():
    print(f"  {source}: {count}개")

# 회사별 통계 (상위 5개)
companies = Counter(job['company'] for job in data['jobs'])
print(f"\n상위 5개 회사:")
for company, count in companies.most_common(5):
    print(f"  {company}: {count}개")
```

---

## 💡 팁

1. **정기적으로 확인**: 하루 2번 업데이트되므로 매일 확인하세요
2. **필터링**: JSON 파일을 다운로드하여 원하는 조건으로 필터링 가능
3. **알림 설정**: GitHub 알림을 설정하여 자동으로 업데이트를 받으세요
4. **히스토리**: 과거 수집 결과도 `jobs_*.json` 파일로 확인 가능

