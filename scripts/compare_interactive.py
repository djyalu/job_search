"""
인터랙티브 모드로 이력서와 채용 공고를 비교하는 스크립트
"""
import sys
import io
from pathlib import Path

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except:
        pass

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.compare_resume import load_resume, load_jobs, compare_resume_with_jobs, display_comparison_results, save_comparison_report

def main():
    """인터랙티브 메인 함수"""
    print("=" * 70)
    print("[RESUME COMPARISON] 이력서 적합도 분석 (인터랙티브 모드)")
    print("=" * 70)
    print()
    
    # 이력서 파일 입력
    print("이력서 파일 경로를 입력하세요:")
    print("  (PDF, DOCX, TXT 파일 지원)")
    resume_path = input("> ").strip().strip('"').strip("'")
    
    if not resume_path:
        print("[ERROR] 이력서 파일 경로를 입력해주세요.")
        sys.exit(1)
    
    # 채용 공고 파일 입력 (선택사항)
    print("\n채용 공고 파일 경로를 입력하세요 (Enter 시 최신 결과 사용):")
    jobs_path = input("> ").strip().strip('"').strip("'")
    if not jobs_path:
        jobs_path = None
    
    # 상위 N개 결과
    print("\n표시할 상위 결과 개수를 입력하세요 (Enter 시 10개):")
    top_input = input("> ").strip()
    top_n = int(top_input) if top_input.isdigit() else 10
    
    # HTML 리포트 생성 여부
    print("\nHTML 리포트를 생성하시겠습니까? (y/n, Enter 시 n):")
    html_input = input("> ").strip().lower()
    create_html = html_input in ['y', 'yes', '예', 'ㅇ']
    
    print("\n" + "=" * 70)
    print("[PROCESSING] 분석 시작...")
    print("=" * 70)
    
    # 이력서 로드
    resume_data = load_resume(resume_path)
    if not resume_data:
        sys.exit(1)
    
    # 채용 공고 로드
    jobs = load_jobs(jobs_path)
    if not jobs:
        sys.exit(1)
    
    # 비교 분석
    results = compare_resume_with_jobs(resume_data, jobs, top_n)
    
    # 결과 출력
    display_comparison_results(resume_data, results)
    
    # HTML 리포트 생성
    if create_html:
        html_file = save_comparison_report(resume_data, results)
        print(f"\n[SUCCESS] HTML 리포트 생성 완료: {html_file}")
        print(f"   브라우저에서 열어서 확인하세요!")
    
    print("\n" + "=" * 70)
    print("[COMPLETE] 분석 완료!")
    print("=" * 70)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[WARNING] 사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

