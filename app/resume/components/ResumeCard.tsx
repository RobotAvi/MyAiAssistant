'use client';

import { useState } from 'react';
import { FileText, MapPin, Calendar, Star, Edit, Trash2, Download } from 'lucide-react';

interface Resume {
  id: number;
  filename: string;
  position_title: string;
  skills: string[];
  experience_years: number;
  location: string;
  created_at: string;
  isActive: boolean;
}

interface ResumeCardProps {
  resume: Resume;
}

export function ResumeCard({ resume }: ResumeCardProps) {
  const [isActive, setIsActive] = useState(resume.isActive);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const handleToggleActive = () => {
    setIsActive(!isActive);
    // Здесь будет API вызов для обновления статуса
  };

  const handleDelete = () => {
    if (confirm('Вы уверены, что хотите удалить это резюме?')) {
      // Здесь будет API вызов для удаления
      console.log('Deleting resume:', resume.id);
    }
  };

  const handleDownload = () => {
    // Здесь будет логика скачивания файла
    console.log('Downloading resume:', resume.filename);
  };

  return (
    <div className={`card transition-all duration-200 ${isActive ? 'ring-2 ring-primary-200 border-primary-300' : ''}`}>
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-2">
            <FileText className="h-5 w-5 text-gray-400" />
            <span className="text-sm text-gray-500 truncate">
              {resume.filename}
            </span>
            {isActive && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                <Star className="h-3 w-3 mr-1" />
                Активное
              </span>
            )}
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-1">
            {resume.position_title}
          </h3>
        </div>
      </div>

      {/* Info */}
      <div className="space-y-3 mb-4">
        <div className="flex items-center text-sm text-gray-600">
          <MapPin className="h-4 w-4 mr-2" />
          <span>{resume.location}</span>
          <span className="ml-4">
            {resume.experience_years} {resume.experience_years === 1 ? 'год' : resume.experience_years < 5 ? 'года' : 'лет'} опыта
          </span>
        </div>

        <div className="flex items-center text-sm text-gray-600">
          <Calendar className="h-4 w-4 mr-2" />
          <span>Загружено {formatDate(resume.created_at)}</span>
        </div>
      </div>

      {/* Skills */}
      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-700 mb-2">Ключевые навыки:</h4>
        <div className="flex flex-wrap gap-1">
          {resume.skills.slice(0, 4).map((skill, index) => (
            <span
              key={index}
              className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-primary-50 text-primary-700"
            >
              {skill}
            </span>
          ))}
          {resume.skills.length > 4 && (
            <span className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-600">
              +{resume.skills.length - 4}
            </span>
          )}
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-200">
        <div className="flex space-x-2">
          <button
            onClick={handleDownload}
            className="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 transition-colors"
          >
            <Download className="h-4 w-4 mr-1" />
            Скачать
          </button>
          
          <button
            className="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 transition-colors"
          >
            <Edit className="h-4 w-4 mr-1" />
            Редактировать
          </button>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={handleToggleActive}
            className={`text-sm font-medium transition-colors ${
              isActive 
                ? 'text-orange-600 hover:text-orange-700' 
                : 'text-green-600 hover:text-green-700'
            }`}
          >
            {isActive ? 'Деактивировать' : 'Активировать'}
          </button>
          
          <button
            onClick={handleDelete}
            className="text-red-600 hover:text-red-700 transition-colors"
          >
            <Trash2 className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
}