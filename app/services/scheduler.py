import asyncio
from celery import Celery
from datetime import datetime, time
from sqlalchemy.orm import Session
from typing import List

from app.core.config import settings
from app.db.database import SessionLocal
from app.models.user import User
from app.models.resume import Resume
from app.services.job_scraper import JobScraper
from app.services.llm_service import LLMService
from app.services.telegram_service import TelegramService
from app.services.email_service import EmailService

# Создаем Celery app
celery_app = Celery(
    'hr_assistant',
    broker=settings.redis_url,
    backend=settings.redis_url
)

# Конфигурация Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Moscow',
    enable_utc=True,
)

# Расписание задач
celery_app.conf.beat_schedule = {
    'daily-job-search': {
        'task': 'app.services.scheduler.daily_job_search',
        'schedule': time(hour=9, minute=0),  # Каждый день в 9:00
    },
    'weekly-summary': {
        'task': 'app.services.scheduler.weekly_summary',
        'schedule': time(hour=18, minute=0),  # Каждую пятницу в 18:00
    },
}

@celery_app.task
def daily_job_search():
    """Ежедневный поиск вакансий для всех пользователей"""
    
    asyncio.run(_daily_job_search_async())

async def _daily_job_search_async():
    """Асинхронная версия ежедневного поиска"""
    
    db = SessionLocal()
    
    try:
        # Получаем всех активных пользователей с резюме
        users = db.query(User).filter(
            User.is_active == True,
            User.resumes.any()
        ).all()
        
        print(f"Запускаем поиск вакансий для {len(users)} пользователей")
        
        job_scraper = JobScraper()
        telegram_service = TelegramService()
        
        for user in users:
            try:
                # Получаем последнее резюме пользователя
                resume = db.query(Resume).filter(
                    Resume.user_id == user.id
                ).order_by(Resume.created_at.desc()).first()
                
                if not resume:
                    continue
                
                # Формируем ключевые слова для поиска на основе резюме
                keywords = resume.skills[:5] if resume.skills else []
                if resume.position_title:
                    keywords.append(resume.position_title)
                
                # Ищем вакансии
                jobs = await job_scraper.search_jobs(
                    keywords=keywords,
                    location=resume.location,
                    experience_level=_determine_experience_level(resume.experience_years),
                    limit=20
                )
                
                # Фильтруем только релевантные вакансии (score > 0.6)
                relevant_jobs = [job for job in jobs if job.get('match_score', 0) > 0.6]
                
                if relevant_jobs:
                    # Отправляем уведомление в Telegram
                    if user.telegram_chat_id:
                        await telegram_service.send_jobs_notification(
                            user_chat_id=user.telegram_chat_id,
                            jobs=relevant_jobs,
                            user_id=user.id
                        )
                    
                    print(f"Найдено {len(relevant_jobs)} релевантных вакансий для {user.email}")
                else:
                    print(f"Релевантных вакансий для {user.email} не найдено")
                
                # Небольшая задержка между пользователями
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"Ошибка поиска вакансий для пользователя {user.email}: {e}")
                continue
        
    except Exception as e:
        print(f"Ошибка в ежедневном поиске вакансий: {e}")
    
    finally:
        db.close()

@celery_app.task
def weekly_summary():
    """Еженедельная сводка по заявкам"""
    
    asyncio.run(_weekly_summary_async())

async def _weekly_summary_async():
    """Асинхронная версия еженедельной сводки"""
    
    db = SessionLocal()
    
    try:
        from app.models.job import JobApplication
        from datetime import datetime, timedelta
        
        # Получаем статистику за последнюю неделю
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        users = db.query(User).filter(User.is_active == True).all()
        telegram_service = TelegramService()
        
        for user in users:
            if not user.telegram_chat_id:
                continue
                
            # Статистика заявок за неделю
            applications = db.query(JobApplication).filter(
                JobApplication.user_id == user.id,
                JobApplication.applied_at >= week_ago
            ).all()
            
            if not applications:
                continue
            
            # Формируем сводку
            total_applications = len(applications)
            responded = len([app for app in applications if app.response_received])
            pending = total_applications - responded
            
            summary = f"""
📊 *Еженедельная сводка*

За последнюю неделю:
• Подано заявок: {total_applications}
• Получено откликов: {responded}
• Ожидают ответа: {pending}

{f"Коэффициент отклика: {(responded/total_applications*100):.1f}%" if total_applications > 0 else ""}

Продолжайте искать! Удачи в поиске работы! 🍀
            """
            
            await telegram_service._send_message(user.telegram_chat_id, summary)
            
            print(f"Отправлена еженедельная сводка для {user.email}")
        
    except Exception as e:
        print(f"Ошибка в еженедельной сводке: {e}")
    
    finally:
        db.close()

@celery_app.task
def check_job_responses():
    """Проверка откликов на заявки (если есть интеграция с почтой)"""
    
    # Эта задача может быть реализована для автоматической проверки
    # новых писем в почтовом ящике пользователя
    pass

@celery_app.task
def backup_data():
    """Резервное копирование данных"""
    
    # Задача для создания бэкапов базы данных
    pass

def _determine_experience_level(experience_years: int) -> str:
    """Определение уровня опыта по количеству лет"""
    
    if experience_years is None:
        return None
    
    if experience_years < 1:
        return 'junior'
    elif experience_years <= 3:
        return 'middle'
    else:
        return 'senior'

class JobSearchScheduler:
    """Класс для управления планировщиком поиска вакансий"""
    
    def __init__(self):
        self.is_running = False
    
    async def start_daily_search(self):
        """Запуск ежедневного поиска"""
        
        if self.is_running:
            return
        
        self.is_running = True
        
        while self.is_running:
            try:
                # Проверяем время - если 9:00, запускаем поиск
                now = datetime.now()
                if now.hour == 9 and now.minute == 0:
                    await _daily_job_search_async()
                
                # Ждем минуту перед следующей проверкой
                await asyncio.sleep(60)
                
            except Exception as e:
                print(f"Ошибка в планировщике: {e}")
                await asyncio.sleep(60)
    
    def stop_daily_search(self):
        """Остановка ежедневного поиска"""
        self.is_running = False
    
    async def run_search_now(self, user_id: int = None):
        """Запуск поиска прямо сейчас для конкретного пользователя или всех"""
        
        if user_id:
            await self._search_for_user(user_id)
        else:
            await _daily_job_search_async()
    
    async def _search_for_user(self, user_id: int):
        """Поиск вакансий для конкретного пользователя"""
        
        db = SessionLocal()
        
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return
            
            resume = db.query(Resume).filter(
                Resume.user_id == user_id
            ).order_by(Resume.created_at.desc()).first()
            
            if not resume:
                return
            
            job_scraper = JobScraper()
            telegram_service = TelegramService()
            
            keywords = resume.skills[:5] if resume.skills else []
            if resume.position_title:
                keywords.append(resume.position_title)
            
            jobs = await job_scraper.search_jobs(
                keywords=keywords,
                location=resume.location,
                experience_level=_determine_experience_level(resume.experience_years),
                limit=20
            )
            
            relevant_jobs = [job for job in jobs if job.get('match_score', 0) > 0.6]
            
            if relevant_jobs and user.telegram_chat_id:
                await telegram_service.send_jobs_notification(
                    user_chat_id=user.telegram_chat_id,
                    jobs=relevant_jobs,
                    user_id=user.id
                )
        
        finally:
            db.close()