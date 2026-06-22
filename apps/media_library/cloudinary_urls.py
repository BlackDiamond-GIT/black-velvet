"""Cloudinary URL transformation helpers."""

from __future__ import annotations


def normalize_cloudinary_url(url: str) -> str:
    """Collapse duplicated folder segments in Cloudinary delivery paths."""
    if not url:
        return ''
    for folder in ('services', 'team', 'blog', 'interior'):
        doubled = f'/media/{folder}/{folder}/'
        single = f'/media/{folder}/'
        url = url.replace(doubled, single)
    return url


def apply_cloudinary_transform(url: str, transform: str) -> str:
    """Insert *transform* after /upload/; return *url* unchanged if not Cloudinary."""
    url = normalize_cloudinary_url(url)
    if not url or "res.cloudinary.com" not in url or "/upload/" not in url:
        return url
    base, _, rest = url.partition("/upload/")
    if not rest:
        return url
    return f"{base}/upload/{transform}/{rest}"


def cloudinary_srcset(url: str, widths: tuple[int, ...], transform_tpl: str) -> str:
    """Build a srcset string for Cloudinary image *url* at given *widths*."""
    if not url or "res.cloudinary.com" not in url:
        return ""
    parts = [
        f"{apply_cloudinary_transform(url, transform_tpl.format(w=w))} {w}w"
        for w in widths
    ]
    return ", ".join(parts)
