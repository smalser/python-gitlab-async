#!/usr/bin/env python3
"""
Пример использования асинхронного GitLab клиента
"""

import asyncio
import os
from typing import Any

import gitlab


async def main() -> None:
    """Основная функция с примером использования AsyncGitlab"""
    
    # Создаем асинхронный клиент
    # Можно использовать токен из переменной окружения
    token = os.getenv("GITLAB_TOKEN")
    if not token:
        print("Установите переменную окружения GITLAB_TOKEN")
        return
    
    # Создаем асинхронный клиент
    async with gitlab.AsyncGitlab(
        url="https://gitlab.com",  # или ваш GitLab сервер
        private_token=token
    ) as gl:
        
        # Аутентификация
        await gl.auth()
        print(f"Аутентифицирован как: {gl.user.name}")
        
        # Получаем информацию о версии сервера
        version, revision = await gl.version()
        print(f"Версия GitLab: {version}, ревизия: {revision}")
        
        # Получаем список проектов
        projects = await gl.projects.list(per_page=5)
        print(f"Найдено проектов: {len(projects)}")
        
        for project in projects:
            print(f"  - {project.name} ({project.web_url})")
        
        # Поиск по проектам
        search_results = await gl.search("projects", "python")
        print(f"Результаты поиска 'python': {len(search_results)}")
        
        # Получаем информацию о лицензии (если доступно)
        try:
            license_info = await gl.get_license()
            print(f"Лицензия: {license_info.get('plan', 'Unknown')}")
        except gitlab.exceptions.GitlabGetError:
            print("Информация о лицензии недоступна")


async def example_with_project() -> None:
    """Пример работы с конкретным проектом"""
    
    token = os.getenv("GITLAB_TOKEN")
    if not token:
        print("Установите переменную окружения GITLAB_TOKEN")
        return
    
    async with gitlab.AsyncGitlab(
        url="https://gitlab.com",
        private_token=token
    ) as gl:
        
        # Получаем конкретный проект
        project_id = "gitlab-org/gitlab"  # Пример проекта
        try:
            project = await gl.projects.get(project_id)
            print(f"Проект: {project.name}")
            print(f"Описание: {project.description}")
            print(f"Звезды: {project.star_count}")
            
            # Получаем последние коммиты
            commits = await project.commits.list(per_page=3)
            print(f"Последние коммиты:")
            for commit in commits:
                print(f"  - {commit.short_id}: {commit.title}")
                
        except gitlab.exceptions.GitlabGetError as e:
            print(f"Ошибка при получении проекта: {e}")


async def example_with_issues() -> None:
    """Пример работы с issues"""
    
    token = os.getenv("GITLAB_TOKEN")
    if not token:
        print("Установите переменную окружения GITLAB_TOKEN")
        return
    
    async with gitlab.AsyncGitlab(
        url="https://gitlab.com",
        private_token=token
    ) as gl:
        
        # Получаем issues
        issues = await gl.issues.list(per_page=5)
        print(f"Найдено issues: {len(issues)}")
        
        for issue in issues:
            print(f"  - #{issue.iid}: {issue.title}")
            print(f"    Статус: {issue.state}")
            print(f"    Автор: {issue.author['name']}")


if __name__ == "__main__":
    print("=== Пример использования AsyncGitlab ===")
    
    # Запускаем все примеры
    asyncio.run(main())
    print("\n" + "="*50 + "\n")
    asyncio.run(example_with_project())
    print("\n" + "="*50 + "\n")
    asyncio.run(example_with_issues()) 