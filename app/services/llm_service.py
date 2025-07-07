import openai
import json
from typing import Dict, List, Any
from app.core.config import settings

class LLMService:
    def __init__(self):
        openai.api_key = settings.openai_api_key
    
    async def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """Анализ резюме с помощью LLM"""
        
        prompt = f"""
        Проанализируй следующее резюме и извлеки ключевую информацию в формате JSON:

        Резюме:
        {resume_text}

        Верни JSON с полями:
        - skills: список навыков (массив строк)
        - experience_years: количество лет опыта (число)
        - position_title: желаемая должность (строка)
        - location: местоположение (строка)
        - salary_expectation: ожидаемая зарплата (строка)

        Отвечай только JSON без дополнительного текста.
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты эксперт по анализу резюме. Анализируй резюме и возвращай структурированные данные в JSON формате."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            print(f"Ошибка анализа резюме: {e}")
            return {
                "skills": [],
                "experience_years": 0,
                "position_title": "",
                "location": "",
                "salary_expectation": ""
            }
    
    async def analyze_job_match(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Анализ соответствия резюме и вакансии"""
        
        prompt = f"""
        Оцени соответствие резюме и вакансии по шкале от 0 до 1 (где 1 - идеальное соответствие).
        Проанализируй навыки, опыт, требования.

        Резюме:
        {resume_text[:2000]}...

        Описание вакансии:
        {job_description[:2000]}...

        Верни JSON с полями:
        - score: оценка соответствия от 0 до 1 (число)
        - analysis: краткий анализ соответствия (строка до 200 символов)
        - matching_skills: совпадающие навыки (массив строк)
        - missing_skills: недостающие навыки (массив строк)

        Отвечай только JSON.
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты эксперт по подбору персонала. Анализируй соответствие кандидата и вакансии."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=400
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            print(f"Ошибка анализа соответствия: {e}")
            return {
                "score": 0.5,
                "analysis": "Не удалось проанализировать соответствие",
                "matching_skills": [],
                "missing_skills": []
            }
    
    async def generate_cover_letter(
        self, 
        resume_text: str, 
        job_description: str, 
        company_name: str
    ) -> str:
        """Генерация сопроводительного письма"""
        
        prompt = f"""
        Напиши персонализированное сопроводительное письмо для соискателя работы.

        Информация о кандидате (из резюме):
        {resume_text[:1500]}...

        Описание вакансии:
        {job_description[:1500]}...

        Название компании: {company_name}

        Требования к письму:
        - Длина: 150-250 слов
        - Профессиональный тон
        - Подчеркни соответствие навыков требованиям
        - Покажи интерес к компании
        - Избегай шаблонных фраз
        - Пиши на русском языке

        Верни только текст письма без дополнительных комментариев.
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты эксперт по написанию сопроводительных писем для поиска работы."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=400
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Ошибка генерации письма: {e}")
            return f"Здравствуйте!\n\nЯ заинтересован в вакансии в компании {company_name}. Мой опыт и навыки соответствуют требованиям позиции.\n\nБуду рад обсудить детали.\n\nС уважением"
    
    async def create_embedding(self, text: str) -> List[float]:
        """Создание векторного представления текста"""
        
        try:
            response = await openai.Embedding.acreate(
                model="text-embedding-ada-002",
                input=text[:8000]  # Ограничение OpenAI
            )
            
            return response.data[0].embedding
            
        except Exception as e:
            print(f"Ошибка создания embedding: {e}")
            return []
    
    async def generate_hr_email(
        self,
        candidate_name: str,
        job_title: str,
        company_name: str,
        cover_letter: str
    ) -> Dict[str, str]:
        """Генерация письма для HR"""
        
        prompt = f"""
        Напиши профессиональное письмо HR-специалисту от имени кандидата.

        Данные:
        - Имя кандидата: {candidate_name}
        - Должность: {job_title}
        - Компания: {company_name}
        - Сопроводительное письмо: {cover_letter}

        Создай:
        1. Тему письма (до 60 символов)
        2. Текст письма (150-200 слов)

        Требования:
        - Профессиональный тон
        - Конкретность
        - Интерес к компании
        - Русский язык

        Верни JSON с полями: subject, body
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты эксперт по деловой переписке и рекрутингу."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=350
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            print(f"Ошибка генерации HR письма: {e}")
            return {
                "subject": f"Отклик на вакансию {job_title}",
                "body": f"Здравствуйте!\n\nМеня заинтересовала вакансия {job_title} в {company_name}.\n\n{cover_letter}\n\nБуду рад возможности обсудить мою кандидатуру.\n\nС уважением,\n{candidate_name}"
            }