# Health Survey Bot

## Описание
Health Survey Bot – это телеграм-бот для проведения опросов. Он позволяет администраторам собирать ответы на опрос от пользователей.

## Установка
1. Клонируйте репозиторий:
    ```bash
    git clone <URL репозитория>
    cd Health_project
    ```

2. Создайте виртуальное окружение и активируйте его:
    ```bash
    python -m venv venv
    source venv/bin/activate  # На Windows используйте `venv\Scripts\activate`
    ```

3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

4. Создайте файл `.env` на основе `.env.example` и укажите в нем необходимые переменные окружения.

## Использование
Для запуска бота выполните следующую команду:
```bash
python __main__.py
