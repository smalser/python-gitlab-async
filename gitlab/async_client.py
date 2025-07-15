"""Async GitLab client."""

from typing import Any, Dict, Optional, Union

import httpx

from ._backends.httpx_backend import HTTPXBackend
from .client import Gitlab
from .exceptions import GitlabAuthenticationError, GitlabHttpError


class AsyncGitlab(Gitlab):
    """Async GitLab client using HTTPX backend."""

    def __init__(
        self,
        url: str,
        private_token: Optional[str] = None,
        oauth_token: Optional[str] = None,
        job_token: Optional[str] = None,
        api_version: str = "4",
        session: Optional[Any] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the async GitLab client.
        
        Args:
            url: GitLab instance URL
            private_token: Private token for authentication
            oauth_token: OAuth token for authentication
            job_token: Job token for authentication
            api_version: API version to use
            session: Not used in async client (kept for compatibility)
            **kwargs: Additional arguments passed to HTTPX AsyncClient
        """
        
        # Вызываем родительский конструктор
        super().__init__(
            url=url,
            private_token=private_token,
            oauth_token=oauth_token,
            job_token=job_token,
            api_version=api_version,
            session=session,
        )

        self._backend = HTTPXBackend(**kwargs)

    async def http_request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """Make an async HTTP request.
        
        Args:
            method: HTTP method
            url: Request URL
            headers: Request headers
            data: Request data
            params: Query parameters
            timeout: Request timeout
            **kwargs: Additional arguments
            
        Returns:
            Response dictionary with status_code, headers, content, and text
            
        Raises:
            GitlabHttpError: If the request fails
            GitlabAuthenticationError: If authentication fails
        """
        # Формируем полный URL, если передан относительный путь
        if not url.startswith("http"):
            if url.startswith("/"):
                url = url[1:]
            url = f"{self.api_url}/{url}"
        # Добавляем заголовки аутентификации
        if headers is None:
            headers = {}
        
        if self.private_token:
            headers["PRIVATE-TOKEN"] = self.private_token
        elif self.oauth_token:
            headers["Authorization"] = f"Bearer {self.oauth_token}"
        elif self.job_token:
            headers["JOB-TOKEN"] = self.job_token
        
        # Добавляем User-Agent
        headers["User-Agent"] = f"python-gitlab-async/{self.api_version}"
        
        try:
            response = await self._backend.http_request(
                method=method,
                url=url,
                headers=headers,
                data=data,
                params=params,
                timeout=timeout,
                **kwargs,
            )
            
            # Проверяем статус код
            if response.status_code >= 400:
                if response.status_code == 401:
                    raise GitlabAuthenticationError(
                        f"Authentication failed: {response.text}"
                    )
                else:
                    raise GitlabHttpError(
                        f"HTTP {response.status_code}: {response.text}"
                    )
            
            return response
            
        except Exception as e:
            if isinstance(e, (GitlabHttpError, GitlabAuthenticationError)):
                raise
            raise GitlabHttpError(f"Request failed: {str(e)}")

    async def get(self, url: str, **kwargs: Any) -> httpx.Response:
        """Make a GET request."""
        return await self.http_request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs: Any) -> httpx.Response:
        """Make a POST request."""
        return await self.http_request("POST", url, **kwargs)

    async def put(self, url: str, **kwargs: Any) -> httpx.Response:
        """Make a PUT request."""
        return await self.http_request("PUT", url, **kwargs)

    async def delete(self, url: str, **kwargs: Any) -> httpx.Response:
        """Make a DELETE request."""
        return await self.http_request("DELETE", url, **kwargs)

    async def patch(self, url: str, **kwargs: Any) -> httpx.Response:
        """Make a PATCH request."""
        return await self.http_request("PATCH", url, **kwargs)
