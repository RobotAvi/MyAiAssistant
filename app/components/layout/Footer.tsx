import Link from 'next/link';
import { Bot, Github, Mail, MessageCircle } from 'lucide-react';

export function Footer() {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Logo and Description */}
          <div className="md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <Bot className="h-8 w-8 text-primary-400" />
              <span className="text-xl font-bold">HR Assistant</span>
            </div>
            <p className="text-gray-300 mb-4 max-w-md">
              Автоматизированный HR-ассистент, который поможет вам найти работу мечты. 
              Используя искусственный интеллект, мы анализируем вакансии и подбираем 
              наиболее подходящие предложения.
            </p>
            <div className="flex space-x-4">
              <a
                href="https://github.com/your-repo"
                className="text-gray-400 hover:text-white transition-colors"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Github className="h-5 w-5" />
              </a>
              <a
                href="mailto:support@hrassistant.ru"
                className="text-gray-400 hover:text-white transition-colors"
              >
                <Mail className="h-5 w-5" />
              </a>
              <a
                href="https://t.me/hrassistantbot"
                className="text-gray-400 hover:text-white transition-colors"
                target="_blank"
                rel="noopener noreferrer"
              >
                <MessageCircle className="h-5 w-5" />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Быстрые ссылки</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/resume" className="text-gray-300 hover:text-white transition-colors">
                  Загрузить резюме
                </Link>
              </li>
              <li>
                <Link href="/jobs" className="text-gray-300 hover:text-white transition-colors">
                  Поиск вакансий
                </Link>
              </li>
              <li>
                <Link href="/profile" className="text-gray-300 hover:text-white transition-colors">
                  Мой профиль
                </Link>
              </li>
              <li>
                <Link href="/help" className="text-gray-300 hover:text-white transition-colors">
                  Помощь
                </Link>
              </li>
            </ul>
          </div>

          {/* Features */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Возможности</h3>
            <ul className="space-y-2 text-gray-300">
              <li>🔍 Автоматический поиск вакансий</li>
              <li>🤖 Анализ с помощью ИИ</li>
              <li>📱 Уведомления в Telegram</li>
              <li>📧 Автоматическая отправка резюме</li>
              <li>📊 Аналитика и статистика</li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-gray-400 text-sm">
            © 2024 HR Assistant. Все права защищены.
          </p>
          <div className="flex space-x-6 mt-4 md:mt-0">
            <Link href="/privacy" className="text-gray-400 hover:text-white text-sm transition-colors">
              Конфиденциальность
            </Link>
            <Link href="/terms" className="text-gray-400 hover:text-white text-sm transition-colors">
              Условия использования
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}