import asyncio
import json
from typing import Dict, List, Any, Optional
import aiohttp
from datetime import datetime
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.telegram_notification import TelegramNotification
from app.models.user import User

class TelegramService:
    """Сервис для работы с Telegram Bot API"""
    
    def __init__(self):
        self.bot_token = settings.telegram_bot_token
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    async def send_notification(
        self, 
        notification: TelegramNotification, 
        db: Session
    ) -> bool:
        """Отправка уведомления в Telegram"""
        
        try:
            # Получаем пользователя
            user = db.query(User).filter(User.id == notification.user_id).first()
            if not user or not user.telegram_chat_id:
                return False
            
            # Формируем сообщение
            message_text = f"*{notification.title}*\n\n{notification.message}"
            
            # Подготавливаем данные для отправки
            data = {
                'chat_id': user.telegram_chat_id,
                'text': message_text,
                'parse_mode': 'Markdown'
            }
            
            # Добавляем кнопки если есть
            if notification.has_buttons and notification.buttons_data:
                data['reply_markup'] = json.dumps(
                    self._create_inline_keyboard(notification.buttons_data)
                )
            
            # Отправляем сообщение
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/sendMessage"
                
                async with session.post(url, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        # Сохраняем ID сообщения для возможности редактирования
                        if result.get('ok'):
                            notification.telegram_message_id = str(result['result']['message_id'])
                            notification.sent_at = datetime.utcnow()
                            db.commit()
                            return True
            
            return False
            
        except Exception as e:
            print(f"Ошибка отправки Telegram уведомления: {e}")
            return False
    
    async def send_jobs_notification(
        self,
        user_chat_id: str,
        jobs: List[Dict[str, Any]],
        user_id: int
    ) -> bool:
        """Отправка уведомления о найденных вакансиях с кнопками для выбора"""
        
        try:
            if not jobs:
                return False
            
            # Формируем сообщение
            message = f"🎯 *Найдено {len(jobs)} новых вакансий!*\n\n"
            
            # Добавляем топ-3 вакансии в сообщение
            for i, job in enumerate(jobs[:3], 1):
                match_score = job.get('match_score', 0)
                match_percent = int(match_score * 100) if match_score else 0
                
                salary_text = ""
                if job.get('salary_from') or job.get('salary_to'):
                    salary_from = job.get('salary_from', 0)
                    salary_to = job.get('salary_to', 0)
                    currency = job.get('currency', 'RUB')
                    
                    if salary_from and salary_to:
                        salary_text = f" ({salary_from:,}-{salary_to:,} {currency})"
                    elif salary_from:
                        salary_text = f" (от {salary_from:,} {currency})"
                
                message += f"{i}. *{job.get('title')}*\n"
                message += f"🏢 {job.get('company_name')}{salary_text}\n"
                message += f"📊 Соответствие: {match_percent}%\n\n"
            
            if len(jobs) > 3:
                message += f"... и еще {len(jobs) - 3} вакансий\n\n"
            
            message += "Выберите вакансии для отклика:"
            
            # Создаем кнопки для выбора вакансий
            keyboard = self._create_jobs_keyboard(jobs, user_id)
            
            data = {
                'chat_id': user_chat_id,
                'text': message,
                'parse_mode': 'Markdown',
                'reply_markup': json.dumps(keyboard)
            }
            
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/sendMessage"
                
                async with session.post(url, json=data) as response:
                    return response.status == 200
            
        except Exception as e:
            print(f"Ошибка отправки уведомления о вакансиях: {e}")
            return False
    
    async def handle_update(self, update: Dict[str, Any], db: Session):
        """Обработка обновлений от Telegram (callback_query, messages)"""
        
        try:
            # Обработка callback query (нажатия на кнопки)
            if 'callback_query' in update:
                await self._handle_callback_query(update['callback_query'], db)
            
            # Обработка текстовых сообщений
            elif 'message' in update:
                await self._handle_message(update['message'], db)
            
        except Exception as e:
            print(f"Ошибка обработки Telegram update: {e}")
    
    async def _handle_callback_query(self, callback_query: Dict[str, Any], db: Session):
        """Обработка нажатий на кнопки"""
        
        try:
            query_data = callback_query.get('data', '')
            chat_id = callback_query['from']['id']
            message_id = callback_query['message']['message_id']
            
            # Парсим данные кнопки
            if query_data.startswith('select_job_'):
                job_id = query_data.replace('select_job_', '')
                await self._handle_job_selection(chat_id, job_id, message_id, db)
            
            elif query_data.startswith('apply_jobs_'):
                user_id = query_data.replace('apply_jobs_', '')
                await self._handle_apply_jobs(chat_id, user_id, message_id, db)
            
            # Подтверждаем получение callback query
            await self._answer_callback_query(callback_query['id'])
            
        except Exception as e:
            print(f"Ошибка обработки callback query: {e}")
    
    async def _handle_message(self, message: Dict[str, Any], db: Session):
        """Обработка текстовых сообщений"""
        
        try:
            chat_id = message['chat']['id']
            text = message.get('text', '')
            
            # Команда /start
            if text == '/start':
                welcome_text = """
🤖 *Добро пожаловать в HR Assistant!*

Я помогу вам автоматизировать поиск работы:
• Ищу релевантные вакансии каждый день
• Анализирую соответствие вашему резюме
• Отправляю заявки и письма HR
• Уведомляю о результатах

Для начала работы зарегистрируйтесь на сайте и привяжите этот Telegram аккаунт.
                """
                
                await self._send_message(chat_id, welcome_text)
            
            # Команда /help
            elif text == '/help':
                help_text = """
📋 *Доступные команды:*

/start - Начать работу с ботом
/help - Показать это сообщение
/status - Статус последних заявок

🔧 *Как это работает:*
1. Загрузите резюме на сайте
2. Каждое утро бот ищет вакансии
3. Выбираете подходящие через Telegram
4. Бот автоматически отправляет заявки
                """
                
                await self._send_message(chat_id, help_text)
            
        except Exception as e:
            print(f"Ошибка обработки сообщения: {e}")
    
    async def _handle_job_selection(
        self, 
        chat_id: str, 
        job_id: str, 
        message_id: str, 
        db: Session
    ):
        """Обработка выбора вакансии"""
        
        # Логика выбора/отмены выбора вакансии
        # Можно сохранить выбор в сессии или временной таблице
        pass
    
    async def _handle_apply_jobs(
        self, 
        chat_id: str, 
        user_id: str, 
        message_id: str, 
        db: Session
    ):
        """Обработка подачи заявок на выбранные вакансии"""
        
        # Логика подачи заявок через API
        pass
    
    def _create_inline_keyboard(self, buttons_data: Dict[str, Any]) -> Dict[str, Any]:
        """Создание inline клавиатуры"""
        
        keyboard = {"inline_keyboard": []}
        
        # Простой пример создания кнопок
        if 'buttons' in buttons_data:
            for button in buttons_data['buttons']:
                keyboard["inline_keyboard"].append([{
                    "text": button['text'],
                    "callback_data": button['callback_data']
                }])
        
        return keyboard
    
    def _create_jobs_keyboard(self, jobs: List[Dict[str, Any]], user_id: int) -> Dict[str, Any]:
        """Создание клавиатуры для выбора вакансий"""
        
        keyboard = {"inline_keyboard": []}
        
        # Добавляем кнопки для каждой вакансии (максимум 10)
        for i, job in enumerate(jobs[:10]):
            job_id = job.get('id') or job.get('external_id')
            title = job.get('title', 'Вакансия')[:30] + ("..." if len(job.get('title', '')) > 30 else "")
            
            keyboard["inline_keyboard"].append([{
                "text": f"{'☑️' if job.get('selected') else '⬜'} {title}",
                "callback_data": f"select_job_{job_id}"
            }])
        
        # Кнопка "Подать заявки на выбранные"
        keyboard["inline_keyboard"].append([{
            "text": "📤 Подать заявки на выбранные",
            "callback_data": f"apply_jobs_{user_id}"
        }])
        
        # Кнопка "Посмотреть все"
        keyboard["inline_keyboard"].append([{
            "text": "📋 Посмотреть все вакансии",
            "url": f"{settings.frontend_url}/jobs"
        }])
        
        return keyboard
    
    async def _send_message(self, chat_id: str, text: str, **kwargs) -> bool:
        """Отправка простого сообщения"""
        
        try:
            data = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': kwargs.get('parse_mode', 'Markdown')
            }
            
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/sendMessage"
                
                async with session.post(url, json=data) as response:
                    return response.status == 200
            
        except Exception as e:
            print(f"Ошибка отправки сообщения: {e}")
            return False
    
    async def _answer_callback_query(self, callback_query_id: str, text: str = None) -> bool:
        """Подтверждение callback query"""
        
        try:
            data = {'callback_query_id': callback_query_id}
            if text:
                data['text'] = text
            
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/answerCallbackQuery"
                
                async with session.post(url, json=data) as response:
                    return response.status == 200
            
        except Exception as e:
            print(f"Ошибка подтверждения callback query: {e}")
            return False
    
    async def setup_webhook(self, webhook_url: str = None) -> bool:
        """Настройка webhook для бота"""
        
        try:
            url = webhook_url or f"{settings.frontend_url.replace('3000', '8000')}/api/telegram/webhook"
            
            data = {'url': url}
            
            async with aiohttp.ClientSession() as session:
                webhook_url_api = f"{self.base_url}/setWebhook"
                
                async with session.post(webhook_url_api, json=data) as response:
                    return response.status == 200
            
        except Exception as e:
            print(f"Ошибка настройки webhook: {e}")
            return False
    
    async def delete_webhook(self) -> bool:
        """Удаление webhook"""
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/deleteWebhook"
                
                async with session.post(url) as response:
                    return response.status == 200
            
        except Exception as e:
            print(f"Ошибка удаления webhook: {e}")
            return False