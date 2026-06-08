# TeamFinder

## Описание

TeamFinder — веб-приложение для поиска команды и единомышленников для pet-проектов.

Пользователи могут регистрироваться, создавать проекты, просматривать профили других участников, присоединяться к чужим проектам и управлять собственными проектами.

Проект реализован по варианту №2: добавлены навыки пользователей и фильтрация участников по навыкам.

## Основной функционал

- регистрация и вход пользователей по email и паролю;
- кастомная модель пользователя;
- автоматическая генерация аватарки при создании пользователя;
- просмотр списка проектов;
- просмотр страницы отдельного проекта;
- создание и редактирование собственных проектов;
- закрытие собственных проектов;
- присоединение к чужим проектам;
- просмотр списка участников платформы;
- просмотр публичных профилей пользователей;
- редактирование собственного профиля;
- смена пароля;
- добавление и удаление навыков без перезагрузки страницы;
- автодополнение навыков;
- фильтрация пользователей по навыкам;
- админ-панель для управления пользователями, навыками и проектами.

## Технологии

- Python 3.10+
- Django 5.2
- PostgreSQL
- Docker Compose
- Pillow
- python-decouple
- HTML, CSS, JavaScript

## Переменные окружения

Создайте файл `.env` в корне проекта по примеру `.env_example`.

Пример содержимого `.env`:

```env
DJANGO_SECRET_KEY=change_for_safety
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=team_finder
POSTGRES_USER=team_finder
POSTGRES_PASSWORD=team_finder
POSTGRES_HOST=localhost
POSTGRES_PORT=5436
```

## Запуск проекта локально

Клонируйте репозиторий:

```bash
git clone https://github.com/TimurShigg/team-finder-ad.git
cd team-finder-ad
```

Создайте и активируйте виртуальное окружение:

```bash
python -m venv venv
```

Windows PowerShell:

```bash
venv\Scripts\Activate.ps1
```

Windows cmd:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

Запустите PostgreSQL через Docker Compose:

```bash
docker compose up -d
```

Примените миграции:

```bash
python manage.py migrate
```

Если в репозитории есть файл `db.json`, загрузите тестовые данные:

```bash
python manage.py loaddata db.json
```

Запустите сервер разработки:

```bash
python manage.py runserver
```

Проект будет доступен по адресу:

```text
http://127.0.0.1:8000/
```

## Создание администратора

```bash
python manage.py createsuperuser
```

После этого админ-панель будет доступна по адресу:

```text
http://127.0.0.1:8000/admin/
```

## Проверка качества кода

```bash
flake8 .
```

## Автор

Тимур Шиганов

GitHub: https://github.com/TimurShigg
