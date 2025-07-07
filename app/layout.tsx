import './globals.css';
import { Inter } from 'next/font/google';
import { Providers } from './providers';
import { Header } from './components/layout/Header';
import { Footer } from './components/layout/Footer';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'HR Assistant - Автоматизированный поиск работы',
  description: 'Интеллектуальный помощник для поиска и отклика на вакансии с использованием ИИ',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ru">
      <body className={inter.className}>
        <Providers>
          <div className="min-h-screen flex flex-col">
            <Header />
            <main className="flex-1">
              {children}
            </main>
            <Footer />
          </div>
        </Providers>
      </body>
    </html>
  );
}