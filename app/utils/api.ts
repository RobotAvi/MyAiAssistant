const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Типы для API ответов
export interface User {
  id: number;
  email: string;
  full_name: string;
  telegram_chat_id?: string;
  is_active: boolean;
}

export interface Resume {
  id: number;
  filename: string;
  position_title?: string;
  skills: string[];
  experience_years?: number;
  location?: string;
  created_at: string;
}

export interface Job {
  id: number;
  title: string;
  company_name: string;
  description?: string;
  salary_from?: number;
  salary_to?: number;
  currency: string;
  location?: string;
  url: string;
  match_score?: number;
  llm_analysis?: string;
  platform: string;
  created_at: string;
}

export interface JobApplication {
  id: number;
  job: Job;
  status: string;
  applied_at: string;
  response_received: boolean;
  emails_sent_count: number;
}

// Утилиты для HTTP запросов
class ApiClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Методы для работы с пользователями
  async createUser(userData: {
    email: string;
    full_name: string;
    telegram_chat_id?: string;
    email_password?: string;
  }): Promise<User> {
    return this.request<User>('/users/', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async getUser(userId: number): Promise<User> {
    return this.request<User>(`/users/${userId}`);
  }

  async updateUser(userId: number, userData: Partial<User>): Promise<User> {
    return this.request<User>(`/users/${userId}`, {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
  }

  // Методы для работы с резюме
  async uploadResume(userId: number, file: File): Promise<Resume> {
    const formData = new FormData();
    formData.append('file', file);

    return this.request<Resume>(`/resumes/upload/${userId}`, {
      method: 'POST',
      headers: {}, // Убираем Content-Type для FormData
      body: formData,
    });
  }

  async getUserResumes(userId: number): Promise<Resume[]> {
    return this.request<Resume[]>(`/resumes/user/${userId}`);
  }

  async getResume(resumeId: number): Promise<Resume> {
    return this.request<Resume>(`/resumes/${resumeId}`);
  }

  async deleteResume(resumeId: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/resumes/${resumeId}`, {
      method: 'DELETE',
    });
  }

  // Методы для работы с вакансиями
  async searchJobs(params: {
    user_id: number;
    keywords?: string[];
    location?: string;
    salary_from?: number;
    experience_level?: string;
  }): Promise<Job[]> {
    return this.request<Job[]>('/jobs/search', {
      method: 'POST',
      body: JSON.stringify(params),
    });
  }

  async applyToJobs(
    userId: number,
    applicationData: {
      job_ids: number[];
      resume_id: number;
      custom_cover_letter?: string;
    }
  ): Promise<{ success: boolean; message: string; results: any[] }> {
    return this.request(`/jobs/apply?user_id=${userId}`, {
      method: 'POST',
      body: JSON.stringify(applicationData),
    });
  }

  async getUserApplications(userId: number): Promise<JobApplication[]> {
    return this.request<JobApplication[]>(`/jobs/applications/${userId}`);
  }

  // Методы для работы с Telegram
  async sendNotification(notificationData: {
    user_id: number;
    notification_type: string;
    title: string;
    message: string;
    data?: any;
    buttons_data?: any;
  }): Promise<any> {
    return this.request('/telegram/send-notification', {
      method: 'POST',
      body: JSON.stringify(notificationData),
    });
  }

  async getUserNotifications(userId: number): Promise<any[]> {
    return this.request<any[]>(`/telegram/notifications/${userId}`);
  }

  async setupTelegramWebhook(): Promise<{ message: string }> {
    return this.request<{ message: string }>('/telegram/setup-webhook', {
      method: 'POST',
    });
  }
}

// Экспортируем экземпляр API клиента
export const apiClient = new ApiClient(API_BASE_URL);

// Утилитарные функции
export const formatSalary = (from?: number, to?: number, currency = 'RUB') => {
  if (!from && !to) return 'Не указана';
  
  const formatter = new Intl.NumberFormat('ru-RU');
  
  if (from && to) {
    return `${formatter.format(from)} - ${formatter.format(to)} ${currency}`;
  } else if (from) {
    return `от ${formatter.format(from)} ${currency}`;
  } else if (to) {
    return `до ${formatter.format(to)} ${currency}`;
  }
  
  return 'Не указана';
};

export const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

export const getMatchScoreColor = (score?: number) => {
  if (!score) return 'text-gray-500';
  
  if (score >= 0.8) return 'text-green-600';
  if (score >= 0.6) return 'text-yellow-600';
  return 'text-red-600';
};

export const getMatchScoreBadgeColor = (score?: number) => {
  if (!score) return 'bg-gray-100 text-gray-800';
  
  if (score >= 0.8) return 'bg-green-100 text-green-800';
  if (score >= 0.6) return 'bg-yellow-100 text-yellow-800';
  return 'bg-red-100 text-red-800';
};