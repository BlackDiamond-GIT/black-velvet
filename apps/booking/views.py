"""Booking views: WhatsApp redirect with click logging."""

from __future__ import annotations

from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import get_language

from apps.services.models import Service
from apps.team.models import Masseuse

from .click_tracking import log_booking_click
from .utils import build_whatsapp_url


def _parse_duration(raw: str) -> int | None:
    value = (raw or '').strip()
    if not value.isdigit():
        return None
    return int(value)


def _booking_out_response(
    request: HttpRequest,
    *,
    placement: str,
    masseuse_slug: str = '',
    service_slug: str = '',
    duration_raw: str = '',
) -> HttpResponseRedirect:
    masseuse_name = ''
    if masseuse_slug:
        masseuse = get_object_or_404(Masseuse, slug=masseuse_slug, is_active=True)
        masseuse_name = masseuse.name

    service_name = ''
    if service_slug:
        service = Service.objects.filter(slug=service_slug, is_active=True).first()
        service_name = service.name if service else service_slug

    log_booking_click(
        request,
        channel='whatsapp',
        placement=placement,
        masseuse_slug=masseuse_slug,
        service_slug=service_slug,
        duration_min=_parse_duration(duration_raw),
    )

    url = build_whatsapp_url(
        masseuse_name=masseuse_name,
        service_name=service_name,
        duration=duration_raw,
        lang=get_language() or 'cs',
    )
    return HttpResponseRedirect(url)


def booking_out(request: HttpRequest) -> HttpResponseRedirect:
    return _booking_out_response(
        request,
        placement=request.GET.get('placement', 'unknown'),
        masseuse_slug=(request.GET.get('masseuse') or '').strip(),
        service_slug=(request.GET.get('service') or '').strip(),
        duration_raw=request.GET.get('duration', ''),
    )


def whatsapp_redirect(request: HttpRequest, slug: str | None = None) -> HttpResponseRedirect:
    return _booking_out_response(
        request,
        placement=request.GET.get('placement', 'unknown'),
        masseuse_slug=(slug or '').strip(),
        service_slug=(request.GET.get('service') or '').strip(),
        duration_raw=request.GET.get('duration', ''),
    )


def whatsapp_general(request: HttpRequest) -> HttpResponseRedirect:
    return _booking_out_response(
        request,
        placement=request.GET.get('placement', 'unknown'),
        masseuse_slug=(request.GET.get('masseuse') or '').strip(),
        service_slug=(request.GET.get('service') or '').strip(),
        duration_raw=request.GET.get('duration', ''),
    )
