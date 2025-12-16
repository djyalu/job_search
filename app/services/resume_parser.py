import os
import uuid
from typing import Optional
import pdfplumber
from docx import Document
import re
from app.models.resume import ResumeData

class ResumeParser:
    """이력서 파싱 서비스"""
    
    def __init__(self):
        self.upload_dir = "uploads"
        os.makedirs(self.upload_dir, exist_ok=True)
    
    async def parse_resume(self, file_path: str, filename: str) -> tuple[str, ResumeData]:
        """이력서 파일 파싱"""
        file_id = str(uuid.uuid4())
        
        # 파일 확장자에 따라 파싱
        ext = os.path.splitext(filename)[1].lower()
        
        if ext == '.pdf':
            text = self._parse_pdf(file_path)
        elif ext in ['.docx', '.doc']:
            text = self._parse_docx(file_path)
        elif ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            raise ValueError(f"지원하지 않는 파일 형식: {ext}")
        
        # 이력서 데이터 추출
        resume_data = self._extract_resume_data(text)
        
        return file_id, resume_data
    
    def _parse_pdf(self, file_path: str) -> str:
        """PDF 파일 파싱"""
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    
    def _parse_docx(self, file_path: str) -> str:
        """DOCX 파일 파싱"""
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    
    def _extract_resume_data(self, text: str) -> ResumeData:
        """이력서 텍스트에서 데이터 추출"""
        # 이메일 추출
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        email = emails[0] if emails else None
        
        # 전화번호 추출
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        phone = phones[0] if phones else None
        
        # 이름 추출 (첫 번째 줄 또는 이메일 앞)
        name = None
        lines = text.split('\n')
        if lines:
            first_line = lines[0].strip()
            if len(first_line) < 50 and not '@' in first_line:
                name = first_line
        
        # 스킬 추출 (일반적인 기술 스킬 키워드)
        skill_keywords = [
            'Python', 'JavaScript', 'Java', 'C++', 'C#', 'React', 'Vue', 'Angular',
            'Node.js', 'Django', 'Flask', 'FastAPI', 'Spring', 'SQL', 'MongoDB',
            'PostgreSQL', 'AWS', 'Docker', 'Kubernetes', 'Git', 'Linux', 'Agile',
            'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Data Science'
        ]
        found_skills = []
        text_lower = text.lower()
        for skill in skill_keywords:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        # 경력 추출 (간단한 패턴 매칭)
        experience = []
        experience_section = self._extract_section(text, ['Experience', 'Work Experience', 'Employment'])
        if experience_section:
            # 간단한 경력 항목 추출
            exp_items = re.split(r'\n\s*\n', experience_section)
            for item in exp_items[:5]:  # 최대 5개
                if len(item.strip()) > 20:
                    experience.append({'description': item.strip()})
        
        # 학력 추출
        education = []
        education_section = self._extract_section(text, ['Education', 'Academic'])
        if education_section:
            edu_items = re.split(r'\n\s*\n', education_section)
            for item in edu_items[:3]:  # 최대 3개
                if len(item.strip()) > 10:
                    education.append({'description': item.strip()})
        
        # 요약 추출
        summary = None
        summary_section = self._extract_section(text, ['Summary', 'Objective', 'Profile', 'About'])
        if summary_section:
            summary = summary_section[:500]  # 최대 500자
        
        return ResumeData(
            name=name,
            email=email,
            phone=phone,
            skills=found_skills,
            experience=experience,
            education=education,
            summary=summary,
            raw_text=text
        )
    
    def _extract_section(self, text: str, section_names: list) -> Optional[str]:
        """특정 섹션 추출"""
        for section_name in section_names:
            pattern = rf'(?i){re.escape(section_name)}[:\s]*\n(.*?)(?=\n\s*[A-Z][A-Z\s]+:|\Z)'
            match = re.search(pattern, text, re.DOTALL)
            if match:
                return match.group(1).strip()
        return None

