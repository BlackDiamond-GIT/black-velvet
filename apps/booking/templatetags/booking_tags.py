"""Template tags for booking redirect URLs and WhatsApp links."""

from __future__ import annotations

from django import template

from apps.booking.booking_urls import build_booking_out_url, build_reservation_url

register = template.Library()


def _page_from_context(context: dict) -> str:
    request = context.get("request")
    if request is not None:
        return request.path or ""
    return ""


@register.simple_tag(takes_context=True)
def whatsapp_link(
    context: dict,
    masseuse: object | None = None,
    service: object | None = None,
    duration: str = "",
    placement: str = "unknown",
) -> str:
    masseuse_slug = getattr(masseuse, "slug", "") if masseuse else ""
    service_slug = getattr(service, "slug", "") if service else ""
    return build_booking_out_url(
        placement=placement,
        masseuse_slug=str(masseuse_slug),
        service_slug=str(service_slug),
        duration=duration,
        page=_page_from_context(context),
    )


@register.simple_tag(takes_context=True)
def booking_out_link(
    context: dict,
    placement: str,
    masseuse: object | None = None,
    service: object | None = None,
    duration: str = "",
) -> str:
    masseuse_slug = getattr(masseuse, "slug", "") if masseuse else ""
    service_slug = getattr(service, "slug", "") if service else ""
    return build_booking_out_url(
        placement=placement,
        masseuse_slug=str(masseuse_slug),
        service_slug=str(service_slug),
        duration=duration,
        page=_page_from_context(context),
    )


@register.simple_tag(takes_context=True)
def whatsapp_url(context: dict, placement: str = "unknown") -> str:
    return build_booking_out_url(placement=placement, page=_page_from_context(context))


@register.simple_tag(takes_context=True)
def reservation_link(context: dict, placement: str) -> str:
    return build_reservation_url(placement=placement, page=_page_from_context(context))
