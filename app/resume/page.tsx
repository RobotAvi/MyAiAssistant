import Link from 'next/link';
import { Plus, FileText, Calendar, Star } from 'lucide-react';
import { ResumeCard } from './components/ResumeCard';

// Пример данных - в реальном приложении будет загружаться с API
const mockResumes = [
  {
    id: 1,
    filename: 'Иванов_Иван_Frontend.pdf',
    position_title: 'Frontend Developer',
    skills: ['React', 'TypeScript', 'Node.js', 'CSS'],
    experience_years: 3,
    location: 'Москва',
    created_at: '2024-01-15',
    isActive: true,
  },
  {
    id: 2,
    filename: 'Иванов_Иван_Fullstack.pdf',
    position_title: 'Fullstack Developer',
    skills: ['React', 'Python', 'PostgreSQL', 'Docker'],
    experience_years: 3,
    location: 'Москва',
    created_at: '2024-01-10',
    isActive: false,
  },
];

export default function ResumePage() {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Мои резюме
          </h1>
          <p className="text-gray-600">
            Управляйте своими резюме и настройками поиска вакансий
          </p>
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <Link
            href="/resume/upload"
            className="btn-primary inline-flex items-center space-x-2"
          >
            <Plus className="h-4 w-4" />
            <span>Загрузить новое резюме</span>
          </Link>
          
          <Link
            href="/jobs/search"
            className="btn-secondary inline-flex items-center space-x-2"
          >
            <Star className="h-4 w-4" />
            <span>Найти вакансии</span>
          </Link>
        </div>

        {/* Resumes Grid */}
        {mockResumes.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockResumes.map((resume) => (
              <ResumeCard key={resume.id} resume={resume} />
            ))}
          </div>
        ) : (
          /* Empty State */
          <div className="text-center py-12">
            <FileText className="h-16 w-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              У вас пока нет резюме
            </h3>
            <p className="text-gray-600 mb-6">
              Загрузите ваше первое резюме, чтобы начать автоматический поиск вакансий
            </p>
            <Link
              href="/resume/upload"
              className="btn-primary inline-flex items-center space-x-2"
            >
              <Plus className="h-4 w-4" />
              <span>Загрузить резюме</span>
            </Link>
          </div>
        )}

        {/* Info Cards */}
        {mockResumes.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                💡 Советы по резюме
              </h3>
              <ul className="space-y-2 text-gray-600">
                <li>• Обновляйте резюме каждые 3-6 месяцев</li>
                <li>• Адаптируйте резюме под разные позиции</li>
                <li>• Указывайте конкретные достижения с цифрами</li>
                <li>• Проверяйте орфографию и грамматику</li>
              </ul>
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                📊 Статистика поиска
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Найдено вакансий за месяц:</span>
                  <span className="font-semibold">127</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Подано заявок:</span>
                  <span className="font-semibold">23</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Получено откликов:</span>
                  <span className="font-semibold text-green-600">8</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}