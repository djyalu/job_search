"""빠른 테스트"""
import requests
import sys
import io

if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass

print("=" * 70)
print("빠른 API 테스트")
print("=" * 70)

# 1. Health check
print("\n1. Health Check:")
try:
    r = requests.get("http://localhost:8000/health", timeout=2)
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.json()}")
except Exception as e:
    print(f"   ERROR: {e}")

# 2. Root
print("\n2. Root endpoint:")
try:
    r = requests.get("http://localhost:8000/", timeout=2)
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.json()}")
except Exception as e:
    print(f"   ERROR: {e}")

# 3. Local jobs list
print("\n3. Local jobs list:")
try:
    r = requests.get("http://localhost:8000/api/local/jobs/list", timeout=2)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"   Response: {data}")
    else:
        print(f"   Error: {r.text}")
except Exception as e:
    print(f"   ERROR: {e}")

# 4. OpenAPI docs
print("\n4. API Documentation:")
print("   http://localhost:8000/docs")
print("   http://localhost:8000/openapi.json")

print("\n" + "=" * 70)
print("테스트 완료!")
print("=" * 70)
print("\n[TIP] 서버를 재시작하려면:")
print("   1. 현재 실행 중인 서버를 중지 (Ctrl+C)")
print("   2. python -m uvicorn app.main:app --reload")

