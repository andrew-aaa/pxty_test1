# pxty_test1

```markdown
# ToDo List - Django Web Application

Простое веб-приложение для управления задачами с аутентификацией пользователей и фильтрацией задач.

## Основные функции

- ✅ Регистрация и аутентификация пользователей
- 📝 Создание, редактирование и удаление задач
- 🔍 Фильтрация задач по статусу и приоритету
- 📅 Установка сроков выполнения задач
- 🏷️ Категоризация задач по статусам и приоритетам

## Технологии

- Python 3.8+
- Django 4.0+
- Bootstrap 5
- SQLite (по умолчанию, можно заменить на PostgreSQL/MySQL)

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/andrew-aaa/pxty_test1
   cd ToDoList
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Примените миграции:
   ```bash
   python manage.py migrate
   ```

4. Создайте суперпользователя:
   ```bash
   python manage.py createsuperuser
   ```

5. Запустите сервер:
   ```bash
   python manage.py runserver
   ```

6. Откройте в браузере: [http://localhost:8000](http://localhost:8000)

## Структура проекта

```
ToDoList/
├── app/                   # Основное приложение
│   ├── migrations/        # Миграции базы данных
│   ├── templates/         # Шаблоны HTML
│   ├── __init__.py
│   ├── admin.py           # Админ-панель
│   ├── apps.py
│   ├── forms.py           # Формы
│   ├── models.py          # Модели данных
│   ├── urls.py            # URL-маршруты
│   └── views.py           # Контроллеры
├── ToDoList/             # Настройки проекта
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py        # Настройки
│   ├── urls.py            # Главные URL
│   └── wsgi.py
├── manage.py
├── README.md
```

## Использование

1. **Регистрация**: Перейдите по ссылке "Регистрация" и создайте учетную запись
2. **Вход**: Авторизуйтесь с вашими учетными данными
3. **Создание задачи**: Нажмите "Новая задача" и заполните форму
4. **Фильтрация**: Используйте фильтры вверху страницы для сортировки задач
5. **Редактирование**: Нажмите "Редактировать" на нужной задаче
6. **Удаление**: Нажмите "Удалить" на задаче и подтвердите действие

## Настройки

Основные настройки можно изменить в файле `ToDoList/settings.py`:

```python
# Настройки аутентификации
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'task_list'
LOGOUT_REDIRECT_URL = 'login'

# Настройки базы данных (можно заменить на PostgreSQL/MySQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## Развертывание в продакшн

Для развертывания на сервере рекомендуется:

1. Использовать PostgreSQL вместо SQLite
2. Настроить Nginx или Apache в качестве веб-сервера
3. Использовать Gunicorn или uWSGI как application-сервер
4. Настроить статические файлы через Whitenoise
5. Использовать environment variables для секретных данных

## Лицензия

Разработано Андрей © 2025