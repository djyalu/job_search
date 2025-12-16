# 이력서 적합도 분석 가이드

로컬에 업로드한 이력서와 수집된 채용 공고를 비교하여 적합도를 분석하는 방법을 안내합니다.

## 🚀 빠른 시작

### 1단계: 채용 공고 수집

먼저 비교할 채용 공고를 수집해야 합니다:

```bash
python scripts/run_local.py
```

또는 이미 수집된 결과가 있다면 `jobs/latest.json` 파일을 사용할 수 있습니다.

### 2단계: 이력서 비교

**인터랙티브 모드 (가장 간단):**
```bash
python scripts/compare_interactive.py
```

실행하면 다음을 입력하라는 프롬프트가 나타납니다:
1. 이력서 파일 경로
2. 채용 공고 파일 경로 (Enter 시 최신 결과 사용)
3. 표시할 상위 결과 개수
4. HTML 리포트 생성 여부

## 📋 사용 방법

### 인터랙티브 모드

```bash
python scripts/compare_interactive.py
```

**예시:**
```
이력서 파일 경로를 입력하세요:
> C:\Users\YourName\Documents\resume.pdf

채용 공고 파일 경로를 입력하세요 (Enter 시 최신 결과 사용):
> 

표시할 상위 결과 개수를 입력하세요 (Enter 시 10개):
> 15

HTML 리포트를 생성하시겠습니까? (y/n, Enter 시 n):
> y
```

### 명령줄 모드

```bash
# 기본 사용 (최신 채용 공고와 비교)
python scripts/compare_resume.py "resume.pdf"

# 특정 채용 공고 파일과 비교
python scripts/compare_resume.py "resume.pdf" --jobs jobs/jobs_20250115_090000.json

# 상위 20개 결과만 표시
python scripts/compare_resume.py "resume.pdf" --top 20

# HTML 리포트 생성
python scripts/compare_resume.py "resume.pdf" --html

# HTML 리포트 저장 경로 지정
python scripts/compare_resume.py "resume.pdf" --html --output my_report.html
```

### 옵션 설명

- `resume`: 이력서 파일 경로 (필수)
  - 지원 형식: PDF, DOCX, TXT
- `--jobs`: 채용 공고 JSON 파일 경로 (선택)
  - 기본값: `jobs/latest.json`
- `--top`: 표시할 상위 결과 개수 (선택)
  - 기본값: 10개
- `--html`: HTML 리포트 생성 (선택)
- `--output`: HTML 리포트 저장 경로 (선택)
  - 기본값: `jobs/resume_comparison.html`

## 📊 분석 결과

### 콘솔 출력

비교 분석 결과는 다음과 같은 정보를 포함합니다:

1. **전체 적합도 점수** (0-100%)
   - 높을수록 이력서가 채용 공고에 적합함

2. **세부 점수**
   - 스킬 매칭: 이력서의 기술 스킬이 채용 공고 요구사항과 얼마나 일치하는지
   - 경력 매칭: 경력 수준이 채용 공고 요구사항과 맞는지
   - 학력 매칭: 학력 요구사항 충족 여부
   - 설명 매칭: 채용 공고 설명과 이력서 내용의 키워드 일치도

3. **매칭된 키워드**
   - 채용 공고와 이력서에서 공통으로 발견된 키워드

4. **누락된 키워드**
   - 채용 공고에 있지만 이력서에 없는 중요한 키워드

5. **추천사항**
   - 이력서를 개선하기 위한 구체적인 제안

### HTML 리포트

HTML 리포트는 브라우저에서 보기 좋게 표시됩니다:

- **이력서 정보**: 이름, 이메일, 스킬 등
- **채용 공고 카드**: 각 채용 공고별로 카드 형식으로 표시
- **시각적 점수**: 원형 차트로 전체 적합도 표시
- **색상 코딩**: 
  - 초록색 (70% 이상): 높은 적합도
  - 주황색 (50-70%): 보통 적합도
  - 빨간색 (50% 미만): 낮은 적합도
- **키워드 태그**: 매칭/누락된 키워드를 태그로 표시
- **추천사항**: 개선 제안을 박스로 강조

## 💡 활용 팁

### 1. 여러 이력서 버전 비교

```bash
# 버전 1
python scripts/compare_resume.py "resume_v1.pdf" --html --output report_v1.html

# 버전 2 (개선 후)
python scripts/compare_resume.py "resume_v2.pdf" --html --output report_v2.html
```

### 2. 특정 회사/직무에 맞춘 분석

```bash
# 특정 날짜의 채용 공고와 비교
python scripts/compare_resume.py "resume.pdf" --jobs jobs/jobs_20250115_090000.json
```

### 3. 상위 결과만 빠르게 확인

```bash
# 상위 5개만 확인
python scripts/compare_resume.py "resume.pdf" --top 5
```

### 4. 배치 분석

여러 이력서를 한 번에 분석하려면 스크립트를 작성:

```python
import subprocess
from pathlib import Path

resumes = ["resume1.pdf", "resume2.pdf", "resume3.pdf"]

for resume in resumes:
    if Path(resume).exists():
        subprocess.run([
            "python", "scripts/compare_resume.py",
            resume,
            "--html",
            "--output", f"report_{Path(resume).stem}.html"
        ])
```

## 📈 결과 해석

### 점수 의미

- **90-100%**: 매우 높은 적합도, 지원 추천
- **70-89%**: 높은 적합도, 지원 가능
- **50-69%**: 보통 적합도, 이력서 개선 후 지원 권장
- **0-49%**: 낮은 적합도, 이력서 대폭 개선 필요

### 개선 전략

1. **누락된 키워드 추가**
   - 채용 공고에 자주 언급되는 기술이나 경험을 이력서에 추가

2. **스킬 섹션 강화**
   - 채용 공고에서 요구하는 기술 스킬을 명시적으로 나열

3. **경력 설명 개선**
   - 채용 공고의 요구사항과 관련된 경력을 강조

4. **요약 섹션 추가**
   - 채용 공고와의 연관성을 명확히 하는 요약 작성

## ⚠️ 주의사항

### 파일 형식

- **지원 형식**: PDF, DOCX, TXT
- **인코딩**: TXT 파일은 UTF-8 인코딩 권장
- **파일 크기**: 너무 큰 파일은 파싱 시간이 오래 걸릴 수 있습니다

### 정확도

- 자동 파싱은 완벽하지 않을 수 있습니다
- 특히 복잡한 레이아웃의 PDF는 정보 추출이 부정확할 수 있습니다
- 중요한 분석은 수동으로 검토하는 것을 권장합니다

### 성능

- 많은 채용 공고와 비교할 경우 시간이 오래 걸릴 수 있습니다
- 상위 결과만 확인하려면 `--top` 옵션 사용

## 🐛 문제 해결

### "이력서 파일을 찾을 수 없습니다"

- 파일 경로가 정확한지 확인
- 상대 경로 사용 시 현재 디렉토리 확인
- 파일 경로에 공백이 있으면 따옴표로 감싸기

### "채용 공고 파일을 찾을 수 없습니다"

- 먼저 채용 공고를 수집: `python scripts/run_local.py`
- 또는 `--jobs` 옵션으로 올바른 파일 경로 지정

### "이력서 파싱 오류"

- 파일 형식이 지원되는지 확인 (PDF, DOCX, TXT)
- 파일이 손상되지 않았는지 확인
- 다른 형식으로 변환 후 재시도

### 점수가 모두 낮게 나옴

- 이력서에 기술 스킬이 충분히 명시되어 있는지 확인
- 채용 공고와 관련된 경력이 명확히 기술되어 있는지 확인
- 누락된 키워드를 이력서에 추가

## 📚 추가 리소스

- [로컬 사용 가이드](LOCAL_USAGE.md): 채용 공고 수집 방법
- [결과 확인 가이드](HOW_TO_VIEW_RESULTS.md): 수집 결과 확인 방법

