# 문제 해결 가이드

## 서버 상태 확인

### API 서버가 실행 중인지 확인

```bash
# 방법 1: 테스트 스크립트 실행
python test_server.py

# 방법 2: 직접 확인
python -c "import requests; r = requests.get('http://localhost:8006/health'); print(r.json())"
```

### 포트 확인

```bash
# Windows
netstat -ano | findstr :8006

# Linux/Mac
lsof -i :8006
```

## 일반적인 문제

### 1. "서버에 연결할 수 없습니다"

**원인**: 서버가 실행되지 않음

**해결**:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8006
```

또는:
```bash
start_server.bat
```

### 2. "포트가 이미 사용 중입니다"

**원인**: 다른 프로세스가 포트를 사용 중

**해결**:
```bash
# Windows: 프로세스 찾기
netstat -ano | findstr :8006

# 프로세스 종료 (PID는 위 명령어 결과에서 확인)
taskkill /PID [PID번호] /F

# 또는 다른 포트 사용
python -m uvicorn app.main:app --reload --port 8007
```

### 3. 프론트엔드가 로드되지 않음

**원인**: React 개발 서버가 실행되지 않음

**해결**:
```bash
cd frontend
npm install  # 처음 한 번만
npm start
```

### 4. "ModuleNotFoundError"

**원인**: 필요한 패키지가 설치되지 않음

**해결**:
```bash
pip install --user -r requirements.txt
```

### 5. CORS 오류

**원인**: 프론트엔드와 백엔드 포트가 다름

**해결**: `app/main.py`의 CORS 설정 확인:
```python
allow_origins=["http://localhost:3000", "http://localhost:3006", "http://localhost:5173"]
```

## 단계별 확인

### 1단계: API 서버 확인

```bash
# 서버 시작
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8006

# 다른 터미널에서 테스트
python test_server.py
```

예상 결과: 모든 테스트 통과

### 2단계: 브라우저에서 확인

1. http://localhost:8006 접속
2. http://localhost:8006/docs 접속 (API 문서)

예상 결과: 페이지가 정상적으로 로드됨

### 3단계: 프론트엔드 확인

```bash
cd frontend
npm start
```

예상 결과: http://localhost:3006 에서 앱이 실행됨

## 로그 확인

서버 실행 시 나타나는 오류 메시지를 확인하세요:

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8006
```

일반적인 오류:
- `ModuleNotFoundError`: 패키지 설치 필요
- `Address already in use`: 포트 충돌
- `ImportError`: 모듈 경로 문제

## 빠른 해결

모든 것을 처음부터 다시 시작:

```bash
# 1. 의존성 설치
pip install --user -r requirements.txt

# 2. 서버 시작 (터미널 1)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8006

# 3. 프론트엔드 시작 (터미널 2)
cd frontend
npm install
npm start
```

## 도움 요청

문제가 계속되면 다음 정보를 제공해주세요:

1. 오류 메시지 전체 내용
2. 실행한 명령어
3. `python test_server.py` 결과
4. 브라우저 콘솔 오류 (F12)

