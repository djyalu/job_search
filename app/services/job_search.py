import asyncio
from typing import List
from app.models.job import JobPosting, JobSearchRequest
from app.services.linkedin_scraper import LinkedInScraper
from app.services.indeed_scraper import IndeedScraper

class JobSearchService:
    """채용 공고 검색 서비스"""
    
    def __init__(self):
        self.linkedin_scraper = LinkedInScraper()
        self.indeed_scraper = IndeedScraper()
    
    async def search_jobs(self, request: JobSearchRequest) -> List[JobPosting]:
        """여러 소스에서 채용 공고 검색"""
        all_jobs = []
        tasks = []
        
        if "linkedin" in request.sources:
            tasks.append(self.linkedin_scraper.search(request.keyword, request.location, request.max_results))
        
        if "indeed" in request.sources:
            tasks.append(self.indeed_scraper.search(request.keyword, request.location, request.max_results))
        
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, list):
                    all_jobs.extend(result)
                elif isinstance(result, Exception):
                    print(f"검색 중 오류 발생: {result}")
        
        # 중복 제거 (URL 기준)
        seen_urls = set()
        unique_jobs = []
        for job in all_jobs:
            if job.url not in seen_urls:
                seen_urls.add(job.url)
                unique_jobs.append(job)
        
        return unique_jobs[:request.max_results]

