import requests
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from urllib.parse import quote, urljoin
import json
import time
import random

class JobScraper:
    """Сервис для поиска и парсинга вакансий с различных платформ"""
    
    def __init__(self):
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    async def search_jobs(
        self,
        keywords: List[str] = None,
        location: str = None,
        salary_from: int = None,
        experience_level: str = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Поиск вакансий на различных платформах"""
        
        all_jobs = []
        
        # Поиск на HeadHunter
        hh_jobs = await self._search_headhunter(
            keywords, location, salary_from, experience_level, limit // 2
        )
        all_jobs.extend(hh_jobs)
        
        # Поиск на SuperJob (если есть API ключ)
        # sj_jobs = await self._search_superjob(keywords, location, salary_from, experience_level, limit // 2)
        # all_jobs.extend(sj_jobs)
        
        # Можно добавить другие платформы
        
        return all_jobs[:limit]
    
    async def _search_headhunter(
        self,
        keywords: List[str] = None,
        location: str = None,
        salary_from: int = None,
        experience_level: str = None,
        limit: int = 25
    ) -> List[Dict[str, Any]]:
        """Поиск вакансий на HeadHunter через API"""
        
        base_url = "https://api.hh.ru/vacancies"
        
        # Формируем параметры запроса
        params = {
            'per_page': min(limit, 100),  # Максимум 100 за запрос
            'page': 0,
            'area': 1,  # Москва по умолчанию
            'only_with_salary': 'true' if salary_from else 'false'
        }
        
        # Добавляем ключевые слова
        if keywords:
            params['text'] = ' '.join(keywords)
        
        # Добавляем зарплату
        if salary_from:
            params['salary'] = salary_from
        
        # Уровень опыта
        experience_mapping = {
            'junior': 'noExperience',
            'middle': 'between1And3',
            'senior': 'between3And6'
        }
        if experience_level and experience_level.lower() in experience_mapping:
            params['experience'] = experience_mapping[experience_level.lower()]
        
        jobs = []
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, params=params, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        for item in data.get('items', []):
                            job = await self._parse_hh_vacancy(item, session)
                            if job:
                                jobs.append(job)
                                
                        # Небольшая задержка для соблюдения лимитов API
                        await asyncio.sleep(0.5)
                    
        except Exception as e:
            print(f"Ошибка поиска на HeadHunter: {e}")
        
        return jobs
    
    async def _parse_hh_vacancy(self, item: dict, session: aiohttp.ClientSession) -> Optional[Dict[str, Any]]:
        """Парсинг отдельной вакансии с HeadHunter"""
        
        try:
            # Получаем подробную информацию о вакансии
            detail_url = item.get('url')
            if not detail_url:
                return None
            
            async with session.get(detail_url, headers=self.headers) as response:
                if response.status != 200:
                    return None
                
                detail_data = await response.json()
                
                # Парсим контакты HR
                hr_contacts = []
                contacts = detail_data.get('contacts')
                if contacts:
                    if contacts.get('email'):
                        hr_contacts.append({
                            'email': contacts['email'],
                            'name': contacts.get('name', 'HR'),
                            'phone': contacts.get('phones', [{}])[0].get('formatted') if contacts.get('phones') else None
                        })
                
                # Извлекаем информацию о компании
                employer = detail_data.get('employer', {})
                company_contacts = {
                    'company_url': employer.get('alternate_url'),
                    'company_site': employer.get('site_url')
                }
                
                salary = item.get('salary', {})
                
                job_data = {
                    'external_id': str(item['id']),
                    'platform': 'headhunter',
                    'title': item['name'],
                    'company_name': employer.get('name', 'Неизвестная компания'),
                    'description': detail_data.get('description', ''),
                    'requirements': self._extract_requirements(detail_data.get('description', '')),
                    'salary_from': salary.get('from') if salary else None,
                    'salary_to': salary.get('to') if salary else None,
                    'currency': salary.get('currency') if salary else 'RUB',
                    'location': item.get('area', {}).get('name'),
                    'employment_type': item.get('employment', {}).get('name'),
                    'experience_level': item.get('experience', {}).get('name'),
                    'url': item['alternate_url'],
                    'hr_contacts': hr_contacts,
                    'company_contacts': company_contacts,
                    'published_at': item.get('published_at')
                }
                
                return job_data
                
        except Exception as e:
            print(f"Ошибка парсинга вакансии HH: {e}")
            return None
    
    def _extract_requirements(self, description: str) -> str:
        """Извлечение требований из описания вакансии"""
        
        if not description:
            return ""
        
        # Убираем HTML теги
        soup = BeautifulSoup(description, 'html.parser')
        text = soup.get_text()
        
        # Ищем секцию с требованиями
        lines = text.split('\n')
        requirements_lines = []
        in_requirements = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Начало секции требований
            if any(keyword in line.lower() for keyword in ['требования', 'требуется', 'навыки', 'опыт работы']):
                in_requirements = True
                requirements_lines.append(line)
                continue
            
            # Конец секции требований
            if in_requirements and any(keyword in line.lower() for keyword in ['условия', 'предлагаем', 'мы предлагаем', 'обязанности']):
                break
            
            if in_requirements:
                requirements_lines.append(line)
        
        return '\n'.join(requirements_lines)
    
    async def _search_superjob(
        self,
        keywords: List[str] = None,
        location: str = None,
        salary_from: int = None,
        experience_level: str = None,
        limit: int = 25
    ) -> List[Dict[str, Any]]:
        """Поиск вакансий на SuperJob (требует API ключ)"""
        
        # Реализация для SuperJob API
        # Требует регистрации приложения и получения API ключа
        
        return []
    
    async def find_hr_contacts(self, company_name: str, job_url: str) -> List[Dict[str, str]]:
        """Поиск контактов HR специалистов компании"""
        
        contacts = []
        
        try:
            # Поиск на LinkedIn (требует авторизации)
            # linkedin_contacts = await self._search_linkedin_hr(company_name)
            # contacts.extend(linkedin_contacts)
            
            # Поиск в социальных сетях
            # social_contacts = await self._search_social_media_hr(company_name)
            # contacts.extend(social_contacts)
            
            # Пока возвращаем пустой список
            # В реальной реализации здесь будет поиск контактов
            pass
            
        except Exception as e:
            print(f"Ошибка поиска HR контактов: {e}")
        
        return contacts
    
    async def _search_linkedin_hr(self, company_name: str) -> List[Dict[str, str]]:
        """Поиск HR контактов в LinkedIn"""
        
        # Требует авторизации в LinkedIn
        # Можно использовать selenium для автоматизации
        
        return []
    
    def _delay_between_requests(self):
        """Задержка между запросами для соблюдения лимитов"""
        time.sleep(random.uniform(1, 3))