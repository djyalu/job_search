"""
로컬 웹 UI 서버 시작 스크립트
"""
import subprocess
import sys
import webbrowser
import time
from pathlib import Path

def main():
    """메인 함수"""
    print("=" * 70)
    print("🚀 Job Search & Resume Matching - Local Web UI")
    print("=" * 70)
    print()
    
    # FastAPI 서버 시작
    print("[INFO] FastAPI 서버를 시작합니다...")
    print("[INFO] 서버 주소: http://localhost:8006")
    print("[INFO] 웹 UI 주소: http://localhost:3006")
    print()
    print("[TIP] 브라우저가 자동으로 열립니다.")
    print("[TIP] 서버를 중지하려면 Ctrl+C를 누르세요.")
    print()
    print("=" * 70)
    
    try:
        # FastAPI 서버 시작
        uvicorn_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8006"],
            cwd=Path(__file__).parent.parent
        )
        
        # React 개발 서버 시작 (선택사항)
        frontend_dir = Path(__file__).parent.parent / "frontend"
        if frontend_dir.exists():
            print("[INFO] React 개발 서버를 시작합니다...")
            react_process = subprocess.Popen(
                ["npm", "start"],
                cwd=frontend_dir,
                shell=True
            )
        else:
            react_process = None
            print("[WARNING] frontend 디렉토리를 찾을 수 없습니다.")
            print("[INFO] API 서버만 실행됩니다: http://localhost:8006")
        
        # 잠시 대기 후 브라우저 열기
        time.sleep(3)
        
        # 브라우저 열기
        try:
            if react_process:
                webbrowser.open("http://localhost:3006")
            else:
                webbrowser.open("http://localhost:8006/docs")
        except:
            pass
        
        # 프로세스 대기
        try:
            uvicorn_process.wait()
        except KeyboardInterrupt:
            print("\n[INFO] 서버를 종료합니다...")
            uvicorn_process.terminate()
            if react_process:
                react_process.terminate()
    
    except Exception as e:
        print(f"[ERROR] 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

