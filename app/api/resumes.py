from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import os
import json
from datetime import datetime

from app.db.database import get_db
from app.models.resume import Resume
from app.services.resume_processor import ResumeProcessor
from app.services.llm_service import LLMService

router = APIRouter()

class ResumeResponse(BaseModel):
    id: int
    filename: str
    position_title: str = None
    skills: List[str] = []
    experience_years: int = None
    location: str = None
    salary_expectation: str = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class ResumeAnalysis(BaseModel):
    skills: List[str]
    experience_years: int
    position_title: str
    location: str = None
    salary_expectation: str = None

@router.post("/upload/{user_id}", response_model=ResumeResponse)
async def upload_resume(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Загрузка и анализ резюме"""
    
    # Проверяем формат файла
    if not file.filename.lower().endswith(('.pdf', '.doc', '.docx', '.txt')):
        raise HTTPException(status_code=400, detail="Поддерживаются только файлы: PDF, DOC, DOCX, TXT")
    
    # Сохраняем файл
    upload_dir = "uploads/resumes"
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = os.path.join(upload_dir, f"{user_id}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    try:
        # Обрабатываем резюме
        processor = ResumeProcessor()
        extracted_text = await processor.extract_text(file_path)
        
        # Анализируем с помощью LLM
        llm_service = LLMService()
        analysis = await llm_service.analyze_resume(extracted_text)
        
        # Создаем эмбеддинг
        embedding = await llm_service.create_embedding(extracted_text)
        
        # Сохраняем в базу данных
        db_resume = Resume(
            user_id=user_id,
            filename=file.filename,
            file_path=file_path,
            extracted_text=extracted_text,
            skills=analysis.get('skills', []),
            experience_years=analysis.get('experience_years'),
            position_title=analysis.get('position_title'),
            salary_expectation=analysis.get('salary_expectation'),
            location=analysis.get('location'),
            embedding=embedding
        )
        
        db.add(db_resume)
        db.commit()
        db.refresh(db_resume)
        
        return db_resume
        
    except Exception as e:
        # Удаляем файл в случае ошибки
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Ошибка обработки резюме: {str(e)}")

@router.get("/user/{user_id}", response_model=List[ResumeResponse])
async def get_user_resumes(user_id: int, db: Session = Depends(get_db)):
    """Получение всех резюме пользователя"""
    resumes = db.query(Resume).filter(Resume.user_id == user_id).all()
    return resumes

@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(resume_id: int, db: Session = Depends(get_db)):
    """Получение конкретного резюме"""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Резюме не найдено")
    return resume

@router.delete("/{resume_id}")
async def delete_resume(resume_id: int, db: Session = Depends(get_db)):
    """Удаление резюме"""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Резюме не найдено")
    
    # Удаляем файл
    if os.path.exists(resume.file_path):
        os.remove(resume.file_path)
    
    # Удаляем из базы данных
    db.delete(resume)
    db.commit()
    
    return {"message": "Резюме успешно удалено"}