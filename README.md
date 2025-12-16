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

## 🌐 웹 UI 사용 (추천)

로컬에서 웹 브라우저를 통해 모든 기능을 사용할 수 있습니다.

### 웹 UI 시작

```bash
# 방법 1: 자동 시작 스크립트 (추천)
python scripts/start_ui.py

# 방법 2: 수동 시작
# 터미널 1: FastAPI 서버
uvicorn app.main:app --reload

# 터미널 2: React 프론트엔드
cd frontend
npm start
```

브라우저에서 `http://localhost:3006`으로 접속하세요.

### 웹 UI 기능

- **채용 공고 검색**: 키워드와 지역을 입력하여 검색
- **결과 확인**: 수집된 채용 공고 목록 및 상세 정보 확인
- **이력서 업로드**: PDF, DOCX, TXT 파일 업로드
- **이력서 비교**: 업로드한 이력서와 채용 공고 자동 비교 분석
- **HTML 리포트**: 비교 결과를 브라우저에서 바로 확인

## 로컬에서 채용 공고 수집 및 확인

### 빠른 시작

```bash
# 1. 채용 공고 수집 (인터랙티브 모드)
python scripts/run_local.py

# 2. 결과 확인 (콘솔)
python scripts/view_results.py

# 3. 결과 확인 (HTML 뷰어)
python scripts/view_results.py --html
# 생성된 jobs/viewer.html 파일을 브라우저에서 열기
```

### 상세 사용법

**채용 공고 수집:**
```bash
# 방법 1: 인터랙티브 모드 (추천)
python scripts/run_local.py
# 키워드와 지역을 입력하라는 프롬프트가 나타납니다

# 방법 2: 환경 변수 사용
set SEARCH_KEYWORDS=Python Developer,Software Engineer
set SEARCH_LOCATION=Seoul, South Korea
python scripts/daily_job_search.py
```

**결과 확인:**
```bash
# 콘솔에 요약 및 목록 출력
python scripts/view_results.py

# HTML 뷰어 생성 (브라우저에서 보기 좋게 확인)
python scripts/view_results.py --html
# jobs/viewer.html 파일이 생성됩니다
```

**결과 파일 위치:**
- `jobs/latest.json`: 최신 검색 결과
- `jobs/jobs_YYYYMMDD_HHMMSS.json`: 타임스탬프별 결과
- `jobs/viewer.html`: HTML 뷰어 (생성 시)

### 이력서와 채용 공고 비교 분석

**인터랙티브 모드 (추천):**
```bash
python scripts/compare_interactive.py
# 이력서 파일 경로, 채용 공고 파일, 결과 개수 등을 입력
```

**명령줄 모드:**
```bash
# 기본 사용
python scripts/compare_resume.py "path/to/resume.pdf"

# 옵션 지정
python scripts/compare_resume.py "resume.pdf" --jobs jobs/latest.json --top 20 --html

# HTML 리포트 생성
python scripts/compare_resume.py "resume.pdf" --html --output comparison_report.html
```

**비교 결과:**
- 전체 적합도 점수 (0-100%)
- 세부 점수: 스킬, 경력, 학력, 설명 매칭
- 매칭된 키워드 목록
- 누락된 키워드 목록
- 개선 추천사항
- HTML 리포트 생성 (선택사항)

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

**또는 웹 UI 자동 시작:**
```bash
python scripts/start_ui.py
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

**📋 가이드 문서**: 
- 로컬 사용: [LOCAL_USAGE.md](LOCAL_USAGE.md)
- 결과 확인: [HOW_TO_VIEW_RESULTS.md](HOW_TO_VIEW_RESULTS.md)
- 이력서 비교: [RESUME_COMPARISON.md](RESUME_COMPARISON.md)

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

