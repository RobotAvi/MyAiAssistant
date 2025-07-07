from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.db.database import get_db
from app.models.user import User

router = APIRouter()

class UserCreate(BaseModel):
    email: str
    full_name: str
    telegram_chat_id: str = None
    email_password: str = None

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    telegram_chat_id: str = None
    is_active: bool
    
    class Config:
        from_attributes = True

@router.post("/", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Создание нового пользователя"""
    # Проверяем, что пользователь с таким email не существует
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
    
    # Создаем пользователя
    db_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        telegram_chat_id=user_data.telegram_chat_id,
        email_password=user_data.email_password  # В реальности нужно шифровать
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Получение информации о пользователе"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserCreate, db: Session = Depends(get_db)):
    """Обновление информации о пользователе"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    user.email = user_data.email
    user.full_name = user_data.full_name
    user.telegram_chat_id = user_data.telegram_chat_id
    if user_data.email_password:
        user.email_password = user_data.email_password
    
    db.commit()
    db.refresh(user)
    
    return user