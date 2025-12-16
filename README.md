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

