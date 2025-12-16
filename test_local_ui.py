"""
로컬 웹 UI 테스트 스크립트
"""
import requests
import time
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

API_BASE_URL = "http://localhost:8000"

def test_api_health():
    """API 서버 상태 확인"""
    print("=" * 70)
    print("[TEST] API 서버 상태 확인")
    print("=" * 70)
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("[SUCCESS] API 서버가 정상적으로 실행 중입니다!")
            print(f"   응답: {response.json()}")
            return True
        else:
            print(f"[ERROR] API 서버 응답 오류: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("[ERROR] API 서버에 연결할 수 없습니다.")
        print(f"   서버가 실행 중인지 확인하세요: {API_BASE_URL}")
        print("\n[TIP] 다음 명령어로 서버를 시작하세요:")
        print("   uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"[ERROR] 오류 발생: {e}")
        return False

def test_local_endpoints():
    """로컬 API 엔드포인트 테스트"""
    print("\n" + "=" * 70)
    print("[TEST] 로컬 API 엔드포인트 테스트")
    print("=" * 70)
    
    endpoints = [
        ("/api/local/jobs/list", "GET", None),
    ]
    
    results = []
    for endpoint, method, data in endpoints:
        try:
            print(f"\n[TEST] {method} {endpoint}")
            if method == "GET":
                response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=5)
            elif method == "POST":
                response = requests.post(f"{API_BASE_URL}{endpoint}", json=data, timeout=5)
            
            if response.status_code == 200:
                print(f"   [SUCCESS] 상태 코드: {response.status_code}")
                result_data = response.json()
                if isinstance(result_data, dict) and "files" in result_data:
                    print(f"   [INFO] 파일 개수: {len(result_data['files'])}")
                results.append(True)
            else:
                print(f"   [ERROR] 상태 코드: {response.status_code}")
                results.append(False)
        except Exception as e:
            print(f"   [ERROR] {e}")
            results.append(False)
    
    return all(results)

def test_file_structure():
    """필수 파일 구조 확인"""
    print("\n" + "=" * 70)
    print("[TEST] 파일 구조 확인")
    print("=" * 70)
    
    required_files = [
        "app/main.py",
        "app/api/local.py",
        "frontend/src/pages/LocalDashboard.tsx",
        "scripts/start_ui.py",
    ]
    
    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"   [OK] {file_path}")
        else:
            print(f"   [MISSING] {file_path}")
            all_exist = False
    
    return all_exist

def main():
    """메인 테스트 함수"""
    print("\n" + "=" * 70)
    print("로컬 웹 UI 테스트")
    print("=" * 70)
    print()
    
    # 파일 구조 확인
    file_ok = test_file_structure()
    
    if not file_ok:
        print("\n[WARNING] 일부 필수 파일이 없습니다.")
        return 1
    
    # API 서버 상태 확인
    api_ok = test_api_health()
    
    if not api_ok:
        print("\n" + "=" * 70)
        print("[SUMMARY] 테스트 결과")
        print("=" * 70)
        print("[FAIL] API 서버가 실행되지 않았습니다.")
        print("\n[SOLUTION] 다음 명령어로 서버를 시작하세요:")
        print("   uvicorn app.main:app --reload")
        print("\n또는:")
        print("   python scripts/start_ui.py")
        return 1
    
    # 로컬 엔드포인트 테스트
    endpoints_ok = test_local_endpoints()
    
    # 결과 요약
    print("\n" + "=" * 70)
    print("[SUMMARY] 테스트 결과")
    print("=" * 70)
    
    if api_ok and endpoints_ok:
        print("[SUCCESS] 모든 테스트 통과!")
        print("\n[INFO] 웹 UI 접속:")
        print("   - 프론트엔드: http://localhost:3000 (또는 http://localhost:5173)")
        print("   - API 문서: http://localhost:8000/docs")
        print("\n[TIP] 프론트엔드를 시작하려면:")
        print("   cd frontend")
        print("   npm install  # 처음 한 번만")
        print("   npm start")
        return 0
    else:
        print("[FAIL] 일부 테스트 실패")
        return 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[WARNING] 테스트가 중단되었습니다.")
        sys.exit(1)

