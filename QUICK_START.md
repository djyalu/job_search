# 빠른 시작 가이드

## 서버 실행 문제 해결 완료!

필요한 패키지가 모두 설치되었습니다. 이제 서버를 실행할 수 있습니다.

## 서버 시작 방법

### 방법 1: 배치 파일 사용 (Windows)

```bash
start_server.bat
```

또는 PowerShell:
```powershell
.\start_server.ps1
```

### 방법 2: 직접 실행

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8006
```

### 방법 3: 자동 시작 스크립트

```bash
python scripts/start_ui.py
```

## 접속 주소

- **API 서버**: http://localhost:8006
- **API 문서**: http://localhost:8006/docs
- **프론트엔드**: http://localhost:3006 (npm start 후)

## 프론트엔드 시작

```bash
cd frontend
npm install  # 처음 한 번만
npm start
```

## 설치된 패키지

- ✅ FastAPI
- ✅ Uvicorn
- ✅ Selenium
- ✅ BeautifulSoup4
- ✅ pdfplumber
- ✅ Pydantic (버전 호환성 해결)

## 문제 해결

만약 다른 오류가 발생하면:

1. **모듈을 찾을 수 없다는 오류**:
   ```bash
   pip install --user [패키지명]
   ```

2. **포트가 이미 사용 중**:
   - 다른 포트 사용: `--port 8007`
   - 또는 실행 중인 프로세스 종료

3. **권한 오류**:
   - `--user` 옵션 사용
   - 또는 관리자 권한으로 실행

