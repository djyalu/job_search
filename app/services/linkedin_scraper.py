import asyncio
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from app.models.job import JobPosting
from datetime import datetime
import os

class LinkedInScraper:
    """LinkedIn 채용 공고 스크래퍼"""
    
    def __init__(self):
        self.base_url = "https://www.linkedin.com/jobs/search"
        self.driver = None
    
    def _init_driver(self):
        """Selenium 드라이버 초기화"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    async def search(self, keyword: str, location: Optional[str] = None, max_results: int = 20) -> List[JobPosting]:
        """LinkedIn에서 채용 공고 검색"""
        try:
            if not self.driver:
                self._init_driver()
            
            # 검색 URL 구성
            params = f"?keywords={keyword.replace(' ', '%20')}"
            if location:
                params += f"&location={location.replace(' ', '%20')}"
            
            url = f"{self.base_url}{params}"
            self.driver.get(url)
            
            # 페이지 로딩 대기
            await asyncio.sleep(3)
            
            # 스크롤하여 더 많은 결과 로드
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                await asyncio.sleep(2)
            
            # HTML 파싱
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            jobs = []
            
            # LinkedIn 채용 공고 요소 찾기
            job_cards = soup.find_all('div', class_='base-card')[:max_results]
            
            for idx, card in enumerate(job_cards):
                try:
                    title_elem = card.find('h3', class_='base-search-card__title')
                    company_elem = card.find('h4', class_='base-search-card__subtitle')
                    location_elem = card.find('span', class_='job-search-card__location')
                    link_elem = card.find('a', class_='base-card__full-link')
                    
                    if title_elem and company_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        company = company_elem.get_text(strip=True)
                        location_text = location_elem.get_text(strip=True) if location_elem else None
                        job_url = link_elem.get('href', '')
                        
                        # 상세 정보 가져오기 (선택사항)
                        description = await self._get_job_description(job_url) if job_url else ""
                        
                        job = JobPosting(
                            id=f"linkedin_{idx}",
                            title=title,
                            company=company,
                            location=location_text,
                            description=description,
                            url=job_url if job_url.startswith('http') else f"https://www.linkedin.com{job_url}",
                            source="linkedin",
                            posted_date=datetime.now()
                        )
                        jobs.append(job)
                except Exception as e:
                    print(f"채용 공고 파싱 오류: {e}")
                    continue
            
            return jobs
            
        except Exception as e:
            print(f"LinkedIn 검색 오류: {e}")
            return []
    
    async def _get_job_description(self, job_url: str) -> str:
        """채용 공고 상세 설명 가져오기"""
        try:
            if not job_url.startswith('http'):
                job_url = f"https://www.linkedin.com{job_url}"
            
            self.driver.get(job_url)
            await asyncio.sleep(2)
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            description_elem = soup.find('div', class_='show-more-less-html__markup')
            
            if description_elem:
                return description_elem.get_text(strip=True)
            return ""
        except:
            return ""
    
    def __del__(self):
        """드라이버 종료"""
        if self.driver:
            self.driver.quit()

