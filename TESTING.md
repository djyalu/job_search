# 테스트 가이드

## 로컬 테스트

### 1. 구조 테스트
프로젝트의 파일 구조와 워크플로우 구문을 테스트합니다:

```bash
python test_workflow.py
```

이 테스트는 다음을 확인합니다:
- 필수 파일 존재 여부
- GitHub Actions 워크플로우 구문
- 스크립트 구조
- JSON 파일 읽기/쓰기

### 2. 실제 채용 공고 검색 테스트 (선택사항)

로컬에서 실제 스크래핑을 테스트하려면:

1. **ChromeDriver 설치**
   - ChromeDriver 다운로드: https://chromedriver.chromium.org/
   - PATH에 추가하거나 프로젝트 루트에 배치

2. **환경 변수 설정** (선택사항)
   ```bash
   set SEARCH_KEYWORDS=Python Developer,Software Engineer
   set SEARCH_LOCATION=Seoul, South Korea
   ```

3. **스크립트 실행**
   ```bash
   python scripts/daily_job_search.py
   ```

**참고**: 로컬에서 스크래핑은 시간이 오래 걸릴 수 있으며, LinkedIn/Indeed의 봇 차단에 걸릴 수 있습니다.

## GitHub Actions 테스트

### 1. 워크플로우 수동 실행

1. GitHub 저장소의 **Actions** 탭으로 이동
2. **Daily Job Search** 워크플로우 선택
3. **Run workflow** 버튼 클릭
4. 실행 상태 확인

### 2. 스케줄 확인

워크플로우는 다음 시간에 자동 실행됩니다:
- 한국 시간 오전 9시 (UTC 0시)
- 한국 시간 오후 9시 (UTC 12시)

### 3. 결과 확인

- `jobs/latest.json`: 최신 검색 결과
- `jobs/jobs_YYYYMMDD_HHMMSS.json`: 타임스탬프별 결과
- README.md: 상위 10개 채용 공고 자동 업데이트

## 문제 해결

### ChromeDriver 오류
- GitHub Actions에서는 자동으로 설치됩니다
- 로컬에서는 수동으로 설치해야 합니다

### Import 오류
```bash
pip install -r requirements.txt
```

### 스크래핑 실패
- LinkedIn/Indeed는 봇 차단을 할 수 있습니다
- GitHub Actions에서는 더 안정적으로 작동합니다
- 실제 사용 시에는 API를 사용하는 것을 권장합니다

## 다음 단계

1. 코드를 GitHub에 푸시
2. Actions 탭에서 워크플로우 확인
3. 첫 실행 후 결과 확인
4. 필요시 GitHub Secrets에 검색 키워드 설정

