from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    telegram_chat_id = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Email настройки
    email_smtp_server = Column(String, default="smtp.gmail.com")
    email_smtp_port = Column(Integer, default=587)
    email_password = Column(String)  # Зашифрованный пароль
    
    # Связи
    resumes = relationship("Resume", back_populates="user")
    job_applications = relationship("JobApplication", back_populates="user")
    notifications = relationship("TelegramNotification", back_populates="user")