#!/usr/bin/env python3
"""
Простой тест для асинхронного GitLab клиента
"""

import asyncio
import os
from gitlab import AsyncGitlab


async def test_basic_functionality():
    """Тест базовой функциональности."""
    print("=== Тест базовой функциональности ===")
    
    # Создаем клиент
    gl = AsyncGitlab(
        url="https://gitlab.com",
        private_token=os.getenv("GITLAB_TOKEN", "test-token")
    )
    
    try:
        # Тест GET запроса
        print("Тестируем GET запрос...")
        response = await gl.get("/version")
        print(f"Статус: {response['status_code']}")
        print(f"Ответ: {response['text'][:100]}...")
        
        # Тест с параметрами
        print("\nТестируем GET с параметрами...")
        response = await gl.get("/projects", params={"per_page": 1})
        print(f"Статус: {response['status_code']}")
        
    except Exception as e:
        print(f"Ошибка: {e}")


async def test_error_handling():
    """Тест обработки ошибок."""
    print("\n=== Тест обработки ошибок ===")
    
    # Клиент с неверным токеном
    gl = AsyncGitlab(
        url="https://gitlab.com",
        private_token="invalid-token"
    )
    
    try:
        response = await gl.get("/user")
        print(f"Неожиданный успех: {response}")
    except Exception as e:
        print(f"Ожидаемая ошибка: {e}")


async def test_different_auth_methods():
    """Тест различных методов аутентификации."""
    print("\n=== Тест методов аутентификации ===")
    
    # Private Token
    gl1 = AsyncGitlab(
        url="https://gitlab.com",
        private_token="test-token"
    )
    print("✓ Private Token клиент создан")
    
    # OAuth Token
    gl2 = AsyncGitlab(
        url="https://gitlab.com",
        oauth_token="test-oauth-token"
    )
    print("✓ OAuth Token клиент создан")
    
    # Job Token
    gl3 = AsyncGitlab(
        url="https://gitlab.com",
        job_token="test-job-token"
    )
    print("✓ Job Token клиент создан")


async def test_http_methods():
    """Тест различных HTTP методов."""
    print("\n=== Тест HTTP методов ===")
    
    gl = AsyncGitlab(
        url="https://gitlab.com",
        private_token=os.getenv("GITLAB_TOKEN", "test-token")
    )
    
    try:
        # GET
        response = await gl.get("/version")
        print(f"GET: {response['status_code']}")
        
        # POST (создание проекта)
        project_data = {"name": "test-project-async"}
        try:
            response = await gl.post("/projects", data=project_data)
            print(f"POST: {response['status_code']}")
        except Exception as e:
            print(f"POST ошибка (ожидаемо): {e}")
        
        # PUT (обновление проекта)
        update_data = {"description": "Updated description"}
        try:
            response = await gl.put("/projects/test-project-async", data=update_data)
            print(f"PUT: {response['status_code']}")
        except Exception as e:
            print(f"PUT ошибка (ожидаемо): {e}")
        
        # DELETE (удаление проекта)
        try:
            response = await gl.delete("/projects/test-project-async")
            print(f"DELETE: {response['status_code']}")
        except Exception as e:
            print(f"DELETE ошибка (ожидаемо): {e}")
        
        # PATCH (частичное обновление)
        patch_data = {"name": "updated-name"}
        try:
            response = await gl.patch("/projects/test-project-async", data=patch_data)
            print(f"PATCH: {response['status_code']}")
        except Exception as e:
            print(f"PATCH ошибка (ожидаемо): {e}")
            
    except Exception as e:
        print(f"Общая ошибка: {e}")


async def test_parallel_requests():
    """Тест параллельных запросов."""
    print("\n=== Тест параллельных запросов ===")
    
    gl = AsyncGitlab(
        url="https://gitlab.com",
        private_token=os.getenv("GITLAB_TOKEN", "test-token")
    )
    
    try:
        # Выполняем несколько запросов параллельно
        tasks = [
            gl.get("/version"),
            gl.get("/projects", params={"per_page": 1}),
            gl.get("/users", params={"per_page": 1})
        ]
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, response in enumerate(responses):
            if isinstance(response, Exception):
                print(f"Запрос {i+1}: Ошибка - {response}")
            else:
                print(f"Запрос {i+1}: Статус {response['status_code']}")
                
    except Exception as e:
        print(f"Ошибка в параллельных запросах: {e}")


async def main():
    """Основная функция."""
    print("Запуск тестов асинхронного GitLab клиента...")
    
    await test_basic_functionality()
    await test_error_handling()
    await test_different_auth_methods()
    await test_http_methods()
    await test_parallel_requests()
    
    print("\n=== Все тесты завершены ===")


if __name__ == "__main__":
    asyncio.run(main()) 