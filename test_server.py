"""서버 상태 종합 테스트"""
import requests
import sys
import io

if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass

API_BASE = "http://localhost:8006"

print("=" * 70)
print("서버 상태 테스트")
print("=" * 70)

tests = [
    ("Health Check", "/health"),
    ("Root", "/"),
    ("Jobs List", "/api/local/jobs/list"),
    ("OpenAPI Docs", "/docs"),
]

all_ok = True

for name, endpoint in tests:
    try:
        url = f"{API_BASE}{endpoint}"
        print(f"\n[TEST] {name}: {url}")
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            print(f"   [OK] Status: {r.status_code}")
            if endpoint == "/health":
                print(f"   Response: {r.json()}")
        else:
            print(f"   [WARNING] Status: {r.status_code}")
            all_ok = False
    except requests.exceptions.ConnectionError:
        print(f"   [ERROR] 서버에 연결할 수 없습니다!")
        print(f"   서버가 실행 중인지 확인하세요: {API_BASE}")
        all_ok = False
        break
    except Exception as e:
        print(f"   [ERROR] {e}")
        all_ok = False

print("\n" + "=" * 70)
if all_ok:
    print("[SUCCESS] 모든 테스트 통과!")
    print(f"\n접속 주소:")
    print(f"  - API 서버: {API_BASE}")
    print(f"  - API 문서: {API_BASE}/docs")
    print(f"  - 프론트엔드: http://localhost:3006 (npm start 필요)")
else:
    print("[FAIL] 일부 테스트 실패")
    print("\n[SOLUTION] 서버를 시작하세요:")
    print("  python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8006")
print("=" * 70)

