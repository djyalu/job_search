import asyncio
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
from app.models.job import JobPosting
from datetime import datetime
import urllib.parse

class IndeedScraper:
    """Indeed 채용 공고 스크래퍼"""
    
    def __init__(self):
        self.base_url = "https://www.indeed.com/jobs"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    async def search(self, keyword: str, location: Optional[str] = None, max_results: int = 20) -> List[JobPosting]:
        """Indeed에서 채용 공고 검색"""
        try:
            # 검색 파라미터 구성
            params = {
                'q': keyword,
                'limit': max_results
            }
            if location:
                params['l'] = location
            
            url = f"{self.base_url}?{urllib.parse.urlencode(params)}"
            
            # HTTP 요청
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            jobs = []
            
            # Indeed 채용 공고 요소 찾기
            job_cards = soup.find_all('div', class_='job_seen_beacon')[:max_results]
            
            for idx, card in enumerate(job_cards):
                try:
                    title_elem = card.find('h2', class_='jobTitle')
                    company_elem = card.find('span', class_='companyName')
                    location_elem = card.find('div', class_='companyLocation')
                    link_elem = card.find('a', class_='jcs-JobTitle')
                    summary_elem = card.find('div', class_='job-snippet')
                    
                    if title_elem and company_elem:
                        title = title_elem.get_text(strip=True)
                        company = company_elem.get_text(strip=True)
                        location_text = location_elem.get_text(strip=True) if location_elem else None
                        summary = summary_elem.get_text(strip=True) if summary_elem else ""
                        
                        # 링크 구성
                        link = link_elem.get('href', '') if link_elem else ''
                        if link and not link.startswith('http'):
                            link = f"https://www.indeed.com{link}"
                        
                        job = JobPosting(
                            id=f"indeed_{idx}",
                            title=title,
                            company=company,
                            location=location_text,
                            description=summary,
                            url=link,
                            source="indeed",
                            posted_date=datetime.now()
                        )
                        jobs.append(job)
                except Exception as e:
                    print(f"채용 공고 파싱 오류: {e}")
                    continue
            
            return jobs
            
        except Exception as e:
            print(f"Indeed 검색 오류: {e}")
            return []

