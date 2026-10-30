from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

KNOWN_PASSWORDS = ('admin',)
SELLER_EMAIL = 'black.diamond.erotic.massage@gmail.com'
OWNER_EMAIL = 'info@black-velvet.cz'


class Command(BaseCommand):
    help = 'Lock any account that still uses a well-known password; never creates users'

    def handle(self, *args, **options):
        user_model = get_user_model()
        locked = 0
        for user in user_model.objects.all():
            changed = []
            if user.has_usable_password() and any(user.check_password(p) for p in KNOWN_PASSWORDS):
                user.set_unusable_password()
                changed.append('password')
            if user.email == SELLER_EMAIL:
                user.email = OWNER_EMAIL
                changed.append('email')
            if changed:
                user.save()
                locked += 1
                self.stdout.write(f'Secured "{user.get_username()}": {", ".join(changed)}')
        self.stdout.write(self.style.SUCCESS(f'lock_default_admin: {locked} account(s) secured.'))
