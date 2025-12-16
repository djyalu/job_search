"""
로컬에서 채용 공고 검색을 실행하는 간편 스크립트
"""
import os
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

def main():
    """로컬에서 채용 공고 검색 실행"""
    print("=" * 70)
    print("[JOB SEARCH] 로컬 채용 공고 검색")
    print("=" * 70)
    print()
    
    # 검색 키워드 입력
    print("검색 키워드를 입력하세요 (쉼표로 구분, Enter 시 기본값 사용):")
    keywords_input = input("> ").strip()
    keywords = keywords_input.split(',') if keywords_input else ['Python Developer', 'Software Engineer']
    keywords = [k.strip() for k in keywords if k.strip()]
    
    # 검색 지역 입력
    print("\n검색 지역을 입력하세요 (Enter 시 기본값 사용):")
    location_input = input("> ").strip()
    location = location_input if location_input else 'Seoul, South Korea'
    
    # 환경 변수 설정
    os.environ['SEARCH_KEYWORDS'] = ','.join(keywords)
    os.environ['SEARCH_LOCATION'] = location
    
    print(f"\n[SETTINGS] 검색 설정:")
    print(f"   키워드: {', '.join(keywords)}")
    print(f"   지역: {location}")
    print()
    
    # daily_job_search 스크립트 실행
    from scripts.daily_job_search import main as search_main
    
    try:
        search_main()
    except KeyboardInterrupt:
        print("\n\n[WARNING] 사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("[SUCCESS] 검색 완료!")
    print("=" * 70)
    print("\n[VIEW RESULTS] 결과 확인:")
    print("   1. 콘솔: python scripts/view_results.py")
    print("   2. HTML: python scripts/view_results.py --html")
    print("   3. 파일: jobs/latest.json")

if __name__ == '__main__':
    main()

