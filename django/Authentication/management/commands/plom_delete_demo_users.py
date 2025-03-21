from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    """
    This is the command for "python manage.py plom_delete_demo_users.py
    It deletes all the users within demo group.
    """

    def handle(self, *args, **options):
        for demo_user in User.objects.filter(groups__name="demo"):
            demo_user.delete()

        print("All demo users have been deleted!")
