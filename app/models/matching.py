from pydantic import BaseModel
from typing import List, Dict

class MatchScore(BaseModel):
    """적합도 점수 세부 정보"""
    overall_score: float  # 0-100
    skills_match: float
    experience_match: float
    education_match: float
    description_match: float
    matched_keywords: List[str]
    missing_keywords: List[str]
    recommendations: List[str]

class MatchingRequest(BaseModel):
    """적합도 분석 요청"""
    resume_id: str
    job_id: str

class MatchingResponse(BaseModel):
    """적합도 분석 응답"""
    resume_id: str
    job_id: str
    job_title: str
    company: str
    match_score: MatchScore
    analysis: str  # 상세 분석 텍스트

