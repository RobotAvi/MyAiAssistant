from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    
    # Извлеченная информация из резюме
    extracted_text = Column(Text)
    skills = Column(JSON)  # Список навыков
    experience_years = Column(Integer)
    position_title = Column(String)
    salary_expectation = Column(String)
    location = Column(String)
    
    # Векторное представление для поиска
    embedding = Column(JSON)  # Будет содержать векторы от OpenAI
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    user = relationship("User", back_populates="resumes")