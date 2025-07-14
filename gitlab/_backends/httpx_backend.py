from __future__ import annotations

import dataclasses
from typing import Any, BinaryIO, TYPE_CHECKING

import httpx
from httpx import Auth, Request, Response
from requests_toolbelt.multipart.encoder import MultipartEncoder  # type: ignore

from . import protocol


class TokenAuth:
    def __init__(self, token: str):
        self.token = token


class OAuthTokenAuth(TokenAuth, Auth):
    def auth_flow(self, request: Request) -> Any:
        request.headers["Authorization"] = f"Bearer {self.token}"
        request.headers.pop("PRIVATE-TOKEN", None)
        request.headers.pop("JOB-TOKEN", None)
        yield request


class PrivateTokenAuth(TokenAuth, Auth):
    def auth_flow(self, request: Request) -> Any:
        request.headers["PRIVATE-TOKEN"] = self.token
        request.headers.pop("JOB-TOKEN", None)
        request.headers.pop("Authorization", None)
        yield request


class JobTokenAuth(TokenAuth, Auth):
    def auth_flow(self, request: Request) -> Any:
        request.headers["JOB-TOKEN"] = self.token
        request.headers.pop("PRIVATE-TOKEN", None)
        request.headers.pop("Authorization", None)
        yield request


@dataclasses.dataclass
class SendData:
    content_type: str
    data: dict[str, Any] | MultipartEncoder | None = None
    json: dict[str, Any] | bytes | None = None

    def __post_init__(self) -> None:
        if self.json is not None and self.data is not None:
            raise ValueError(
                f"`json` and `data` are mutually exclusive. Only one can be set. "
                f"json={self.json!r}  data={self.data!r}"
            )


class HttpxResponse(protocol.AsyncBackendResponse):
    def __init__(self, response: Response) -> None:
        self._response: Response = response

    @property
    def response(self) -> Response:
        return self._response

    @property
    def status_code(self) -> int:
        return self._response.status_code

    @property
    def headers(self) -> httpx.Headers:
        return self._response.headers

    @property
    def content(self) -> bytes:
        return self._response.content

    @property
    def reason(self) -> str:
        return self._response.reason_phrase

    def json(self) -> Any:
        return self._response.json()


class HttpxBackend(protocol.AsyncBackend):
    def __init__(self, client: httpx.AsyncClient | None = None) -> None:
        self._client: httpx.AsyncClient = client or httpx.AsyncClient()

    @property
    def client(self) -> httpx.AsyncClient:
        return self._client

    @staticmethod
    def prepare_send_data(
        files: dict[str, Any] | None = None,
        post_data: dict[str, Any] | bytes | BinaryIO | None = None,
        raw: bool = False,
    ) -> SendData:
        if files:
            if post_data is None:
                post_data = {}
            else:
                # When creating a `MultipartEncoder` instance with data-types
                # which don't have an `encode` method it will cause an error:
                #       object has no attribute 'encode'
                # So convert common non-string types into strings.
                if TYPE_CHECKING:
                    assert isinstance(post_data, dict)
                for k, v in post_data.items():
                    if isinstance(v, bool):
                        v = int(v)
                    if isinstance(v, (complex, float, int)):
                        post_data[k] = str(v)
            post_data["file"] = files.get("file")
            post_data["avatar"] = files.get("avatar")

            data = MultipartEncoder(fields=post_data)
            return SendData(data=data, content_type=data.content_type)

        if raw and post_data:
            return SendData(data=post_data, content_type="application/octet-stream")

        if TYPE_CHECKING:
            assert not isinstance(post_data, BinaryIO)

        return SendData(json=post_data, content_type="application/json")

    async def http_request(
        self,
        method: str,
        url: str,
        json: dict[str, Any] | bytes | None = None,
        data: dict[str, Any] | MultipartEncoder | None = None,
        params: Any | None = None,
        timeout: float | None = None,
        verify: bool | str | None = True,
        stream: bool | None = False,
        **kwargs: Any,
    ) -> HttpxResponse:
        """Make HTTP request

        Args:
            method: The HTTP method to call ('get', 'post', 'put', 'delete', etc.)
            url: The full URL
            data: The data to send to the server in the body of the request
            json: Data to send in the body in json by default
            timeout: The timeout, in seconds, for the request
            verify: Whether SSL certificates should be validated. If
                the value is a string, it is the path to a CA file used for
                certificate validation.
            stream: Whether the data should be streamed

        Returns:
            A httpx Response object.
        """
        response: Response = await self._client.request(
            method=method,
            url=url,
            params=params,
            data=data,
            timeout=timeout,
            stream=stream,
            verify=verify,
            json=json,
            **kwargs,
        )
        return HttpxResponse(response=response) 