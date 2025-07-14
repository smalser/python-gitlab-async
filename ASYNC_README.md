# Асинхронный GitLab клиент

Этот модуль предоставляет асинхронный клиент для работы с GitLab API, используя HTTPX для HTTP запросов.

## Особенности

- **Полностью асинхронный**: Все HTTP запросы выполняются асинхронно
- **Простота использования**: Каждый запрос создает свой собственный `AsyncClient` и автоматически закрывает его
- **Совместимость**: Наследует от базового класса `Gitlab` и поддерживает все стандартные методы
- **Обработка ошибок**: Встроенная обработка ошибок аутентификации и HTTP ошибок

## Установка

Убедитесь, что у вас установлен `httpx`:

```bash
pip install httpx
```

## Использование

### Базовое использование

```python
import asyncio
from gitlab import AsyncGitlab

async def main():
    # Создаем асинхронный клиент
    gl = AsyncGitlab(
        url="https://gitlab.com",
        private_token="your-token-here"
    )
    
    # Выполняем запросы
    response = await gl.get("/user")
    print(f"Пользователь: {response['text']}")
    
    # Получаем список проектов
    projects = await gl.get("/projects", params={"per_page": 5})
    print(f"Проекты: {projects['text']}")

# Запускаем
asyncio.run(main())
```

### Доступные методы

Клиент поддерживает все основные HTTP методы:

```python
# GET запрос
response = await gl.get("/projects")

# POST запрос
response = await gl.post("/projects", data={"name": "new-project"})

# PUT запрос
response = await gl.put("/projects/123", data={"description": "Updated"})

# DELETE запрос
response = await gl.delete("/projects/123")

# PATCH запрос
response = await gl.patch("/projects/123", data={"name": "new-name"})
```

### Параметры запросов

```python
# С параметрами запроса
response = await gl.get("/projects", params={
    "per_page": 10,
    "page": 1,
    "order_by": "created_at"
})

# С заголовками
response = await gl.get("/projects", headers={
    "Custom-Header": "value"
})

# С таймаутом
response = await gl.get("/projects", timeout=30.0)
```

### Обработка ошибок

```python
try:
    response = await gl.get("/user")
    print(f"Успех: {response['text']}")
except GitlabAuthenticationError as e:
    print(f"Ошибка аутентификации: {e}")
except GitlabHttpError as e:
    print(f"HTTP ошибка: {e}")
except Exception as e:
    print(f"Общая ошибка: {e}")
```

### Аутентификация

Поддерживаются различные типы аутентификации:

```python
# Private Token
gl = AsyncGitlab(
    url="https://gitlab.com",
    private_token="your-private-token"
)

# OAuth Token
gl = AsyncGitlab(
    url="https://gitlab.com",
    oauth_token="your-oauth-token"
)

# Job Token (для CI/CD)
gl = AsyncGitlab(
    url="https://gitlab.com",
    job_token="your-job-token"
)
```

### Параллельные запросы

```python
async def fetch_data():
    gl = AsyncGitlab(
        url="https://gitlab.com",
        private_token="your-token"
    )
    
    # Выполняем несколько запросов параллельно
    tasks = [
        gl.get("/projects"),
        gl.get("/users"),
        gl.get("/groups")
    ]
    
    results = await asyncio.gather(*tasks)
    return results

# Запускаем
projects, users, groups = await fetch_data()
```

## Архитектура

### HTTPX Backend

Клиент использует кастомный HTTPX backend (`HTTPXBackend`), который:

1. Создает новый `AsyncClient` для каждого запроса
2. Автоматически закрывает соединение после выполнения запроса
3. Возвращает стандартизированный ответ в виде словаря

### Структура ответа

Каждый HTTP запрос возвращает словарь с полями:

```python
{
    "status_code": 200,
    "headers": {"content-type": "application/json", ...},
    "content": b'{"id": 1, "name": "project"}',
    "text": '{"id": 1, "name": "project"}'
}
```

### Обработка ошибок

- **401 Unauthorized**: Вызывает `GitlabAuthenticationError`
- **4xx/5xx ошибки**: Вызывают `GitlabHttpError`
- **Сетевые ошибки**: Оборачиваются в `GitlabHttpError`

## Преимущества

1. **Простота**: Не нужно управлять жизненным циклом соединения
2. **Надежность**: Каждый запрос изолирован
3. **Производительность**: HTTPX обеспечивает высокую производительность
4. **Совместимость**: Работает с существующим кодом python-gitlab

## Ограничения

- Только API версии 4
- Базовые HTTP методы (GET, POST, PUT, DELETE, PATCH)
- Нет встроенной поддержки пагинации
- Нет поддержки GraphQL

## Примеры

Смотрите файл `examples/async_example.py` для полных примеров использования. 