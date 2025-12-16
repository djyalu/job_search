import os
from typing import Dict
from app.models.resume import ResumeData
from app.models.job import JobPosting
from app.models.matching import MatchScore
import json

class MatchingService:
    """이력서와 채용 공고 적합도 분석 서비스"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.use_openai = bool(self.openai_api_key)
    
    async def calculate_match(self, resume_data: ResumeData, job: JobPosting) -> MatchScore:
        """이력서와 채용 공고의 적합도 계산"""
        
        # 1. 스킬 매칭
        skills_score = self._calculate_skills_match(resume_data, job)
        
        # 2. 경력 매칭
        experience_score = self._calculate_experience_match(resume_data, job)
        
        # 3. 학력 매칭
        education_score = self._calculate_education_match(resume_data, job)
        
        # 4. 설명 매칭 (키워드 기반)
        description_score, matched_keywords, missing_keywords = self._calculate_description_match(
            resume_data, job
        )
        
        # 전체 점수 계산 (가중 평균)
        overall_score = (
            skills_score * 0.3 +
            experience_score * 0.3 +
            education_score * 0.1 +
            description_score * 0.3
        )
        
        # 추천사항 생성
        recommendations = self._generate_recommendations(
            resume_data, job, matched_keywords, missing_keywords
        )
        
        return MatchScore(
            overall_score=round(overall_score, 2),
            skills_match=round(skills_score, 2),
            experience_match=round(experience_score, 2),
            education_match=round(education_score, 2),
            description_match=round(description_score, 2),
            matched_keywords=matched_keywords,
            missing_keywords=missing_keywords,
            recommendations=recommendations
        )
    
    def _calculate_skills_match(self, resume: ResumeData, job: JobPosting) -> float:
        """스킬 매칭 점수 계산"""
        if not resume.skills:
            return 0.0
        
        # 채용 공고에서 스킬 키워드 추출
        job_text = (job.title + " " + job.description).lower()
        resume_skills_lower = [s.lower() for s in resume.skills]
        
        # 공통 스킬 찾기
        matched_skills = []
        for skill in resume_skills_lower:
            if skill in job_text:
                matched_skills.append(skill)
        
        # 채용 공고에서 요구하는 스킬 추정
        common_tech_keywords = [
            'python', 'javascript', 'java', 'react', 'vue', 'angular', 'node.js',
            'django', 'flask', 'fastapi', 'spring', 'sql', 'mongodb', 'postgresql',
            'aws', 'docker', 'kubernetes', 'git', 'linux', 'agile', 'machine learning'
        ]
        required_skills = [kw for kw in common_tech_keywords if kw in job_text]
        
        if not required_skills:
            return 50.0  # 스킬 요구사항이 명확하지 않으면 중간 점수
        
        # 매칭 비율 계산
        match_ratio = len(matched_skills) / len(required_skills) if required_skills else 0
        return min(match_ratio * 100, 100.0)
    
    def _calculate_experience_match(self, resume: ResumeData, job: JobPosting) -> float:
        """경력 매칭 점수 계산"""
        if not resume.experience:
            return 0.0
        
        # 채용 공고에서 경력 관련 키워드 추출
        job_text = job.description.lower()
        experience_keywords = ['experience', 'years', 'senior', 'junior', 'lead', 'manager']
        
        # 경력 수준 추정
        is_senior = any(kw in job_text for kw in ['senior', 'lead', 'manager', '5+', '10+'])
        is_junior = any(kw in job_text for kw in ['junior', 'entry', '0-2', '1-3'])
        
        # 이력서 경력 항목 수로 추정
        experience_count = len(resume.experience)
        
        if is_senior and experience_count >= 3:
            return 90.0
        elif is_junior and experience_count >= 1:
            return 80.0
        elif experience_count >= 2:
            return 70.0
        elif experience_count >= 1:
            return 50.0
        else:
            return 20.0
    
    def _calculate_education_match(self, resume: ResumeData, job: JobPosting) -> float:
        """학력 매칭 점수 계산"""
        if not resume.education:
            return 50.0  # 학력 정보가 없으면 중간 점수
        
        job_text = job.description.lower()
        education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college']
        
        # 학력 요구사항이 있는지 확인
        has_education_requirement = any(kw in job_text for kw in education_keywords)
        
        if has_education_requirement:
            # 학력 정보가 있으면 높은 점수
            return 80.0
        else:
            return 70.0  # 학력 요구사항이 없으면 중간 점수
    
    def _calculate_description_match(
        self, resume: ResumeData, job: JobPosting
    ) -> tuple[float, list, list]:
        """설명 매칭 점수 계산 및 키워드 추출"""
        resume_text = resume.raw_text.lower()
        job_text = (job.title + " " + job.description).lower()
        
        # 중요한 키워드 추출 (간단한 방법)
        job_words = set(job_text.split())
        resume_words = set(resume_text.split())
        
        # 공통 키워드 (3글자 이상)
        common_keywords = [
            word for word in job_words
            if len(word) > 3 and word in resume_words
        ]
        
        # 누락된 키워드
        important_keywords = [
            word for word in job_words
            if len(word) > 4 and word not in resume_words
            and word not in ['the', 'and', 'for', 'with', 'this', 'that']
        ][:10]  # 상위 10개만
        
        # 매칭 비율 계산
        if len(job_words) > 0:
            match_ratio = len(common_keywords) / min(len(job_words), 100)
            score = min(match_ratio * 100, 100.0)
        else:
            score = 0.0
        
        return score, common_keywords[:20], important_keywords
    
    def _generate_recommendations(
        self, resume: ResumeData, job: JobPosting,
        matched_keywords: list, missing_keywords: list
    ) -> list:
        """추천사항 생성"""
        recommendations = []
        
        if missing_keywords:
            recommendations.append(
                f"이력서에 다음 키워드를 추가하는 것을 고려하세요: {', '.join(missing_keywords[:5])}"
            )
        
        if resume.skills and len(resume.skills) < 5:
            recommendations.append("더 많은 기술 스킬을 이력서에 추가하세요.")
        
        if not resume.experience:
            recommendations.append("경력 섹션을 추가하여 관련 경험을 강조하세요.")
        
        if not resume.summary:
            recommendations.append("요약 섹션을 추가하여 채용 공고와의 연관성을 명확히 하세요.")
        
        if len(recommendations) == 0:
            recommendations.append("이력서가 채용 공고와 잘 맞습니다!")
        
        return recommendations

