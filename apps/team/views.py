from django.urls import reverse
from django.views.generic.base import RedirectView


class TeamListView(RedirectView):
    permanent = False
    pattern_name = 'core:home'


class MasseuseDetailView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """Ignore the matched masseuse slug when reversing the homepage."""
        return reverse('core:home')
