import smtplib
import ssl
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from email.mime.base import MimeBase
from email import encoders
import os
from typing import Optional, Dict, Any
from app.core.config import settings
from app.services.llm_service import LLMService

class EmailService:
    """Сервис для отправки email писем"""
    
    def __init__(self):
        self.smtp_server = settings.smtp_server
        self.smtp_port = settings.smtp_port
        self.llm_service = LLMService()
    
    async def send_application_email(
        self,
        user_email: str,
        user_password: str,
        hr_email: str,
        job_title: str,
        company_name: str,
        cover_letter: str,
        resume_path: str,
        candidate_name: str = None
    ) -> bool:
        """Отправка заявки на вакансию HR"""
        
        try:
            # Генерируем письмо с помощью LLM
            if not candidate_name:
                candidate_name = user_email.split('@')[0]
            
            email_content = await self.llm_service.generate_hr_email(
                candidate_name=candidate_name,
                job_title=job_title,
                company_name=company_name,
                cover_letter=cover_letter
            )
            
            # Создаем сообщение
            message = MimeMultipart()
            message["From"] = user_email
            message["To"] = hr_email
            message["Subject"] = email_content["subject"]
            
            # Добавляем текст письма
            message.attach(MimeText(email_content["body"], "plain", "utf-8"))
            
            # Прикрепляем резюме
            if os.path.exists(resume_path):
                with open(resume_path, "rb") as attachment:
                    part = MimeBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                
                filename = os.path.basename(resume_path)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {filename}'
                )
                
                message.attach(part)
            
            # Отправляем письмо
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(user_email, user_password)
                server.sendmail(user_email, hr_email, message.as_string())
            
            return True
            
        except Exception as e:
            print(f"Ошибка отправки email: {e}")
            return False
    
    async def send_notification_email(
        self,
        user_email: str,
        user_password: str,
        subject: str,
        body: str,
        recipient_email: str = None
    ) -> bool:
        """Отправка уведомления по email"""
        
        try:
            recipient = recipient_email or user_email
            
            message = MimeMultipart()
            message["From"] = user_email
            message["To"] = recipient
            message["Subject"] = subject
            
            message.attach(MimeText(body, "plain", "utf-8"))
            
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(user_email, user_password)
                server.sendmail(user_email, recipient, message.as_string())
            
            return True
            
        except Exception as e:
            print(f"Ошибка отправки уведомления: {e}")
            return False
    
    async def send_job_digest(
        self,
        user_email: str,
        user_password: str,
        jobs: list,
        recipient_email: str = None
    ) -> bool:
        """Отправка дайджеста найденных вакансий"""
        
        try:
            recipient = recipient_email or user_email
            
            # Формируем HTML письмо с вакансиями
            html_body = self._create_jobs_html(jobs)
            
            message = MimeMultipart("alternative")
            message["From"] = user_email
            message["To"] = recipient
            message["Subject"] = f"HR Assistant: Найдено {len(jobs)} новых вакансий"
            
            # Добавляем HTML версию
            html_part = MimeText(html_body, "html", "utf-8")
            message.attach(html_part)
            
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(user_email, user_password)
                server.sendmail(user_email, recipient, message.as_string())
            
            return True
            
        except Exception as e:
            print(f"Ошибка отправки дайджеста: {e}")
            return False
    
    def _create_jobs_html(self, jobs: list) -> str:
        """Создание HTML для списка вакансий"""
        
        html = """
        <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    .job { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
                    .job-title { font-size: 18px; font-weight: bold; color: #333; }
                    .company { color: #666; margin: 5px 0; }
                    .salary { color: #008000; font-weight: bold; }
                    .match-score { background: #007bff; color: white; padding: 2px 8px; border-radius: 3px; font-size: 12px; }
                    .location { color: #888; }
                    .description { margin: 10px 0; line-height: 1.4; }
                    .link { color: #007bff; text-decoration: none; }
                </style>
            </head>
            <body>
                <h2>🎯 Новые вакансии для вас</h2>
                <p>HR Assistant нашел новые вакансии, соответствующие вашему резюме:</p>
        """
        
        for job in jobs[:10]:  # Показываем максимум 10 вакансий
            salary_text = ""
            if job.get('salary_from') or job.get('salary_to'):
                salary_from = job.get('salary_from', 0)
                salary_to = job.get('salary_to', 0)
                currency = job.get('currency', 'RUB')
                
                if salary_from and salary_to:
                    salary_text = f"{salary_from:,} - {salary_to:,} {currency}"
                elif salary_from:
                    salary_text = f"от {salary_from:,} {currency}"
                elif salary_to:
                    salary_text = f"до {salary_to:,} {currency}"
            
            match_score = job.get('match_score', 0)
            match_percent = int(match_score * 100) if match_score else 0
            
            description = job.get('llm_analysis', job.get('description', ''))[:200] + "..."
            
            html += f"""
                <div class="job">
                    <div class="job-title">{job.get('title', 'Без названия')}</div>
                    <div class="company">🏢 {job.get('company_name', 'Неизвестная компания')}</div>
                    {f'<div class="salary">💰 {salary_text}</div>' if salary_text else ''}
                    <div class="location">📍 {job.get('location', 'Не указано')}</div>
                    <div style="margin: 8px 0;">
                        <span class="match-score">Соответствие: {match_percent}%</span>
                    </div>
                    <div class="description">{description}</div>
                    <div style="margin-top: 10px;">
                        <a href="{job.get('url', '#')}" class="link">Посмотреть вакансию</a>
                    </div>
                </div>
            """
        
        html += """
                <div style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px;">
                    <p><strong>Что дальше?</strong></p>
                    <p>Перейдите в HR Assistant, чтобы выбрать интересные вакансии и отправить заявки автоматически.</p>
                </div>
            </body>
        </html>
        """
        
        return html
    
    def validate_email_settings(self, email: str, password: str) -> bool:
        """Проверка настроек email"""
        
        try:
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(email, password)
            
            return True
            
        except Exception as e:
            print(f"Ошибка проверки email настроек: {e}")
            return False