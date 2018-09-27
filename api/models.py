from django.db import models
from spotifydj.users.modelsi import User


# Create your models here.
class RefreshToken(model.Models):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    expired = models.BooleanField(default=False)
