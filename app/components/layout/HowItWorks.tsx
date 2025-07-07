import { Upload, Search, MessageSquare, Send } from 'lucide-react';

export function HowItWorks() {
  const steps = [
    {
      icon: Upload,
      title: 'Загрузите резюме',
      description: 'Загрузите ваше резюме в формате PDF, DOC или DOCX. ИИ автоматически проанализирует ваши навыки и опыт.',
      step: 1,
    },
    {
      icon: Search,
      title: 'Автоматический поиск',
      description: 'Каждое утро система ищет новые вакансии, соответствующие вашему профилю на популярных job-сайтах.',
      step: 2,
    },
    {
      icon: MessageSquare,
      title: 'Выберите вакансии',
      description: 'Получайте уведомления в Telegram с лучшими предложениями и выбирайте интересные позиции.',
      step: 3,
    },
    {
      icon: Send,
      title: 'Автоматический отклик',
      description: 'Система автоматически отправит ваше резюме и персонализированное письмо HR-специалистам.',
      step: 4,
    },
  ];

  return (
    <section className="py-20 bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Как это работает
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Всего 4 простых шага от загрузки резюме до получения приглашений на собеседование
          </p>
        </div>

        <div className="relative">
          {/* Connection line for desktop */}
          <div className="hidden lg:block absolute top-16 left-1/2 transform -translate-x-1/2 w-full max-w-4xl">
            <div className="flex justify-between">
              {steps.slice(0, -1).map((_, index) => (
                <div key={index} className="flex-1 h-0.5 bg-primary-200 mt-6 mx-8"></div>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 relative z-10">
            {steps.map((step, index) => (
              <div key={index} className="text-center">
                {/* Step number */}
                <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-600 text-white text-xl font-bold rounded-full mb-4">
                  {step.step}
                </div>
                
                {/* Icon */}
                <div className="inline-flex items-center justify-center w-16 h-16 bg-white border-2 border-primary-100 rounded-xl shadow-sm mb-4">
                  <step.icon className="h-8 w-8 text-primary-600" />
                </div>

                {/* Content */}
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {step.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {step.description}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* CTA */}
        <div className="text-center mt-16">
          <a
            href="/resume/upload"
            className="btn-primary inline-flex items-center space-x-2 text-lg px-8 py-3"
          >
            <Upload className="h-5 w-5" />
            <span>Начать сейчас</span>
          </a>
          <p className="text-sm text-gray-500 mt-2">
            Бесплатно • Без обязательств • Результат за 24 часа
          </p>
        </div>
      </div>
    </section>
  );
}