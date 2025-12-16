import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.resume import ResumeUpload
from app.services.resume_parser import ResumeParser

router = APIRouter()
resume_parser = ResumeParser()

# 저장된 이력서 데이터 (실제로는 데이터베이스 사용 권장)
resume_storage = {}

@router.post("/upload", response_model=ResumeUpload)
async def upload_resume(file: UploadFile = File(...)):
    """이력서 업로드 및 파싱"""
    try:
        # 파일 저장
        file_path = os.path.join(resume_parser.upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 이력서 파싱
        file_id, resume_data = await resume_parser.parse_resume(file_path, file.filename)
        
        # 저장
        resume_storage[file_id] = {
            "file_path": file_path,
            "filename": file.filename,
            "resume_data": resume_data
        }
        
        return ResumeUpload(
            file_id=file_id,
            filename=file.filename,
            resume_data=resume_data,
            message="이력서가 성공적으로 업로드되었습니다."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"이력서 업로드 중 오류 발생: {str(e)}")

@router.get("/{file_id}")
async def get_resume(file_id: str):
    """업로드된 이력서 조회"""
    if file_id not in resume_storage:
        raise HTTPException(status_code=404, detail="이력서를 찾을 수 없습니다.")
    
    return resume_storage[file_id]

