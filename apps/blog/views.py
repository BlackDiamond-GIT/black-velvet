from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView

from apps.core.breadcrumbs import crumb, home_crumb
from apps.core.mixins import SEOMixin
from apps.pages.models import FAQ

from .models import Post


class PostListView(SEOMixin, ListView):
    model = Post
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 6
    seo_title = _('Blog o masáži a relaxaci Praha | Black Velvet')
    seo_description = _(
        'Tipy, rady a články o masáži, relaxaci a wellness v Praze. '
        'Praktické informace od odborníků Black Velvet Spa.'
    )

    def get_queryset(self):
        return Post.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [home_crumb(), crumb(_('Blog'))]
        context['schema_breadcrumb'] = True
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.htmx:
            return render(self.request, 'blog/partials/post_list.html', context)
        return super().render_to_response(context, **response_kwargs)


class PostDetailView(SEOMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Post.objects.filter(is_published=True)

    def get_seo_title(self):
        obj = self.object
        return obj.meta_title or f'{obj.title} | Black Velvet Blog'

    def get_seo_description(self):
        obj = self.object
        return obj.meta_description or obj.excerpt

    def get_seo_og_image(self):
        if self.object.image:
            return self.request.build_absolute_uri(self.object.image.url)
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = FAQ.objects.filter(is_active=True, page=FAQ.PAGE_GENERAL)[:3]
        context['related_posts'] = (
            Post.objects.filter(is_published=True).exclude(pk=self.object.pk)[:3]
        )
        context['breadcrumbs'] = [
            home_crumb(),
            crumb(_('Blog'), 'blog:list'),
            crumb(self.object.title),
        ]
        context['schema_article'] = True
        context['schema_breadcrumb'] = True
        return context
