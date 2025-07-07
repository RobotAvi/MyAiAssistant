import { Search, Brain, MessageSquare, Mail, BarChart3, Zap } from 'lucide-react';

export function Features() {
  const features = [
    {
      icon: Search,
      title: 'Автоматический поиск',
      description: 'Ежедневный поиск вакансий на HeadHunter, LinkedIn и других платформах',
    },
    {
      icon: Brain,
      title: 'ИИ анализ',
      description: 'Умный анализ соответствия вашего резюме требованиям вакансий',
    },
    {
      icon: MessageSquare,
      title: 'Telegram уведомления',
      description: 'Получайте уведомления о новых вакансиях прямо в Telegram',
    },
    {
      icon: Mail,
      title: 'Автоматическая отправка',
      description: 'Автоматическая отправка резюме и писем HR-специалистам',
    },
    {
      icon: BarChart3,
      title: 'Аналитика',
      description: 'Подробная статистика откликов и советы по улучшению резюме',
    },
    {
      icon: Zap,
      title: 'Экономия времени',
      description: 'Сократите время поиска работы в 10 раз с автоматизацией',
    },
  ];

  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Как HR Assistant упростит ваш поиск работы
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Мощные функции искусственного интеллекта для автоматизации 
            всего процесса поиска и отклика на вакансии
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="group p-6 rounded-xl bg-gray-50 hover:bg-white hover:shadow-lg transition-all duration-300 border hover:border-primary-200"
            >
              <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-100 group-hover:bg-primary-600 text-primary-600 group-hover:text-white rounded-lg mb-4 transition-colors">
                <feature.icon className="h-6 w-6" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600 leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}