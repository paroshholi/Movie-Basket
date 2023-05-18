from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from enter.models import UserProfile
User = get_user_model()

class Command(BaseCommand):
    help = 'Set default language for existing users'

    def handle(self, *args, **options):
        # A dictionary to map user IDs to their default language
        default_languages = {
            1: 'en'
            # Add more users and their default languages here
        }

        for user_id, language in default_languages.items():
            try:
                user = User.objects.get(id=user_id)
                profile, created = UserProfile.objects.get_or_create(user=user)
                profile.favorite_language = language
                profile.save()
                self.stdout.write(self.style.SUCCESS(f"Set default language='{language}' for user '{user.username}'"))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"User with ID {user_id} does not exist"))
