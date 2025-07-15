"""
Defines http backends for processing http requests
"""

from .requests_backend import (
    JobTokenAuth,
    OAuthTokenAuth,
    PrivateTokenAuth,
    RequestsBackend,
    RequestsResponse,
)

try:
    from .httpx_backend import HTTPXBackend
    _ASYNC_AVAILABLE = True
except ImportError:
    _ASYNC_AVAILABLE = False

DefaultBackend = RequestsBackend
DefaultResponse = RequestsResponse

__all__ = [
    "DefaultBackend",
    "DefaultResponse",
    "JobTokenAuth",
    "OAuthTokenAuth",
    "PrivateTokenAuth",
]

if _ASYNC_AVAILABLE:
    __all__.append("HTTPXBackend")
