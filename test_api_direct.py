"""API 직접 테스트"""
import sys
import io

if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass

try:
    from app.api import local
    print("[SUCCESS] local 모듈 import 성공")
    print(f"[INFO] Router: {local.router}")
    
    # 엔드포인트 확인
    routes = [route.path for route in local.router.routes]
    print(f"[INFO] 등록된 엔드포인트:")
    for route in routes:
        print(f"   - {route}")
except Exception as e:
    print(f"[ERROR] Import 실패: {e}")
    import traceback
    traceback.print_exc()

