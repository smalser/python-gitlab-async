"""Тесты для асинхронного GitLab клиента."""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch

from gitlab import AsyncGitlab
from gitlab.exceptions import GitlabAuthenticationError, GitlabHttpError


class TestAsyncGitlab:
    """Тесты для AsyncGitlab клиента."""

    def test_init(self):
        """Тест инициализации клиента."""
        gl = AsyncGitlab(
            url="https://gitlab.com",
            private_token="test-token"
        )
        
        assert gl.url == "https://gitlab.com"
        assert gl.private_token == "test-token"
        assert gl.api_version == "4"

    def test_init_with_oauth_token(self):
        """Тест инициализации с OAuth токеном."""
        gl = AsyncGitlab(
            url="https://gitlab.com",
            oauth_token="oauth-token"
        )
        
        assert gl.oauth_token == "oauth-token"
        assert gl.private_token is None

    def test_init_with_job_token(self):
        """Тест инициализации с Job токеном."""
        gl = AsyncGitlab(
            url="https://gitlab.com",
            job_token="job-token"
        )
        
        assert gl.job_token == "job-token"
        assert gl.private_token is None

    @pytest.mark.asyncio
    async def test_get_request(self):
        """Тест GET запроса."""
        gl = AsyncGitlab(
            url="https://gitlab.com",
            private_token="test-token"
        )
        
        # Мокаем backend
        mock_response = {
            "status_code": 200,
            "headers": {"content-type": "application/json"},
            "content": b'{"id": 1, "name": "test"}',
            "text": '{"id": 1, "name": "test"}'
        }
        
        with patch.object(gl._backend, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response
            
            response = await gl.get("/user")
            
            assert response == mock_response
            mock_request.assert_called_once()
            
            # Проверяем, что заголовки аутентификации добавлены
            call_args = mock_request.call_args
            assert call_args[1]["headers"]["PRIVATE-TOKEN"] == "test-token"
            assert call_args[1]["headers"]["User-Agent"] == "python-gitlab-async/4"

    @pytest.mark.asyncio
    async def test_post_request(self):
        """Тест POST запроса."""
        gl = AsyncGitlab(
            url="https://gitlab.com",
            private_token="test-token"
        )
        
        mock_response = {
            "status_code": 201,
            "headers": {"content-type": "application/json"},
            "content": b'{"id": 2, "name": "new-project"}',
            "text": '{"id": 2, "name": "new-project"}'
        }
        
        with patch.object(gl._backend, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response
            
            data = {"name": "new-project"}
            response = await gl.post("/projects", data=data)
            
            assert response == mock_response
            mock_request.assert_called_once()
            
            call_args = mock_request.call_args
            assert call_args[1]["data"] == data

    @pytest.mark.asyncio
    async def test_put_request(self):
        """Тест PUT запроса."""
        gl = AsyncGitlab(
            url="https://gitlab.com",
            private_token="test-token"
        )
        
        mock_response = {
            "status_code": 200,
            "headers": {"content-type": "application/json"},
            "content": b'{"id": 1, "name": "updated"}',
            "text": '{"id": 1, "name": "updated"}'
        }
        
        with patch.object(gl._backend, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response
            
            data = {"name": "updated"}
            response = await gl.put("/projects/1", data=data)
            
            assert response == mock_response
            mock_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_request(self):
        """Тест DELETE запроса."""
        gl = AsyncGitlab(
            url="https://gitlab.com",
            private_token="test-token"
        )
        
        mock_response = {
            "status_code": 204,
            "headers": {},
            "content": b'',
            "text": ''
        }
        
        with patch.object(gl._backend, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response
            
            response = await gl.delete("/projects/1")
            
            assert response == mock_response
            mock_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_patch_request(self):
        """Тест PATCH запроса."""
        gl = AsyncGitlab(
            url="https://gitlab.com",
            private_token="test-token"
        )
        
        mock_response = {
            "status_code": 200,
            "headers": {"content-type": "application/json"},
            "content": b'{"id": 1, "name": "patched"}',
            "text": '{"id": 1, "name": "patched"}'
        }
        
        with patch.object(gl._backend, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response
            
            data = {"name": "patched"}
            response = await gl.patch("/projects/1", data=data)
            
            assert response == mock_response
            mock_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_authentication_error(self):
        """Тест ошибки аутентификации."""
        gl = AsyncGitlab(
            url="https://gitlab.com",
            private_token="invalid-token"
        )
        
        mock_response = {
            "status_code": 401,
            "headers": {},
            "content": b'Unauthorized',
            "text": 'Unauthorized'
        }
        
        with patch.object(gl._backend, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response
            
            with pytest.raises(GitlabAuthenticationError) as exc_info:
                await gl.get("/user")
            
            assert "Authentication failed" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_http_error(self):
        """Тест HTTP ошибки."""
        gl = AsyncGitlab(
            url="https://gitlab.com",
            private_token="test-token"
        )
        
        mock_response = {
            "status_code": 404,
            "headers": {},
            "content": b'Not Found',
            "text": 'Not Found'
        }
        
        with patch.object(gl._backend, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response
            
            with pytest.raises(GitlabHttpError) as exc_info:
                await gl.get("/nonexistent")
            
            assert "HTTP 404" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_oauth_token_auth(self):
        """Тест аутентификации с OAuth токеном."""
        gl = AsyncGitlab(
            url="https://gitlab.com",
            oauth_token="oauth-token"
        )
        
        mock_response = {
            "status_code": 200,
            "headers": {},
            "content": b'{"id": 1}',
            "text": '{"id": 1}'
        }
        
        with patch.object(gl._backend, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response
            
            await gl.get("/user")
            
            call_args = mock_request.call_args
            assert call_args[1]["headers"]["Authorization"] == "Bearer oauth-token"

    @pytest.mark.asyncio
    async def test_job_token_auth(self):
        """Тест аутентификации с Job токеном."""
        gl = AsyncGitlab(
            url="https://gitlab.com",
            job_token="job-token"
        )
        
        mock_response = {
            "status_code": 200,
            "headers": {},
            "content": b'{"id": 1}',
            "text": '{"id": 1}'
        }
        
        with patch.object(gl._backend, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response
            
            await gl.get("/user")
            
            call_args = mock_request.call_args
            assert call_args[1]["headers"]["JOB-TOKEN"] == "job-token"

    @pytest.mark.asyncio
    async def test_request_with_params(self):
        """Тест запроса с параметрами."""
        gl = AsyncGitlab(
            url="https://gitlab.com",
            private_token="test-token"
        )
        
        mock_response = {
            "status_code": 200,
            "headers": {},
            "content": b'[]',
            "text": '[]'
        }
        
        with patch.object(gl._backend, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response
            
            params = {"per_page": 10, "page": 1}
            await gl.get("/projects", params=params)
            
            call_args = mock_request.call_args
            assert call_args[1]["params"] == params

    @pytest.mark.asyncio
    async def test_request_with_timeout(self):
        """Тест запроса с таймаутом."""
        gl = AsyncGitlab(
            url="https://gitlab.com",
            private_token="test-token"
        )
        
        mock_response = {
            "status_code": 200,
            "headers": {},
            "content": b'[]',
            "text": '[]'
        }
        
        with patch.object(gl._backend, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response
            
            await gl.get("/projects", timeout=30.0)
            
            call_args = mock_request.call_args
            assert call_args[1]["timeout"] == 30.0

    @pytest.mark.asyncio
    async def test_backend_exception_handling(self):
        """Тест обработки исключений от backend."""
        gl = AsyncGitlab(
            url="https://gitlab.com",
            private_token="test-token"
        )
        
        with patch.object(gl._backend, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = Exception("Network error")
            
            with pytest.raises(GitlabHttpError) as exc_info:
                await gl.get("/user")
            
            assert "Request failed" in str(exc_info.value)


class TestAsyncGitlabIntegration:
    """Интеграционные тесты для AsyncGitlab."""

    @pytest.mark.asyncio
    async def test_multiple_requests(self):
        """Тест выполнения нескольких запросов."""
        gl = AsyncGitlab(
            url="https://gitlab.com",
            private_token="test-token"
        )
        
        mock_response = {
            "status_code": 200,
            "headers": {},
            "content": b'{"id": 1}',
            "text": '{"id": 1}'
        }
        
        with patch.object(gl._backend, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response
            
            # Выполняем несколько запросов
            responses = await asyncio.gather(
                gl.get("/user"),
                gl.get("/projects"),
                gl.get("/groups")
            )
            
            assert len(responses) == 3
            assert all(r == mock_response for r in responses)
            assert mock_request.call_count == 3 