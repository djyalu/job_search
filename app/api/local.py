"""
로컬 웹 UI를 위한 API 엔드포인트
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from pathlib import Path
import json
import shutil
import os
from datetime import datetime

class SearchRequest(BaseModel):
    keyword: str
    location: str = ""
    max_results: int = 30

router = APIRouter()

@router.get("/jobs/list")
async def list_job_files():
    """수집된 채용 공고 파일 목록"""
    jobs_dir = Path("jobs")
    if not jobs_dir.exists():
        return {"files": []}
    
    files = []
    for file in jobs_dir.glob("*.json"):
        if file.name != "latest.json":
            stat = file.stat()
            files.append({
                "name": file.name,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
    
    # latest.json도 추가
    latest_file = jobs_dir / "latest.json"
    if latest_file.exists():
        stat = latest_file.stat()
        files.insert(0, {
            "name": "latest.json",
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
        })
    
    return {"files": files}

@router.get("/jobs/{filename}")
async def get_job_file(filename: str):
    """특정 채용 공고 파일 내용"""
    jobs_dir = Path("jobs")
    file_path = jobs_dir / filename
    
    if not file_path.exists() or not filename.endswith('.json'):
        raise HTTPException(status_code=404, detail="File not found")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data

@router.post("/jobs/search")
async def search_jobs_local(keyword: str, location: str = "", max_results: int = 30):
    """로컬에서 채용 공고 검색 실행"""
    import subprocess
    import os
    
    # 환경 변수 설정
    env = os.environ.copy()
    env['SEARCH_KEYWORDS'] = request.keyword
    env['SEARCH_LOCATION'] = request.location or 'Seoul, South Korea'
    
    try:
        # 스크립트 실행
        result = subprocess.run(
            ["python", "scripts/daily_job_search.py"],
            env=env,
            capture_output=True,
            text=True,
            timeout=600  # 10분 타임아웃
        )
        
        if result.returncode == 0:
            # 최신 결과 로드
            latest_file = Path("jobs/latest.json")
            if latest_file.exists():
                with open(latest_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return {
                    "success": True,
                    "message": "검색 완료",
                    "data": data
                }
            else:
                return {
                    "success": True,
                    "message": "검색 완료되었지만 결과 파일을 찾을 수 없습니다"
                }
        else:
            return {
                "success": False,
                "message": f"검색 중 오류 발생: {result.stderr}"
            }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "message": "검색 시간이 초과되었습니다"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"오류 발생: {str(e)}"
        }

@router.post("/resume/upload")
async def upload_resume_local(file: UploadFile = File(...)):
    """이력서 업로드"""
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    
    file_path = upload_dir / file.filename
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "success": True,
            "message": "이력서가 업로드되었습니다",
            "filename": file.filename,
            "path": str(file_path)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"업로드 오류: {str(e)}")

@router.post("/resume/compare")
async def compare_resume_local(resume_path: str, jobs_file: str = "latest.json", top_n: int = 10):
    """이력서와 채용 공고 비교"""
    import subprocess
    
    try:
        # 비교 스크립트 실행
        cmd = [
            "python", "scripts/compare_resume.py",
            resume_path,
            "--jobs", f"jobs/{jobs_file}",
            "--top", str(top_n),
            "--html",
            "--output", "jobs/resume_comparison.html"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5분 타임아웃
        )
        
        if result.returncode == 0:
            # HTML 리포트 경로 반환
            return {
                "success": True,
                "message": "비교 완료",
                "report_path": "jobs/resume_comparison.html"
            }
        else:
            return {
                "success": False,
                "message": f"비교 중 오류 발생: {result.stderr}"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"오류 발생: {str(e)}"
        }

@router.get("/reports/comparison")
async def get_comparison_report():
    """비교 리포트 HTML 반환"""
    report_path = Path("jobs/resume_comparison.html")
    
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="비교 리포트를 찾을 수 없습니다")
    
    return FileResponse(
        report_path,
        media_type="text/html",
        filename="resume_comparison.html"
    )

@router.get("/uploads/list")
async def list_uploaded_resumes():
    """업로드된 이력서 목록"""
    upload_dir = Path("uploads")
    if not upload_dir.exists():
        return {"files": []}
    
    files = []
    for file in upload_dir.iterdir():
        if file.is_file() and file.suffix.lower() in ['.pdf', '.docx', '.doc', '.txt']:
            stat = file.stat()
            files.append({
                "name": file.name,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "path": str(file)
            })
    
    return {"files": files}

