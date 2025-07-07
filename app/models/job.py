from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, nullable=False)  # ID с внешней платформы
    platform = Column(String, nullable=False)  # hh.ru, linkedin, etc.
    
    title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    description = Column(Text)
    requirements = Column(Text)
    salary_from = Column(Integer)
    salary_to = Column(Integer)
    currency = Column(String, default="RUB")
    location = Column(String)
    employment_type = Column(String)  # full-time, part-time, contract
    experience_level = Column(String)  # junior, middle, senior
    
    # URL и контакты
    url = Column(String, nullable=False)
    hr_contacts = Column(JSON)  # Список HR контактов
    company_contacts = Column(JSON)  # Контакты компании
    
    # Анализ соответствия
    match_score = Column(Float)  # Скор соответствия резюме (0-1)
    llm_analysis = Column(Text)  # Анализ от LLM
    
    # Статус
    is_active = Column(Boolean, default=True)
    is_applied = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    applications = relationship("JobApplication", back_populates="job")

class JobApplication(Base):
    __tablename__ = "job_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    
    # Статус отклика
    status = Column(String, default="pending")  # pending, sent, responded, rejected
    
    # Сопроводительное письмо
    cover_letter = Column(Text)
    
    # HR письма
    hr_emails_sent = Column(JSON)  # Список отправленных писем HR
    
    # Отклики
    response_received = Column(Boolean, default=False)
    response_date = Column(DateTime)
    response_text = Column(Text)
    
    applied_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    user = relationship("User", back_populates="job_applications")
    job = relationship("Job", back_populates="applications")
    resume = relationship("Resume")