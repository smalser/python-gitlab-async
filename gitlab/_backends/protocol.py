from __future__ import annotations

import abc
from typing import Any, Protocol, Union

import httpx
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder  # type: ignore


class BackendResponse(Protocol):
    @abc.abstractmethod
    def __init__(self, response: Union[requests.Response, httpx.Response]) -> None: ...

    @property
    def response(self) -> requests.Response: ...

    @property
    def status_code(self) -> int: ...

    @property
    def headers(self) -> Dict[str]: ...

    @property
    def content(self) -> bytes: ...

    @property
    def reason(self) -> str: ...

    def json(self) -> Any: ...


class Backend(Protocol):
    @abc.abstractmethod
    def http_request(
        self,
        method: str,
        url: str,
        json: dict[str, Any] | bytes | None,
        data: dict[str, Any] | MultipartEncoder | None,
        params: Any | None,
        timeout: float | None,
        verify: bool | str | None,
        stream: bool | None,
        **kwargs: Any,
    ) -> BackendResponse: ...


class AsyncBackend(Protocol):
    @abc.abstractmethod
    async def http_request(
        self,
        method: str,
        url: str,
        json: dict[str, Any] | bytes | None,
        data: dict[str, Any] | MultipartEncoder | None,
        params: Any | None,
        timeout: float | None,
        verify: bool | str | None,
        stream: bool | None,
        **kwargs: Any,
    ) -> BackendResponse: ...
