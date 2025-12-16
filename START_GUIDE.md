# 시작 가이드

## ✅ 서버 상태

서버가 정상적으로 실행 중입니다!
- API 서버: http://localhost:8006 ✅
- 응답 확인: `{"message":"Job Search & Resume Matching API","version":"1.0.0"}`

## 🚀 웹 UI 사용하기

### 1단계: 프론트엔드 의존성 설치 및 시작

**Windows (배치 파일):**
```bash
start_frontend.bat
```

**또는 수동으로:**
```bash
cd frontend
npm install
npm start
```

### 2단계: 브라우저에서 접속

프론트엔드가 시작되면 자동으로 브라우저가 열립니다:
- **웹 UI**: http://localhost:3006

## 📋 전체 시작 순서

### 터미널 1: API 서버
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8006
```

또는:
```bash
start_server.bat
```

### 터미널 2: 프론트엔드
```bash
cd frontend
npm install  # 처음 한 번만
npm start
```

또는:
```bash
start_frontend.bat
```

## 🌐 접속 주소

- **웹 UI (프론트엔드)**: http://localhost:3006
- **API 서버**: http://localhost:8006
- **API 문서**: http://localhost:8006/docs
- **Health Check**: http://localhost:8006/health

## ✨ 웹 UI 기능

1. **채용 공고 검색**: 키워드와 지역 입력하여 검색
2. **결과 확인**: 수집된 채용 공고 목록 확인
3. **이력서 업로드**: PDF, DOCX, TXT 파일 업로드
4. **이력서 비교**: 업로드한 이력서와 채용 공고 비교 분석

## 🔧 문제 해결

### 프론트엔드가 시작되지 않음

1. **node_modules 없음**:
   ```bash
   cd frontend
   npm install
   ```

2. **포트 3006이 사용 중**:
   - 다른 포트 사용: `set PORT=3007 && npm start`
   - 또는 실행 중인 프로세스 종료

3. **npm이 설치되지 않음**:
   - Node.js 설치 필요: https://nodejs.org/

### API 연결 오류

- API 서버가 실행 중인지 확인: http://localhost:8006/health
- CORS 오류: `app/main.py`의 CORS 설정 확인

## 💡 팁

- API 서버와 프론트엔드는 별도의 터미널에서 실행해야 합니다
- 서버를 중지하려면 `Ctrl+C`를 누르세요
- 코드 변경 시 자동으로 재시작됩니다 (--reload 옵션)

