"""HTTPX backend for async HTTP requests."""

from typing import Any, Dict, Optional, Union

import httpx

from .protocol import AsyncBackend, BackendResponse


class HTTPXResponse(BackendResponse):
    def __init__(self, response: httpx.Response) -> None:
        self._response: httpx.Response = response

    @property
    def response(self) -> httpx.Response:
        return self._response

    @property
    def status_code(self) -> int:
        return self._response.status_code

    @property
    def headers(self) -> Dict[str, str]:
        return dict(self._response.headers)

    @property
    def content(self) -> bytes:
        return self._response.content

    @property
    def text(self) -> str:
        return self._response.text

    @property
    def reason(self) -> str:
        return self._response.reason

    def json(self) -> Any:
        return self._response.json()


class HTTPXBackend(AsyncBackend):
    """HTTPX backend for async HTTP requests."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the HTTPX backend."""
        self._kwargs = kwargs

    async def http_request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs: Any,
    ) -> HTTPXResponse:
        """Make an async HTTP request using HTTPX."""
        # Создаем новый AsyncClient для каждого запроса
        async with httpx.AsyncClient(**self._kwargs) as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                data=data,
                params=params,
                timeout=timeout,
                **kwargs,
            )
            return HTTPXResponse(response=response)
