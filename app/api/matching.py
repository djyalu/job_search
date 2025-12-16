from fastapi import APIRouter, HTTPException
from app.models.matching import MatchingRequest, MatchingResponse
from app.services.matching import MatchingService
from app.api.resume import resume_storage
from app.services.job_search import JobSearchService

router = APIRouter()
matching_service = MatchingService()
job_search_service = JobSearchService()

# 임시 채용 공고 저장소 (실제로는 데이터베이스 사용 권장)
job_storage = {}

@router.post("/analyze", response_model=MatchingResponse)
async def analyze_match(request: MatchingRequest):
    """이력서와 채용 공고의 적합도 분석"""
    try:
        # 이력서 조회
        if request.resume_id not in resume_storage:
            raise HTTPException(status_code=404, detail="이력서를 찾을 수 없습니다.")
        
        resume_info = resume_storage[request.resume_id]
        resume_data = resume_info["resume_data"]
        
        # 채용 공고 조회 (임시 저장소 또는 재검색)
        if request.job_id not in job_storage:
            raise HTTPException(status_code=404, detail="채용 공고를 찾을 수 없습니다.")
        
        job = job_storage[request.job_id]
        
        # 적합도 계산
        match_score = await matching_service.calculate_match(resume_data, job)
        
        # 분석 텍스트 생성
        analysis = f"""
이력서와 '{job.title}' 채용 공고의 적합도 분석 결과입니다.

전체 적합도: {match_score.overall_score}%

세부 점수:
- 스킬 매칭: {match_score.skills_match}%
- 경력 매칭: {match_score.experience_match}%
- 학력 매칭: {match_score.education_match}%
- 설명 매칭: {match_score.description_match}%

매칭된 키워드: {', '.join(match_score.matched_keywords[:10])}

추천사항:
{chr(10).join('- ' + rec for rec in match_score.recommendations)}
        """.strip()
        
        return MatchingResponse(
            resume_id=request.resume_id,
            job_id=request.job_id,
            job_title=job.title,
            company=job.company,
            match_score=match_score,
            analysis=analysis
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"적합도 분석 중 오류 발생: {str(e)}")

@router.post("/store-job")
async def store_job(job_data: dict):
    """채용 공고를 임시 저장소에 저장 (검색 후 사용)"""
    from app.models.job import JobPosting
    job = JobPosting(**job_data)
    job_storage[job.id] = job
    return {"message": "채용 공고가 저장되었습니다.", "job_id": job.id}

