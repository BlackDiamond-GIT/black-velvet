"""Views for Media Library: upload signing, AJAX record creation, and image assignment."""

from __future__ import annotations

import hashlib
import json
import os

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import CloudinaryImage


@staff_member_required
def image_picker(request: HttpRequest) -> HttpResponse:
    """Popup: select CloudinaryImage(s) from the library. Used by custom admin widget."""
    q = request.GET.get("q", "").strip()
    qs = CloudinaryImage.objects.order_by("-uploaded_at")
    if q:
        qs = qs.filter(title__icontains=q) | qs.filter(public_id__icontains=q)

    return render(request, "admin/media_library/picker.html", {
        "images": qs[:200],
        "query": q,
        "is_popup": True,
    })


@staff_member_required
@require_POST
def sign_upload(request):
    """Sign the exact paramsToSign dict sent by Cloudinary Upload Widget (Option B).

    The Widget passes all final upload parameters (including source=uw) in the
    callback. We sign exactly those params — sorted alphabetically — and return
    only the signature. The API secret never leaves the server.
    """
    api_secret = os.getenv("CLOUDINARY_API_SECRET", "")
    if not api_secret:
        return JsonResponse({"error": "Cloudinary not configured"}, status=503)

    try:
        params = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        params = {}

    # Exclude keys that must not be part of the signature string
    exclude = {"api_key", "api_secret", "cloud_name", "resource_type", "file"}
    sorted_pairs = sorted(
        (k, v) for k, v in params.items() if k not in exclude
    )
    params_string = "&".join(f"{k}={v}" for k, v in sorted_pairs)
    string_to_sign = f"{params_string}{api_secret}"
    signature = hashlib.sha256(string_to_sign.encode()).hexdigest()

    return JsonResponse({"signature": signature})


@staff_member_required
@require_POST
def save_image(request):
    """Persist a Cloudinary upload result to the DB (called by Upload Widget callback)."""
    public_id = request.POST.get("public_id", "").strip()
    secure_url = request.POST.get("secure_url", "").strip()

    if not public_id or not secure_url:
        return JsonResponse({"error": "public_id and secure_url are required"}, status=400)

    obj, created = CloudinaryImage.objects.get_or_create(
        public_id=public_id,
        defaults={
            "secure_url": secure_url,
            "title": request.POST.get("original_filename", ""),
            "width": request.POST.get("width") or None,
            "height": request.POST.get("height") or None,
            "format": request.POST.get("format", ""),
            "bytes": request.POST.get("bytes") or None,
        },
    )
    if not created:
        # Update URL in case image was replaced in Cloudinary
        obj.secure_url = secure_url
        obj.save(update_fields=["secure_url"])

    return JsonResponse({"id": obj.pk, "public_id": obj.public_id, "created": created})


@staff_member_required
@require_POST
def assign_image(request, image_id: int):
    """Assign a CloudinaryImage to a masseuse as main photo or gallery item."""
    from apps.team.models import Masseuse

    try:
        image = CloudinaryImage.objects.get(pk=image_id)
    except CloudinaryImage.DoesNotExist:
        return JsonResponse({"error": "Image not found"}, status=404)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    masseuse_id = data.get("masseuse_id")
    assign_type = data.get("type")  # "main" | "gallery"

    try:
        masseuse = Masseuse.objects.get(pk=masseuse_id)
    except Masseuse.DoesNotExist:
        return JsonResponse({"error": "Masseuse not found"}, status=404)

    if assign_type == "main":
        masseuse.main_cloudinary_photo = image
        masseuse.save(update_fields=["main_cloudinary_photo"])
    elif assign_type == "gallery":
        masseuse.gallery_cloudinary.add(image)
    else:
        return JsonResponse({"error": "type must be 'main' or 'gallery'"}, status=400)

    return JsonResponse({"ok": True, "masseuse": masseuse.name, "type": assign_type})


@staff_member_required
@require_POST
def unassign_image(request, image_id: int):
    """Remove a CloudinaryImage assignment from a masseuse."""
    from apps.team.models import Masseuse

    try:
        image = CloudinaryImage.objects.get(pk=image_id)
    except CloudinaryImage.DoesNotExist:
        return JsonResponse({"error": "Image not found"}, status=404)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    masseuse_id = data.get("masseuse_id")
    assign_type = data.get("type")

    try:
        masseuse = Masseuse.objects.get(pk=masseuse_id)
    except Masseuse.DoesNotExist:
        return JsonResponse({"error": "Masseuse not found"}, status=404)

    if assign_type == "main":
        if masseuse.main_cloudinary_photo_id == image.pk:
            masseuse.main_cloudinary_photo = None
            masseuse.save(update_fields=["main_cloudinary_photo"])
    elif assign_type == "gallery":
        masseuse.gallery_cloudinary.remove(image)
    else:
        return JsonResponse({"error": "type must be 'main' or 'gallery'"}, status=400)

    return JsonResponse({"ok": True})
