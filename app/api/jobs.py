from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.db.database import get_db
from app.models.job import Job, JobApplication
from app.services.job_scraper import JobScraper
from app.services.llm_service import LLMService
from app.services.email_service import EmailService

router = APIRouter()

class JobResponse(BaseModel):
    id: int
    title: str
    company_name: str
    description: str = None
    salary_from: int = None
    salary_to: int = None
    currency: str
    location: str = None
    url: str
    match_score: float = None
    llm_analysis: str = None
    platform: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class JobSearchRequest(BaseModel):
    user_id: int
    keywords: List[str] = []
    location: str = None
    salary_from: int = None
    experience_level: str = None

class JobApplicationRequest(BaseModel):
    job_ids: List[int]
    resume_id: int
    custom_cover_letter: str = None

@router.post("/search", response_model=List[JobResponse])
async def search_jobs(
    search_request: JobSearchRequest,
    db: Session = Depends(get_db)
):
    """Поиск вакансий по параметрам"""
    
    try:
        # Получаем резюме пользователя для анализа соответствия
        from app.models.resume import Resume
        user_resume = db.query(Resume).filter(Resume.user_id == search_request.user_id).first()
        
        if not user_resume:
            raise HTTPException(status_code=400, detail="У пользователя нет загруженного резюме")
        
        # Ищем вакансии
        scraper = JobScraper()
        jobs_data = await scraper.search_jobs(
            keywords=search_request.keywords,
            location=search_request.location,
            salary_from=search_request.salary_from,
            experience_level=search_request.experience_level
        )
        
        # Анализируем соответствие с помощью LLM
        llm_service = LLMService()
        jobs = []
        
        for job_data in jobs_data:
            # Проверяем, не существует ли уже эта вакансия
            existing_job = db.query(Job).filter(
                Job.external_id == job_data['external_id'],
                Job.platform == job_data['platform']
            ).first()
            
            if existing_job:
                jobs.append(existing_job)
                continue
            
            # Анализируем соответствие резюме и вакансии
            match_analysis = await llm_service.analyze_job_match(
                user_resume.extracted_text,
                job_data['description']
            )
            
            # Создаем новую вакансию
            db_job = Job(
                external_id=job_data['external_id'],
                platform=job_data['platform'],
                title=job_data['title'],
                company_name=job_data['company_name'],
                description=job_data['description'],
                requirements=job_data.get('requirements'),
                salary_from=job_data.get('salary_from'),
                salary_to=job_data.get('salary_to'),
                currency=job_data.get('currency', 'RUB'),
                location=job_data.get('location'),
                employment_type=job_data.get('employment_type'),
                experience_level=job_data.get('experience_level'),
                url=job_data['url'],
                hr_contacts=job_data.get('hr_contacts', []),
                company_contacts=job_data.get('company_contacts', []),
                match_score=match_analysis['score'],
                llm_analysis=match_analysis['analysis']
            )
            
            db.add(db_job)
            jobs.append(db_job)
        
        db.commit()
        
        # Сортируем по соответствию
        jobs.sort(key=lambda x: x.match_score or 0, reverse=True)
        
        return jobs
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка поиска вакансий: {str(e)}")

@router.post("/apply", response_model=dict)
async def apply_to_jobs(
    application_request: JobApplicationRequest,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Подача заявок на выбранные вакансии"""
    
    try:
        from app.models.resume import Resume
        from app.models.user import User
        
        # Получаем данные пользователя и резюме
        user = db.query(User).filter(User.id == user_id).first()
        resume = db.query(Resume).filter(Resume.id == application_request.resume_id).first()
        
        if not user or not resume:
            raise HTTPException(status_code=404, detail="Пользователь или резюме не найдены")
        
        results = []
        email_service = EmailService()
        
        for job_id in application_request.job_ids:
            job = db.query(Job).filter(Job.id == job_id).first()
            if not job:
                continue
            
            # Проверяем, не подавали ли уже заявку
            existing_application = db.query(JobApplication).filter(
                JobApplication.user_id == user_id,
                JobApplication.job_id == job_id
            ).first()
            
            if existing_application:
                results.append({
                    "job_id": job_id,
                    "status": "already_applied",
                    "message": f"Заявка на вакансию '{job.title}' уже подана"
                })
                continue
            
            # Генерируем сопроводительное письмо
            llm_service = LLMService()
            cover_letter = application_request.custom_cover_letter or await llm_service.generate_cover_letter(
                resume.extracted_text,
                job.description,
                job.company_name
            )
            
            # Создаем заявку
            application = JobApplication(
                user_id=user_id,
                job_id=job_id,
                resume_id=application_request.resume_id,
                cover_letter=cover_letter,
                status="pending"
            )
            
            db.add(application)
            
            # Отправляем письма HR
            hr_emails_sent = []
            if job.hr_contacts:
                for hr_contact in job.hr_contacts:
                    if hr_contact.get('email'):
                        email_sent = await email_service.send_application_email(
                            user_email=user.email,
                            user_password=user.email_password,
                            hr_email=hr_contact['email'],
                            job_title=job.title,
                            company_name=job.company_name,
                            cover_letter=cover_letter,
                            resume_path=resume.file_path
                        )
                        
                        if email_sent:
                            hr_emails_sent.append({
                                "email": hr_contact['email'],
                                "sent_at": datetime.utcnow().isoformat(),
                                "status": "sent"
                            })
            
            application.hr_emails_sent = hr_emails_sent
            application.status = "sent" if hr_emails_sent else "pending"
            
            results.append({
                "job_id": job_id,
                "status": "success",
                "message": f"Заявка на '{job.title}' отправлена",
                "emails_sent": len(hr_emails_sent)
            })
        
        db.commit()
        
        return {
            "success": True,
            "message": f"Обработано {len(application_request.job_ids)} вакансий",
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка подачи заявок: {str(e)}")

@router.get("/applications/{user_id}", response_model=List[dict])
async def get_user_applications(user_id: int, db: Session = Depends(get_db)):
    """Получение всех заявок пользователя"""
    
    applications = db.query(JobApplication).filter(JobApplication.user_id == user_id).all()
    
    result = []
    for app in applications:
        result.append({
            "id": app.id,
            "job": {
                "title": app.job.title,
                "company_name": app.job.company_name,
                "url": app.job.url
            },
            "status": app.status,
            "applied_at": app.applied_at,
            "response_received": app.response_received,
            "emails_sent_count": len(app.hr_emails_sent) if app.hr_emails_sent else 0
        })
    
    return result