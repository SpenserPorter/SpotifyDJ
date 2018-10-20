from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, BooleanField, IntegerField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    name = CharField(_("Name of User"), blank=True, max_length=255)
    karma = IntegerField(default=0)
    is_logged_into_spotify = BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
