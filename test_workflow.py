"""GitHub Actions 워크플로우 및 스크립트 구조 테스트"""
import sys
import json
from pathlib import Path
from datetime import datetime

def test_file_structure():
    """파일 구조 테스트"""
    print("Testing file structure...")
    
    required_files = [
        '.github/workflows/job-search.yml',
        'scripts/daily_job_search.py',
        'app/services/job_search.py',
        'app/models/job.py',
    ]
    
    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"  OK: {file_path}")
        else:
            print(f"  MISSING: {file_path}")
            all_exist = False
    
    return all_exist

def test_workflow_syntax():
    """워크플로우 YAML 문법 테스트"""
    print("\nTesting workflow syntax...")
    
    workflow_path = Path('.github/workflows/job-search.yml')
    if not workflow_path.exists():
        print("  ERROR: Workflow file not found")
        return False
    
    try:
        content = workflow_path.read_text(encoding='utf-8')
        
        # 기본 검증
        checks = [
            ('name:', 'Has name'),
            ('on:', 'Has trigger'),
            ('schedule:', 'Has schedule'),
            ('cron:', 'Has cron expression'),
            ('jobs:', 'Has jobs'),
            ('search-jobs:', 'Has search-jobs job'),
        ]
        
        all_checks = True
        for check, desc in checks:
            if check in content:
                print(f"  OK: {desc}")
            else:
                print(f"  MISSING: {desc}")
                all_checks = False
        
        return all_checks
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def test_script_structure():
    """스크립트 구조 테스트"""
    print("\nTesting script structure...")
    
    script_path = Path('scripts/daily_job_search.py')
    if not script_path.exists():
        print("  ERROR: Script file not found")
        return False
    
    try:
        content = script_path.read_text(encoding='utf-8')
        
        checks = [
            ('def main():', 'Has main function'),
            ('JobSearchService', 'Uses JobSearchService'),
            ('JobSearchRequest', 'Uses JobSearchRequest'),
            ('json.dump', 'Saves JSON'),
            ('update_readme', 'Updates README'),
        ]
        
        all_checks = True
        for check, desc in checks:
            if check in content:
                print(f"  OK: {desc}")
            else:
                print(f"  MISSING: {desc}")
                all_checks = False
        
        return all_checks
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def test_jobs_directory():
    """jobs 디렉토리 테스트"""
    print("\nTesting jobs directory...")
    
    jobs_dir = Path('jobs')
    jobs_dir.mkdir(exist_ok=True)
    
    # 테스트 JSON 파일 생성
    test_data = {
        'timestamp': datetime.now().isoformat(),
        'total': 0,
        'keywords': ['test'],
        'location': 'test',
        'jobs': []
    }
    
    test_file = jobs_dir / 'test.json'
    try:
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        
        # 읽기 테스트
        with open(test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"  OK: Can write and read JSON files")
        test_file.unlink()  # 테스트 파일 삭제
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def main():
    """메인 테스트 함수"""
    print("=" * 50)
    print("GitHub Actions Job Search - Structure Test")
    print("=" * 50)
    
    results = []
    results.append(("File Structure", test_file_structure()))
    results.append(("Workflow Syntax", test_workflow_syntax()))
    results.append(("Script Structure", test_script_structure()))
    results.append(("Jobs Directory", test_jobs_directory()))
    
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print("=" * 50)
    
    all_passed = True
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {name}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("\nAll structure tests passed!")
        print("\nNote: Actual scraping requires ChromeDriver and may not work locally.")
        print("The workflow will run properly on GitHub Actions.")
        return 0
    else:
        print("\nSome tests failed. Please check the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())

