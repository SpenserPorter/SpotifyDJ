from django.db import models
from spotifydj.users.models import User
import datetime as dt
from . import oauth2

class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=64)
    scope = models.CharField(max_length=1024)
    expires_at = models.BigIntegerField()
    refresh_token = models.CharField(max_length=255)

    def __repr__(self):
        return ''.join(self.user.name, ' token')

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(ClientToken, self).save(*args, **kwargs)

    @classmethod
    def create(cls, user, access_token, token_type, scope, expires_at, refresh_token):
        out = cls(user=user, access_token=access_token, token_type=token_type,
            scope=scope, expires_at=expires_at, refresh_token=refresh_token
            )
        return out

    @classmethod
    def persist(cls, token, user):
        access_token = token['access_token']
        token_type = token['token_type']
        expires_at = token['expires_at']
        scope = token['scope']
        refresh_token = token['refresh_token']
        return cls.create(user, access_token, token_type, scope, expires_at, refresh_token)

    def get_refresh_token(self):
        return self.refresh_token

    def is_expired(self):
        if self.expires_at < dt.datetime.utcnow().timestamp():
            return False
        return True

class UserGrant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=255)
    scope = models.CharField(max_length=1025)
    timestamp_created = models.DateTimeField(default=dt.datetime.utcnow)

    @classmethod
    def create(cls, user, state, scope):
        return cls(user=user, state=state, scope=scope)

class ClientToken(models.Model):
    access_token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=255)
    scope = models.CharField(max_length=1024)
    expires_at = models.BigIntegerField()

    @classmethod
    def create(cls, access_token, token_type, scope, expires_at):
        return cls(access_token=access_token, token_type=token_type, scope=scope, expires_at=expires_at)

    @classmethod
    def persist(cls, token):
        access_token = token['access_token']
        token_type = token['token_type']
        expires_at = token['expires_at']
        scope = token['scope']
        return cls.create(access_token, token_type, scope, expires_at)

    def to_dict(self):
        token_dict = {
            'access_token': self.access_token,
            'token_type': self.token_type,
            'scope': self.scope,
            'expires_at': self.expires_at,
        }
        return token_dict

    @classmethod
    def get_token(cls):
        try:
            token_cls = cls.objects.get()
            if token_cls.is_expired():
                token = oauth2.SpotifyClientCredentials().get_new_token()
                token_cls = token.persist(token)
                token._cls.save()
        except cls.DoesNotExist:
            token = oauth2.SpotifyClientCredentials().get_new_token()
            token_cls = token.persist(token)
            token_cls.save()
        return token_cls.to_dict()

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(ClientToken, self).save(*args, **kwargs)

    def is_expired(self):
        if self.expires_at - dt.datetime.utcnow().timestamp() < 60:
            return False
        return True
