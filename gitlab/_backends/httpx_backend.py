"""HTTPX backend for async HTTP requests."""

import asyncio
from typing import Any, Dict, Optional, Union

import httpx

from .protocol import AsyncHTTPBackend


class HTTPXBackend(AsyncHTTPBackend):
    """HTTPX backend for async HTTP requests."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the HTTPX backend."""
        self._kwargs = kwargs

    async def request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
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
            
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": response.content,
                "text": response.text,
            } 