from fastapi import APIRouter, HTTPException
from app.models.job import JobSearchRequest, JobSearchResponse
from app.services.job_search import JobSearchService

router = APIRouter()
job_search_service = JobSearchService()

@router.post("/search", response_model=JobSearchResponse)
async def search_jobs(request: JobSearchRequest):
    """채용 공고 검색"""
    try:
        jobs = await job_search_service.search_jobs(request)
        return JobSearchResponse(
            total=len(jobs),
            jobs=jobs,
            search_params=request
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"검색 중 오류 발생: {str(e)}")

@router.get("/sources")
async def get_sources():
    """사용 가능한 검색 소스 목록"""
    return {
        "sources": [
            {"id": "linkedin", "name": "LinkedIn"},
            {"id": "indeed", "name": "Indeed"}
        ]
    }

