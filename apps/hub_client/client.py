"""Hub API client with Django cache and stale fallback.

Configuration (settings.py of each child site):
    HUB_API_URL = "https://tantra-prague.com"   # no trailing slash
    HUB_API_KEY = "<uuid from SiteConfig.api_key>"
    HUB_SITE_SLUG = "black-diamond"  # must match SiteConfig.slug

Usage:
    from apps.hub_client.client import HubClient

    client = HubClient()
    entries = client.fetch_schedule_json(from_date=date.today(), days=35)
    masseuses = client.get_masseuses()
"""

from __future__ import annotations

import hashlib
import logging
from datetime import date
from typing import Any

import requests
from django.conf import settings
from django.core.cache import cache

from .exceptions import HubAPIError, HubUnavailableError

logger = logging.getLogger(__name__)

_TIMEOUT = 10
_CACHE_TTL = 1800          # 30 minutes for content (masseuses, services…)
_SCHEDULE_CACHE_TTL = 300  # 5 minutes for schedule (more time-sensitive)
_STALE_SUFFIX = ":stale"


def _cache_key(method: str, *args: Any) -> str:
    site = getattr(settings, "HUB_SITE_SLUG", "unknown")
    raw = f"hub:{site}:{method}:" + ":".join(str(a) for a in args)
    return hashlib.md5(raw.encode()).hexdigest()


class HubClient:
    """Thin HTTP client for the tantra-prague.com hub API."""

    def __init__(self) -> None:
        self.base_url = getattr(settings, "HUB_API_URL", "").rstrip("/")
        self.api_key = getattr(settings, "HUB_API_KEY", "")
        self.site_slug = getattr(settings, "HUB_SITE_SLUG", "")

    # ── internal helpers ──────────────────────────────────────────────────────

    def _headers(self) -> dict[str, str]:
        return {"X-Site-Key": self.api_key, "Accept": "application/json"}

    def _url(self, path: str) -> str:
        return f"{self.base_url}/api/v1/{self.site_slug}/{path.lstrip('/')}"

    def _get(self, path: str, **params: Any) -> Any:
        """Perform GET and return parsed JSON data list/dict.

        Stores a stale copy in cache. On network failure returns stale data
        instead of raising, logging a warning.
        """
        url = self._url(path)
        key = _cache_key(path, str(params))
        stale_key = key + _STALE_SUFFIX

        try:
            resp = requests.get(
                url, params=params, headers=self._headers(), timeout=_TIMEOUT
            )
            if not resp.ok:
                raise HubAPIError(
                    f"Hub returned {resp.status_code} for {url}", status_code=resp.status_code
                )
            data = resp.json().get("data", resp.json())
            # Persist stale fallback (long TTL — used on outage)
            cache.set(stale_key, data, timeout=86400)
            return data

        except HubAPIError:
            raise
        except Exception as exc:
            stale = cache.get(stale_key)
            if stale is not None:
                logger.warning("Hub unreachable (%s), using stale cache for %s", exc, url)
                return stale
            raise HubUnavailableError(f"Hub unreachable and no stale cache: {exc}") from exc

    def _cached(self, cache_key: str, ttl: int, fetch_fn: Any) -> Any:
        """Return cached value or call fetch_fn() and cache the result."""
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
        data = fetch_fn()
        cache.set(cache_key, data, timeout=ttl)
        return data

    # ── schedule (sync-oriented) ──────────────────────────────────────────────

    def fetch_schedule_json(
        self, from_date: date | None = None, days: int = 35
    ) -> list[dict]:
        """Fetch schedule entries from hub. Not cached — used in sync commands."""
        if from_date is None:
            from_date = date.today()
        return self._get("schedule/", **{"from": from_date.isoformat(), "days": days})

    # ── content (live API + cache) ────────────────────────────────────────────

    def get_masseuses(self) -> list[dict]:
        key = _cache_key("masseuses")
        return self._cached(key, _CACHE_TTL, lambda: self._get("masseuses/"))

    def get_masseuse(self, slug: str) -> dict | None:
        key = _cache_key("masseuse", slug)
        try:
            return self._cached(key, _CACHE_TTL, lambda: self._get(f"masseuses/{slug}/"))
        except HubAPIError as exc:
            if exc.status_code == 404:
                return None
            raise

    def get_services(self, lang: str = "cs") -> list[dict]:
        key = _cache_key("services", lang)
        return self._cached(key, _CACHE_TTL, lambda: self._get("services/", lang=lang))

    def get_service(self, slug: str, lang: str = "cs") -> dict | None:
        key = _cache_key("service", slug, lang)
        try:
            return self._cached(
                key, _CACHE_TTL, lambda: self._get(f"services/{slug}/", lang=lang)
            )
        except HubAPIError as exc:
            if exc.status_code == 404:
                return None
            raise

    def get_blog_posts(self, page: int = 1, lang: str = "cs") -> dict:
        key = _cache_key("blog", page, lang)
        return self._cached(
            key, _CACHE_TTL, lambda: self._get("blog/", page=page, lang=lang)
        )

    def get_blog_post(self, slug: str, lang: str = "cs") -> dict | None:
        key = _cache_key("blog_post", slug, lang)
        try:
            return self._cached(
                key, _CACHE_TTL, lambda: self._get(f"blog/{slug}/", lang=lang)
            )
        except HubAPIError as exc:
            if exc.status_code == 404:
                return None
            raise

    def get_faq(self) -> list[dict]:
        key = _cache_key("faq")
        return self._cached(key, _CACHE_TTL, lambda: self._get("faq/"))

    def get_settings(self) -> dict:
        key = _cache_key("settings")
        return self._cached(key, _CACHE_TTL, lambda: self._get("settings/"))

    def invalidate_cache(self, method: str = "") -> None:
        """Invalidate cached data for a specific method or all methods."""
        patterns = [method] if method else [
            "masseuses", "services", "blog", "faq", "settings"
        ]
        for pattern in patterns:
            key = _cache_key(pattern)
            cache.delete(key)
