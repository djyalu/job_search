# Job Search & Resume Matching Service

LinkedIn과 Indeed에서 채용 공고를 검색하고, 이력서를 업로드하여 적합도를 분석해주는 서비스입니다.

## 주요 기능

- 🔍 **채용 공고 검색**: LinkedIn과 Indeed에서 키워드로 채용 공고 검색
- 📄 **이력서 업로드**: PDF 또는 텍스트 형식의 이력서 업로드
- 🎯 **적합도 분석**: 이력서와 채용 공고의 적합도를 AI 기반으로 분석
- 📊 **결과 시각화**: 검색 결과 및 적합도 점수를 시각적으로 표시
- 🤖 **자동 업데이트**: GitHub Actions를 통한 하루 2회 자동 채용 공고 수집

## 기술 스택

- **Backend**: FastAPI (Python)
- **Frontend**: React + TypeScript
- **AI/ML**: OpenAI API 또는 Hugging Face 모델
- **Database**: SQLite (개발) / PostgreSQL (프로덕션)
- **Web Scraping**: Selenium / BeautifulSoup

## 설치 및 실행

### 백엔드 설정

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn app.main:app --reload
```

### 프론트엔드 설정

```bash
cd frontend
npm install
npm start
```

## 환경 변수

`.env` 파일을 생성하고 다음 변수들을 설정하세요:

```
OPENAI_API_KEY=your_openai_api_key
LINKEDIN_EMAIL=your_linkedin_email
LINKEDIN_PASSWORD=your_linkedin_password
```

## GitHub Actions 자동 업데이트

이 프로젝트는 GitHub Actions를 사용하여 하루에 2번(오전 9시, 오후 9시) 자동으로 최신 채용 공고를 수집합니다.

### 설정 방법

1. **GitHub Secrets 설정** (선택사항)
   - Repository Settings → Secrets and variables → Actions
   - `SEARCH_KEYWORDS`: 검색할 키워드 (쉼표로 구분, 예: `Python Developer,Software Engineer`)
   - `SEARCH_LOCATION`: 검색 지역 (예: `Seoul, South Korea`)

2. **자동 실행**
   - 워크플로우는 매일 자동으로 실행됩니다
   - 수동 실행: Actions 탭 → "Daily Job Search" → "Run workflow"

3. **결과 확인**
   - `jobs/` 디렉토리에 JSON 파일로 저장됩니다
   - `jobs/latest.json`: 최신 검색 결과
   - README.md에 상위 10개 채용 공고가 자동 업데이트됩니다

자세한 테스트 방법은 [TESTING.md](TESTING.md)를 참조하세요.

**📋 결과 확인 가이드**: 채용 공고 수집 결과를 확인하는 상세한 방법은 [HOW_TO_VIEW_RESULTS.md](HOW_TO_VIEW_RESULTS.md)를 참조하세요.

### 결과 확인 방법

채용 공고 수집 결과는 다음 방법으로 확인할 수 있습니다:

#### 1. GitHub 저장소에서 직접 확인

**방법 A: README.md 확인**
- 저장소 메인 페이지의 README.md 파일을 확인하세요
- "📋 최신 채용 공고" 섹션에 상위 10개 채용 공고가 자동으로 표시됩니다
- 마지막 업데이트 시간도 함께 표시됩니다

**방법 B: JSON 파일 확인**
1. 저장소의 `jobs/` 디렉토리로 이동
2. `latest.json` 파일 클릭하여 최신 결과 확인
3. 또는 `jobs_YYYYMMDD_HHMMSS.json` 형식의 타임스탬프별 파일 확인

**방법 C: GitHub Actions 로그 확인**
1. **Actions** 탭 클릭
2. 최근 실행된 "Daily Job Search" 워크플로우 선택
3. "Run job search" 단계를 클릭하여 실행 로그 확인
4. 수집된 채용 공고 개수와 키워드 정보 확인

#### 2. 로컬에서 확인

```bash
# 저장소 클론
git clone https://github.com/djyalu/job_search.git
cd job_search

# 최신 결과 확인
cat jobs/latest.json

# 또는 Python으로 읽기
python -c "import json; data = json.load(open('jobs/latest.json', encoding='utf-8')); print(f'총 {data[\"total\"]}개의 채용 공고'); [print(f'{i+1}. {job[\"title\"]} - {job[\"company\"]}') for i, job in enumerate(data['jobs'][:10])]"
```

#### 3. JSON 파일 구조

`jobs/latest.json` 파일 구조:
```json
{
  "timestamp": "2025-01-XX 09:00:00",
  "total": 25,
  "keywords": ["Python Developer", "Software Engineer"],
  "location": "Seoul, South Korea",
  "jobs": [
    {
      "id": "linkedin_0",
      "title": "Senior Python Developer",
      "company": "Tech Company",
      "location": "Seoul",
      "description": "...",
      "url": "https://...",
      "source": "linkedin",
      "posted_date": "2025-01-XX..."
    }
  ]
}
```

#### 4. 커밋 히스토리 확인

매 실행마다 결과가 자동으로 커밋되므로:
1. 저장소의 **Commits** 탭에서 최근 커밋 확인
2. 커밋 메시지: "Auto update: Latest job postings YYYY-MM-DD HH:MM"
3. 커밋 상세에서 변경된 파일 확인

## 프로젝트 구조

```
job_search/
├── .github/
│   └── workflows/
│       └── job-search.yml   # GitHub Actions 워크플로우
├── app/
│   ├── main.py              # FastAPI 메인 애플리케이션
│   ├── models/              # 데이터 모델
│   ├── services/            # 비즈니스 로직
│   │   ├── job_search.py    # 채용 공고 검색 서비스
│   │   ├── resume_parser.py # 이력서 파싱 서비스
│   │   └── matching.py      # 적합도 분석 서비스
│   ├── api/                 # API 엔드포인트
│   └── utils/               # 유틸리티 함수
├── frontend/                # React 프론트엔드
├── scripts/
│   └── daily_job_search.py  # 일일 채용 공고 검색 스크립트
├── jobs/                    # 수집된 채용 공고 (JSON)
├── uploads/                 # 업로드된 이력서 저장
└── requirements.txt         # Python 의존성
```

## 라이선스

MIT

