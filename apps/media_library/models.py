"""Media Library: Cloudinary image metadata stored in DB."""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from .cloudinary_urls import apply_cloudinary_transform, cloudinary_srcset

_CARD = "w_{w},c_limit,q_auto,f_auto"
_GALLERY = "w_{w},c_limit,q_auto,f_auto"
_DETAIL = "w_800,c_limit,q_auto,f_auto"


class CloudinaryImage(models.Model):
    """Metadata record for an image uploaded to Cloudinary."""

    public_id = models.CharField(
        _("Cloudinary public_id"),
        max_length=255,
        unique=True,
        db_index=True,
    )
    secure_url = models.URLField(_("Secure URL"), max_length=500)
    title = models.CharField(_("Title / label"), max_length=200, blank=True)
    width = models.PositiveIntegerField(_("Width (px)"), null=True, blank=True)
    height = models.PositiveIntegerField(_("Height (px)"), null=True, blank=True)
    format = models.CharField(_("Format"), max_length=10, blank=True)
    bytes = models.PositiveIntegerField(_("File size (bytes)"), null=True, blank=True)
    uploaded_at = models.DateTimeField(_("Uploaded at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
        ordering = ["-uploaded_at"]

    def __str__(self) -> str:
        return self.title or self.public_id

    def url_with_transform(self, transform: str) -> str:
        """Return secure_url with a Cloudinary transformation segment."""
        return apply_cloudinary_transform(self.secure_url, transform)

    @property
    def thumbnail_url(self) -> str:
        """Return a 200px-wide thumbnail URL via Cloudinary transformation."""
        return self.url_with_transform("w_200,c_fill,q_auto,f_auto")

    @property
    def display_url(self) -> str:
        """Return URL optimized for display (auto quality/format)."""
        return self.url_with_transform("q_auto,f_auto")

    @property
    def card_url(self) -> str:
        return self.url_with_transform("w_400,c_limit,q_auto,f_auto")

    @property
    def card_srcset(self) -> str:
        return cloudinary_srcset(self.secure_url, (400, 800), _CARD)

    @property
    def gallery_url(self) -> str:
        return self.url_with_transform("w_800,c_limit,q_auto,f_auto")

    @property
    def gallery_srcset(self) -> str:
        return cloudinary_srcset(self.secure_url, (800, 1200), _GALLERY)

    @property
    def detail_url(self) -> str:
        return self.url_with_transform(_DETAIL)
