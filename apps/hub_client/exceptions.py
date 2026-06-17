"""Hub API client exceptions."""

from __future__ import annotations


class HubAPIError(Exception):
    """Hub returned a non-2xx response or invalid JSON."""

    def __init__(self, message: str, status_code: int = 0) -> None:
        super().__init__(message)
        self.status_code = status_code


class HubUnavailableError(HubAPIError):
    """Hub could not be reached (network error, timeout)."""
