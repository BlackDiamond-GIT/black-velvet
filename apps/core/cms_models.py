from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class LegacyRedirect(models.Model):
    """Maps old WordPress URL slugs/paths to new Django URLs."""

    old_path = models.CharField(
        _("Old path"),
        max_length=500,
        unique=True,
        db_index=True,
        help_text=_("e.g. /cs/nuru-masaz/ or /klasicka-eroticka-masaz/"),
    )
    new_path = models.CharField(
        _("New path"),
        max_length=500,
        blank=True,
        help_text=_("Leave blank to redirect to /. Use full path e.g. /cs/services/nuru/"),
    )
    is_active = models.BooleanField(_("Active"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Legacy Redirect")
        verbose_name_plural = _("Legacy Redirects")
        ordering = ["old_path"]

    def __str__(self) -> str:
        return f"{self.old_path} → {self.new_path or '/'}"


class ContentPage(models.Model):
    """Editable HTML for static pages (privacy, first visit, price list intro)."""

    class PageKey(models.TextChoices):
        PRIVACY = "privacy", _("Privacy Policy")
        FIRST_VISIT = "first_visit", _("First Visit")
        PRICES = "prices", _("Price list")
        JOBS = "jobs", _("Jobs")

    page_key = models.CharField(
        _("Page"),
        max_length=32,
        choices=PageKey.choices,
        unique=True,
    )
    body_cs = models.TextField(_("Body (Czech, HTML)"), blank=True)
    body_en = models.TextField(_("Body (English, HTML)"), blank=True)
    body_ru = models.TextField(_("Body (Russian, HTML)"), blank=True)
    hero_sub_cs = models.CharField(
        _("Hero subtitle (Czech)"),
        max_length=300,
        blank=True,
        help_text=_("Optional. Shown under the page title when filled."),
    )
    hero_sub_en = models.CharField(_("Hero subtitle (English)"), max_length=300, blank=True)
    hero_sub_ru = models.CharField(_("Hero subtitle (Russian)"), max_length=300, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Page Content")
        verbose_name_plural = _("Page Content")
        ordering = ["page_key"]

    def __str__(self) -> str:
        return self.get_page_key_display()  # type: ignore[attr-defined]

    def _lang_code(self, language_code: str) -> str:
        return (language_code or "cs").split("-")[0].lower()

    def get_body(self, language_code: str) -> str:
        code = self._lang_code(language_code)
        val = (getattr(self, f"body_{code}", "") or "").strip()
        if val:
            return val
        return (self.body_cs or "").strip()

    def get_hero_subtitle(self, language_code: str) -> str:
        code = self._lang_code(language_code)
        val = (getattr(self, f"hero_sub_{code}", "") or "").strip()
        if val:
            return val
        return (self.hero_sub_cs or "").strip()


class InteriorImage(models.Model):
    """Gallery image for the Interior page (Cloudinary, upload, or static file)."""

    cloudinary_image = models.ForeignKey(
        "media_library.CloudinaryImage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Cloudinary image"),
        related_name="interior_usages",
    )
    image = models.ImageField(_("Uploaded image"), upload_to="interior/", blank=True)
    static_path = models.CharField(
        _("Static file path"),
        max_length=255,
        blank=True,
        help_text=_("Relative to static/, e.g. src/img/interior/photo.jpg"),
    )
    alt_cs = models.CharField(_("Alt text (Czech)"), max_length=300, blank=True)
    alt_en = models.CharField(_("Alt text (English)"), max_length=300, blank=True)
    alt_ru = models.CharField(_("Alt text (Russian)"), max_length=300, blank=True)
    sort_order = models.PositiveIntegerField(_("Sort order"), default=0, db_index=True)
    is_active = models.BooleanField(_("Active"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Interior photo")
        verbose_name_plural = _("Interior photos")
        ordering = ["sort_order", "pk"]

    def __str__(self) -> str:
        label = self.alt_cs or self.static_path or str(self.pk)
        return label[:80]

    def clean(self) -> None:
        super().clean()
        if not self.cloudinary_image_id and not self.image and not self.static_path:
            raise ValidationError(
                _("Add a Cloudinary image, upload a file, or set a static path.")
            )
        if self._local_media_url_unavailable():
            raise ValidationError(
                {
                    "image": _(
                        "This file is stored only on the server disk and is not published. "
                        "Clear the upload and choose an image from the Cloudinary library."
                    ),
                }
            )

    def _local_media_url_unavailable(self) -> bool:
        from django.conf import settings

        if not settings.CLOUDINARY_URL or self.cloudinary_image_id or not self.image:
            return False
        return self.image.url.startswith("/media/")

    def get_image_url(self) -> str:
        if self.cloudinary_image_id:
            return self.cloudinary_image.gallery_url
        if self.image:
            url = self.image.url
            if url.startswith("/media/"):
                from django.conf import settings

                if settings.CLOUDINARY_URL:
                    return ""
            return url
        if self.static_path:
            return staticfiles_storage.url(self.static_path)
        return ""

    def get_alt(self, language_code: str) -> str:
        code = (language_code or "cs").split("-")[0].lower()
        val = (getattr(self, f"alt_{code}", "") or "").strip()
        if val:
            return val
        return (self.alt_cs or "").strip()


class GuestReview(models.Model):
    """Guest testimonial shown on the home page."""

    text_cs = models.TextField(_("Review (Czech)"))
    text_en = models.TextField(_("Review (English)"), blank=True)
    text_ru = models.TextField(_("Review (Russian)"), blank=True)
    author_label = models.CharField(
        _("Author"),
        max_length=40,
        help_text=_("e.g. M. K."),
    )
    city = models.CharField(_("City"), max_length=80, blank=True)
    google_review_id = models.CharField(
        _("Google review ID"),
        max_length=120,
        blank=True,
        null=True,
        unique=True,
        db_index=True,
        help_text=_("Stable ID from Google Places API (for sync)."),
    )
    rating = models.PositiveSmallIntegerField(
        _("Rating"),
        null=True,
        blank=True,
        help_text=_("Star rating (1–5) from Google."),
    )
    order = models.IntegerField(_("Order"), default=0)
    is_active = models.BooleanField(_("Active"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Guest review")
        verbose_name_plural = _("Guest reviews")
        ordering = ["order", "pk"]

    def __str__(self) -> str:
        return f"{self.author_label} — {self.text_cs[:60]}"

    def get_text(self, lang: str = "cs") -> str:
        code = (lang or "cs").split("-")[0].lower()
        val = (getattr(self, f"text_{code}", "") or "").strip()
        if val:
            return val
        return (self.text_cs or "").strip()


class EtiquetteRule(models.Model):
    """A single house-rule entry for the salon etiquette page."""

    class Category(models.TextChoices):
        BEHAVIOR = "behavior", _("Behavior")
        HYGIENE = "hygiene", _("Hygiene")
        PRIVACY = "privacy", _("Privacy")
        BOOKING = "booking", _("Booking & Cancellation")

    category = models.CharField(_("Category"), max_length=20, choices=Category.choices)
    rule_cs = models.TextField(_("Rule (Czech)"))
    rule_en = models.TextField(_("Rule (English)"), blank=True)
    rule_ru = models.TextField(_("Rule (Russian)"), blank=True)
    order = models.PositiveSmallIntegerField(_("Order"), default=0)
    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Etiquette rule")
        verbose_name_plural = _("Etiquette rules")
        ordering = ["category", "order"]

    def __str__(self) -> str:
        return f"[{self.get_category_display()}] {self.rule_cs[:60]}"  # type: ignore[attr-defined]

    def get_rule(self, lang: str = "cs") -> str:
        code = (lang or "cs").split("-")[0].lower()
        val = (getattr(self, f"rule_{code}", "") or "").strip()
        return val if val else (self.rule_cs or "").strip()
