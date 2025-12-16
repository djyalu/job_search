from pydantic import BaseModel
from typing import Optional, List

class ResumeData(BaseModel):
    """파싱된 이력서 데이터"""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = []
    experience: List[dict] = []
    education: List[dict] = []
    summary: Optional[str] = None
    raw_text: str

class ResumeUpload(BaseModel):
    """이력서 업로드 응답"""
    file_id: str
    filename: str
    resume_data: ResumeData
    message: str

