"""Build first-party booking redirect URLs (click tracking before wa.me)."""

from __future__ import annotations

import urllib.parse

from django.urls import reverse


def build_booking_out_url(
    *,
    placement: str,
    masseuse_slug: str = "",
    service_slug: str = "",
    duration: str = "",
    page: str = "",
) -> str:
    """Return /booking/out/?placement=… for server-side click logging."""
    params: dict[str, str] = {"placement": placement}
    if masseuse_slug:
        params["masseuse"] = masseuse_slug
    if service_slug:
        params["service"] = service_slug
    if duration:
        params["duration"] = duration
    if page:
        params["page"] = page[:200]
    query = urllib.parse.urlencode(params)
    return f"{reverse('booking:booking_out')}?{query}"


def build_reservation_url(*, placement: str, page: str = "") -> str:
    """Return reservation URL with click-tracking query params."""
    params: dict[str, str] = {"placement": placement}
    if page:
        params["page"] = page[:200]
    query = urllib.parse.urlencode(params)
    return f"{reverse('reservation_page')}?{query}"
