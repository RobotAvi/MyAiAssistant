from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class TelegramNotification(Base):
    __tablename__ = "telegram_notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Тип уведомления
    notification_type = Column(String, nullable=False)  # jobs_found, application_sent, response_received
    
    # Содержимое
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    data = Column(JSON)  # Дополнительные данные (список вакансий, статусы и т.д.)
    
    # Статус
    is_sent = Column(Boolean, default=False)
    sent_at = Column(DateTime)
    telegram_message_id = Column(String)  # ID сообщения в Telegram для редактирования
    
    # Интерактивные кнопки
    has_buttons = Column(Boolean, default=False)
    buttons_data = Column(JSON)  # Данные для кнопок
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    user = relationship("User", back_populates="notifications")