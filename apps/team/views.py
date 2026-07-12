from django.views.generic.base import RedirectView


class TeamListView(RedirectView):
    permanent = False
    pattern_name = 'core:home'


class MasseuseDetailView(RedirectView):
    permanent = False
    pattern_name = 'core:home'
