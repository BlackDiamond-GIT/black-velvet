"""Custom admin widgets for Cloudinary image fields on Masseuse."""

from __future__ import annotations

from django import forms
from django.urls import reverse
from django.utils.html import format_html, mark_safe


_BTN_STYLE = (
    "background:#BE1E2D;color:#fff;border:none;border-radius:6px;"
    "padding:.45rem 1rem;cursor:pointer;font-size:.85rem;font-weight:500;"
    "white-space:nowrap;"
)


class CloudinaryFKWidget(forms.Select):
    """Dropdown for ForeignKey to CloudinaryImage (main photo) with thumbnail preview."""

    def render(self, name: str, value: object, attrs: dict | None = None, renderer: object = None) -> str:
        select_html = super().render(name, value, attrs, renderer=renderer)
        picker_url = reverse("media_library:image_picker") + "?single=1"

        thumb_html = ""
        if value:
            from apps.media_library.models import CloudinaryImage
            try:
                img = CloudinaryImage.objects.get(pk=value)
                thumb_html = format_html(
                    '<div id="cld-fk-thumb-{}" style="margin-top:.5rem">'
                    '<img src="{}" style="height:80px;width:64px;object-fit:cover;'
                    'border-radius:6px;border:2px solid #BE1E2D">'
                    '</div>',
                    name, img.thumbnail_url,
                )
            except CloudinaryImage.DoesNotExist:
                pass

        picker_btn = format_html(
            '<button type="button" class="cld-picker-open" '
            'data-target="{}" data-single="1" data-picker="{}" '
            'style="{}">'
            'Вибрати з бібліотеки'
            '</button>',
            name, picker_url, _BTN_STYLE,
        )

        return mark_safe(
            '<div style="display:flex;align-items:center;flex-wrap:wrap;gap:.5rem">'
            + select_html
            + picker_btn
            + '</div>'
            + thumb_html
            + _picker_js()
        )


class CloudinaryM2MWidget(forms.SelectMultiple):
    """Multi-select widget for M2M to CloudinaryImage (gallery) with thumbnail strip."""

    def render(self, name: str, value: object, attrs: dict | None = None, renderer: object = None) -> str:
        if attrs is None:
            attrs = {}
        attrs = dict(attrs, style="display:none")
        select_html = super().render(name, value, attrs, renderer=renderer)
        picker_url = reverse("media_library:image_picker")

        selected_ids = list(value) if value else []
        thumbs = ""
        if selected_ids:
            from apps.media_library.models import CloudinaryImage
            imgs = CloudinaryImage.objects.filter(pk__in=selected_ids)
            thumbs = "".join(
                format_html(
                    '<div class="cld-thumb" data-id="{}" '
                    'style="position:relative;display:inline-block;">'
                    '<img src="{}" style="height:72px;width:58px;object-fit:cover;'
                    'border-radius:6px;border:2px solid #9A1524">'
                    '<button type="button" class="cld-thumb-remove" '
                    'data-image-id="{}" data-field="{}" '
                    'style="position:absolute;top:-6px;right:-6px;width:18px;height:18px;'
                    'background:#ef4444;border:none;border-radius:50%;color:#fff;cursor:pointer;'
                    'font-size:.7rem;line-height:1;display:flex;align-items:center;'
                    'justify-content:center;">✕</button>'
                    '</div>',
                    img.pk, img.thumbnail_url, img.pk, name,
                )
                for img in imgs
            )

        # Always render strip div so JS picker callback can append to it
        strip_html = (
            f'<div id="cld-strip-{name}" '
            f'style="display:flex;flex-wrap:wrap;gap:.5rem;margin-bottom:.5rem">'
            + thumbs
            + '</div>'
        )

        picker_btn = format_html(
            '<button type="button" class="cld-picker-open" '
            'data-target="{}" data-single="0" data-picker="{}" '
            'style="{}">'
            'Вибрати з бібліотеки'
            '</button>',
            name, picker_url, _BTN_STYLE,
        )

        return mark_safe(
            strip_html
            + select_html
            + '<div style="margin-top:.5rem">' + picker_btn + '</div>'
            + _picker_js()
        )


def _picker_js() -> str:
    return """
<script>
(function () {
  if (window._cldPickerJsLoaded) return;
  window._cldPickerJsLoaded = true;

  /* Build a remove button safely via DOM (avoids all string-escaping issues). */
  function makeRemoveBtn(imageId, fieldName) {
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'cld-thumb-remove';
    btn.textContent = '\u2715';
    btn.style.cssText = 'position:absolute;top:-6px;right:-6px;width:18px;height:18px;' +
      'background:#ef4444;border:none;border-radius:50%;color:#fff;cursor:pointer;' +
      'font-size:.7rem;line-height:1;display:flex;align-items:center;justify-content:center;';
    btn.addEventListener('click', function () { cldM2MRemove(imageId, fieldName); });
    return btn;
  }

  window.cldPickerCallback = function (items, single) {
    var target = window._cldPickerTarget;
    if (!target) return;
    var select = document.querySelector('select[name="' + target + '"]');
    if (!select) return;

    if (single) {
      select.value = items[0].id;
      /* Update or create preview thumbnail below the select. */
      var container = select.closest('div') || select.parentElement;
      var thumb = container.querySelector('.cld-fk-thumb-set');
      if (!thumb) {
        thumb = document.createElement('div');
        thumb.className = 'cld-fk-thumb-set';
        thumb.style.marginTop = '.5rem';
        container.parentElement.appendChild(thumb);
      }
      var img = document.createElement('img');
      img.src = items[0].thumb;
      img.style.cssText = 'height:80px;width:64px;object-fit:cover;border-radius:6px;border:2px solid #BE1E2D';
      thumb.innerHTML = '';
      thumb.appendChild(img);
      return;
    }

    var strip = document.getElementById('cld-strip-' + target);

    items.forEach(function (item) {
      /* Mark option as selected (it already exists in hidden select). */
      var opt = select.querySelector('option[value="' + item.id + '"]');
      if (!opt) {
        opt = document.createElement('option');
        opt.value = item.id;
        opt.textContent = item.label;
        select.appendChild(opt);
      }
      opt.selected = true;

      /* Add thumbnail to strip. */
      if (strip && !strip.querySelector('[data-id="' + item.id + '"]')) {
        var div = document.createElement('div');
        div.className = 'cld-thumb';
        div.dataset.id = item.id;
        div.style.cssText = 'position:relative;display:inline-block;';

        var img = document.createElement('img');
        img.src = item.thumb;
        img.style.cssText = 'height:72px;width:58px;object-fit:cover;border-radius:6px;border:2px solid #9A1524';

        div.appendChild(img);
        div.appendChild(makeRemoveBtn(item.id, target));
        strip.appendChild(div);
      }
    });
  };

  window.cldM2MRemove = function (imageId, fieldName) {
    var select = document.querySelector('select[name="' + fieldName + '"]');
    if (select) {
      var opt = select.querySelector('option[value="' + imageId + '"]');
      if (opt) opt.selected = false;
    }
    var strip = document.getElementById('cld-strip-' + fieldName);
    if (strip) {
      var thumb = strip.querySelector('[data-id="' + imageId + '"]');
      if (thumb) thumb.remove();
    }
  };

  /* Delegated remove handler for server-rendered thumbnails. */
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.cld-thumb-remove');
    if (btn) {
      cldM2MRemove(btn.dataset.imageId, btn.dataset.field);
      return;
    }

    /* Open picker popup. */
    var open = e.target.closest('.cld-picker-open');
    if (!open) return;
    var target = open.dataset.target;
    var single = open.dataset.single === '1';
    var url = open.dataset.picker + (single ? '?single=1' : '');
    window._cldPickerTarget = target;
    window.open(url, 'cld_picker', 'width=900,height=600,resizable=yes,scrollbars=yes');
  });
})();
</script>
"""
