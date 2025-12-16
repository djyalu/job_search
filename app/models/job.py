from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class JobPosting(BaseModel):
    """채용 공고 정보"""
    id: str
    title: str
    company: str
    location: Optional[str] = None
    description: str
    url: str
    source: str  # "linkedin" or "indeed"
    posted_date: Optional[datetime] = None
    salary: Optional[str] = None
    job_type: Optional[str] = None  # "Full-time", "Part-time", etc.

class JobSearchRequest(BaseModel):
    """채용 공고 검색 요청"""
    keyword: str = Field(..., description="검색 키워드")
    location: Optional[str] = Field(None, description="지역 (선택사항)")
    max_results: int = Field(20, ge=1, le=100, description="최대 결과 수")
    sources: List[str] = Field(["linkedin", "indeed"], description="검색할 플랫폼")

class JobSearchResponse(BaseModel):
    """채용 공고 검색 응답"""
    total: int
    jobs: List[JobPosting]
    search_params: JobSearchRequest

