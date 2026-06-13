from .seo import build_hreflang, get_seo_context


class SEOMixin:
    seo_title = ''
    seo_description = ''
    seo_og_image = None
    seo_canonical_path = None

    def get_seo_title(self):
        return self.seo_title

    def get_seo_description(self):
        return self.seo_description

    def get_seo_og_image(self):
        return self.seo_og_image

    def get_seo_canonical_path(self):
        return self.seo_canonical_path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seo'] = get_seo_context(
            self.request,
            title=self.get_seo_title(),
            description=self.get_seo_description(),
            og_image=self.get_seo_og_image(),
            canonical_path=self.get_seo_canonical_path(),
        )
        hreflang = build_hreflang(self.request)
        context['hreflang_urls'] = hreflang
        context['hreflang_default'] = hreflang.get('x-default', '')
        return context
