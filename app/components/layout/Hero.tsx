'use client';

import Link from 'next/link';
import { ArrowRight, Bot, Zap, Users } from 'lucide-react';

export function Hero() {
  return (
    <section className="relative bg-gradient-to-br from-primary-50 to-primary-100 pt-20 pb-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          {/* Badge */}
          <div className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-primary-100 text-primary-800 mb-6">
            <Bot className="h-3 w-3 mr-1" />
            Работает на искусственном интеллекте
          </div>

          {/* Heading */}
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6 text-balance">
            Найдите работу мечты с{' '}
            <span className="text-primary-600">HR Assistant</span>
          </h1>

          {/* Subheading */}
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto text-balance">
            Автоматизированный поиск и отклик на вакансии с помощью ИИ. 
            Загрузите резюме, получайте уведомления о подходящих позициях 
            и автоматически отправляйте заявки.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
            <Link
              href="/resume/upload"
              className="btn-primary flex items-center justify-center space-x-2 text-lg px-8 py-3"
            >
              <span>Начать поиск</span>
              <ArrowRight className="h-5 w-5" />
            </Link>
            <Link
              href="/demo"
              className="btn-secondary flex items-center justify-center space-x-2 text-lg px-8 py-3"
            >
              <span>Посмотреть демо</span>
            </Link>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-3xl mx-auto">
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-600 text-white rounded-lg mb-3">
                <Zap className="h-6 w-6" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900">95%</h3>
              <p className="text-gray-600">Точность анализа вакансий</p>
            </div>
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-600 text-white rounded-lg mb-3">
                <Users className="h-6 w-6" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900">1000+</h3>
              <p className="text-gray-600">Довольных пользователей</p>
            </div>
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-600 text-white rounded-lg mb-3">
                <Bot className="h-6 w-6" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900">24/7</h3>
              <p className="text-gray-600">Автоматический поиск</p>
            </div>
          </div>
        </div>
      </div>

      {/* Background decoration */}
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute -top-40 -right-32 w-80 h-80 bg-primary-200 rounded-full opacity-20 blur-3xl"></div>
        <div className="absolute -bottom-40 -left-32 w-80 h-80 bg-primary-300 rounded-full opacity-20 blur-3xl"></div>
      </div>
    </section>
  );
}