# Асинхронная поддержка для python-gitlab

Этот патч добавляет асинхронную поддержку в библиотеку python-gitlab, позволяя использовать `httpx` вместо `requests` для асинхронных HTTP запросов.

## Установка

Убедитесь, что у вас установлен `httpx`:

```bash
pip install httpx
```

## Использование

### Базовое использование

```python
import asyncio
import gitlab

async def main():
    # Создаем асинхронный клиент
    async with gitlab.AsyncGitlab(
        url="https://gitlab.com",
        private_token="your-token"
    ) as gl:
        
        # Аутентификация
        await gl.auth()
        print(f"Аутентифицирован как: {gl.user.name}")
        
        # Получаем список проектов
        projects = await gl.projects.list(per_page=10)
        for project in projects:
            print(f"Проект: {project.name}")

# Запуск
asyncio.run(main())
```

### Работа с проектами

```python
async def work_with_project():
    async with gitlab.AsyncGitlab(
        url="https://gitlab.com",
        private_token="your-token"
    ) as gl:
        
        # Получаем конкретный проект
        project = await gl.projects.get("group/project")
        
        # Получаем issues
        issues = await project.issues.list(per_page=20)
        
        # Получаем merge requests
        mrs = await project.mergerequests.list(per_page=20)
        
        # Получаем коммиты
        commits = await project.commits.list(per_page=10)
```

### Поиск

```python
async def search_example():
    async with gitlab.AsyncGitlab(
        url="https://gitlab.com",
        private_token="your-token"
    ) as gl:
        
        # Поиск проектов
        projects = await gl.search("projects", "python")
        
        # Поиск issues
        issues = await gl.search("issues", "bug")
```

### Параллельные запросы

```python
async def parallel_requests():
    async with gitlab.AsyncGitlab(
        url="https://gitlab.com",
        private_token="your-token"
    ) as gl:
        
        # Выполняем несколько запросов параллельно
        tasks = [
            gl.projects.list(per_page=5),
            gl.users.list(per_page=5),
            gl.groups.list(per_page=5)
        ]
        
        results = await asyncio.gather(*tasks)
        projects, users, groups = results
        
        print(f"Проектов: {len(projects)}")
        print(f"Пользователей: {len(users)}")
        print(f"Групп: {len(groups)}")
```

## Основные отличия от синхронной версии

1. **Импорт**: Используйте `gitlab.AsyncGitlab` вместо `gitlab.Gitlab`
2. **Контекстный менеджер**: Используйте `async with` для автоматического закрытия соединения
3. **Асинхронные методы**: Все методы HTTP запросов теперь асинхронные
4. **Await**: Добавьте `await` перед всеми вызовами методов клиента

## Поддерживаемые методы

Все основные методы синхронной версии поддерживаются в асинхронной версии:

- `http_get()`
- `http_post()`
- `http_put()`
- `http_patch()`
- `http_delete()`
- `http_list()`
- `http_head()`
- `search()`
- `auth()`
- `version()`
- `markdown()`
- `get_license()`
- `set_license()`

## Обработка ошибок

```python
async def error_handling():
    async with gitlab.AsyncGitlab(
        url="https://gitlab.com",
        private_token="your-token"
    ) as gl:
        
        try:
            project = await gl.projects.get("non-existent/project")
        except gitlab.exceptions.GitlabGetError as e:
            print(f"Проект не найден: {e}")
        except gitlab.exceptions.GitlabAuthenticationError as e:
            print(f"Ошибка аутентификации: {e}")
```

## Конфигурация

Асинхронный клиент поддерживает те же параметры конфигурации, что и синхронный:

```python
async with gitlab.AsyncGitlab(
    url="https://gitlab.com",
    private_token="your-token",
    timeout=30.0,
    ssl_verify=True,
    retry_transient_errors=True,
    per_page=20,
    user_agent="MyApp/1.0"
) as gl:
    # Ваш код здесь
    pass
```

## Зависимости

- `httpx>=0.28.1` - для асинхронных HTTP запросов
- `requests-toolbelt` - для работы с multipart данными

## Примеры

Смотрите файл `examples/async_example.py` для полных примеров использования.

## Ограничения

1. GraphQL клиент уже поддерживает асинхронность через `gitlab.AsyncGraphQL`
2. Некоторые продвинутые функции могут требовать дополнительной адаптации
3. Тестирование асинхронного кода требует специальных подходов

## Миграция с синхронной версии

Для миграции с синхронной версии:

1. Замените `gitlab.Gitlab` на `gitlab.AsyncGitlab`
2. Оберните код в `async def` функцию
3. Добавьте `await` перед всеми вызовами методов клиента
4. Используйте `async with` для контекстного менеджера
5. Запускайте с `asyncio.run()`

```python
# Было
gl = gitlab.Gitlab(url="https://gitlab.com", private_token="token")
projects = gl.projects.list()

# Стало
async with gitlab.AsyncGitlab(url="https://gitlab.com", private_token="token") as gl:
    projects = await gl.projects.list()
``` 