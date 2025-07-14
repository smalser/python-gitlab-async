#!/usr/bin/env python3
"""
Простой тест для асинхронного GitLab клиента
"""

import asyncio
import os
import pytest

import gitlab


@pytest.mark.asyncio
async def test_async_client_creation():
    """Тест создания асинхронного клиента"""
    
    # Тест без токена (для публичных ресурсов)
    async with gitlab.AsyncGitlab(url="https://gitlab.com") as gl:
        assert gl.url == "https://gitlab.com"
        assert gl.api_url == "https://gitlab.com/api/v4"
        assert gl.api_version == "4"


@pytest.mark.asyncio
async def test_async_client_with_token():
    """Тест создания асинхронного клиента с токеном"""
    
    token = os.getenv("GITLAB_TOKEN")
    if not token:
        pytest.skip("GITLAB_TOKEN не установлен")
    
    async with gitlab.AsyncGitlab(
        url="https://gitlab.com",
        private_token=token
    ) as gl:
        assert gl.private_token == token
        assert gl.url == "https://gitlab.com"


@pytest.mark.asyncio
async def test_async_version():
    """Тест получения версии сервера"""
    
    async with gitlab.AsyncGitlab(url="https://gitlab.com") as gl:
        version, revision = await gl.version()
        assert isinstance(version, str)
        assert isinstance(revision, str)


@pytest.mark.asyncio
async def test_async_http_get():
    """Тест HTTP GET запроса"""
    
    async with gitlab.AsyncGitlab(url="https://gitlab.com") as gl:
        # Тестируем публичный endpoint
        result = await gl.http_get("/version")
        assert isinstance(result, dict)
        assert "version" in result


@pytest.mark.asyncio
async def test_async_search():
    """Тест поиска"""
    
    async with gitlab.AsyncGitlab(url="https://gitlab.com") as gl:
        # Поиск публичных проектов
        results = await gl.search("projects", "python")
        assert isinstance(results, list)


@pytest.mark.asyncio
async def test_async_context_manager():
    """Тест контекстного менеджера"""
    
    gl = gitlab.AsyncGitlab(url="https://gitlab.com")
    assert not gl.session.is_closed
    
    async with gl:
        assert not gl.session.is_closed
    
    # После выхода из контекста сессия должна быть закрыта
    assert gl.session.is_closed


@pytest.mark.asyncio
async def test_async_error_handling():
    """Тест обработки ошибок"""
    
    async with gitlab.AsyncGitlab(url="https://gitlab.com") as gl:
        try:
            await gl.http_get("/non-existent-endpoint")
            assert False, "Должна была возникнуть ошибка"
        except gitlab.exceptions.GitlabHttpError:
            # Ожидаемая ошибка
            pass


if __name__ == "__main__":
    # Запуск тестов
    pytest.main([__file__, "-v"]) 