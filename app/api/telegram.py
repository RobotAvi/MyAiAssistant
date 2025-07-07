from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.db.database import get_db
from app.models.telegram_notification import TelegramNotification
from app.services.telegram_service import TelegramService

router = APIRouter()

class NotificationResponse(BaseModel):
    id: int
    notification_type: str
    title: str
    message: str
    is_sent: bool
    created_at: str
    
    class Config:
        from_attributes = True

class SendNotificationRequest(BaseModel):
    user_id: int
    notification_type: str
    title: str
    message: str
    data: dict = None
    buttons_data: dict = None

@router.post("/webhook")
async def telegram_webhook(update: dict, db: Session = Depends(get_db)):
    """Обработка webhook от Telegram Bot"""
    
    try:
        telegram_service = TelegramService()
        await telegram_service.handle_update(update, db)
        return {"status": "ok"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки webhook: {str(e)}")

@router.post("/send-notification", response_model=NotificationResponse)
async def send_notification(
    notification_request: SendNotificationRequest,
    db: Session = Depends(get_db)
):
    """Отправка уведомления в Telegram"""
    
    try:
        # Создаем уведомление в БД
        notification = TelegramNotification(
            user_id=notification_request.user_id,
            notification_type=notification_request.notification_type,
            title=notification_request.title,
            message=notification_request.message,
            data=notification_request.data,
            has_buttons=bool(notification_request.buttons_data),
            buttons_data=notification_request.buttons_data
        )
        
        db.add(notification)
        db.commit()
        db.refresh(notification)
        
        # Отправляем через Telegram
        telegram_service = TelegramService()
        success = await telegram_service.send_notification(notification, db)
        
        if success:
            notification.is_sent = True
            db.commit()
        
        return notification
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка отправки уведомления: {str(e)}")

@router.get("/notifications/{user_id}", response_model=List[NotificationResponse])
async def get_user_notifications(user_id: int, db: Session = Depends(get_db)):
    """Получение всех уведомлений пользователя"""
    
    notifications = db.query(TelegramNotification).filter(
        TelegramNotification.user_id == user_id
    ).order_by(TelegramNotification.created_at.desc()).all()
    
    return notifications

@router.post("/setup-webhook")
async def setup_webhook():
    """Настройка webhook для Telegram Bot"""
    
    try:
        telegram_service = TelegramService()
        success = await telegram_service.setup_webhook()
        
        if success:
            return {"message": "Webhook успешно настроен"}
        else:
            raise HTTPException(status_code=500, detail="Ошибка настройки webhook")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка настройки webhook: {str(e)}")

@router.delete("/webhook")
async def delete_webhook():
    """Удаление webhook"""
    
    try:
        telegram_service = TelegramService()
        success = await telegram_service.delete_webhook()
        
        if success:
            return {"message": "Webhook успешно удален"}
        else:
            raise HTTPException(status_code=500, detail="Ошибка удаления webhook")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка удаления webhook: {str(e)}")