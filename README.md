### Музыкальный магазин
Музыкальный магазин - это проект на FastAPI и Streamlit, предназначенный для управления ансамблями, музыкантами, музыкальными произведениями и компакт-дисками.

## О проекте
### Проект включает следующие модули:
#### Ансамбли - создание и управление ансамблями.
#### Музыканты - добавление и управление музыкантами.
#### Музыкальные произведения - создание и управление музыкальными произведениями.
#### Компакт-диски - добавление и управление компакт-дисками, а также добавление исполнений.
Установка и настройка
## 1. Клонирование репозитория
git clone https://github.com/yourusername/musical_store.git
cd musical_store

## 2. Создание и активация виртуального окружения
python -m venv venv

source venv/Scripts/activate # Windows
source venv/bin/activate # macOS/Linux

## 3. Установка зависимостей
pip install -r requirements.txt

## 4. Применение миграций
python -m app.database.migrate

## 5. Запуск сервера разработки
Запуск FastAPI сервера
uvicorn app.main
--reload

Запуск Streamlit интерфейса
streamlit run app/frontend.py

## Автор
Автор проекта: [Maksim]
