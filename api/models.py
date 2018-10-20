from django.db import models
from spotifydj.users.models import User
import datetime as dt
from . import oauth2
import uuid

class Party(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def create(cls, host):
        return cls(host=host)

class Playlist(models.Model):
    name = models.CharField(max_length=64)
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='playlists')

    @classmethod
    def create(cls, name, party):
        return cls(name=name, party=party)

class Song(models.Model):
    uri = models.CharField(max_length=64)
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='songs')
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='songs')
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)

    @classmethod
    def create(cls, uri, name, artist, album, added_by, playlist):
        return cls(uri=uri, name=name, artist=artist, album=album, added_by=added_by, playlist=playlist)

    def modify_score(self, amount):
        self.score += amount
        self.save()
        return self.score

    def __str__(self):
        return self.name

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voted_songs')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='voted')
    vote = models.BooleanField()

    @classmethod
    def create(cls, user, song, vote):
        return cls(user=user, song=song, vote=vote)

class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=64)
    scope = models.CharField(max_length=1024)
    expires_at = models.BigIntegerField()
    refresh_token = models.CharField(max_length=255)

    def __str__(self):
        return ''.join([str(self.user), "'s token"])

    def save(self, *args, **kwargs):
        self.__class__.objects.filter(user=self.user).exclude(id=self.id).delete()
        super(UserToken, self).save(*args, **kwargs)

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

    def to_dict(self):
        token_dict = {
            'access_token': self.access_token,
            'token_type': self.token_type,
            'scope': self.scope,
            'expires_at': self.expires_at,
            'refresh_token': self.refresh_token,
        }
        return token_dict

    @classmethod
    def get_token(cls, user):
        try:
            token_cls = cls.objects.filter(user=user).get()
            if token_cls.is_expired():
                token = token_cls.to_dict()
                new_token = oauth2.SpotifyUserAuth(user=user, token=token).refresh_token()
                token_cls = cls.persist(token=new_token, user=user)
                token_cls.save()
        except cls.DoesNotExist:
            raise Exception("User has not authorized spotify access")
        return token_cls.to_dict()

    def is_expired(self):
        if dt.datetime.now().timestamp() - self.expires_at < 60:
            return False
        return True

class UserGrant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=255)
    scope = models.CharField(max_length=1025)
    timestamp_created = models.DateTimeField(default=dt.datetime.now)

    def __str__(self):
        return str(self.user) + "'s grant"

    @classmethod
    def create(cls, user, state, scope):
        return cls(user=user, state=state, scope=scope)

class ClientToken(models.Model):
    access_token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=255)
    scope = models.CharField(max_length=1024)
    expires_at = models.BigIntegerField(default=0)

    @classmethod
    def create(cls, access_token, token_type, scope, expires_at):
        return cls(access_token=access_token, token_type=token_type, scope=scope, expires_at=expires_at)

    @classmethod
    def get_token(cls):
        try:
            token_cls = cls.objects.get()
            if token_cls.is_expired():
                token = oauth2.SpotifyClientCredentials().get_new_token()
                token_cls = cls.persist(token)
                token_cls.save()
        except cls.DoesNotExist:
            token = oauth2.SpotifyClientCredentials().get_new_token()
            token_cls = cls.persist(token)
            token_cls.save()
        return token_cls.to_dict()

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

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(ClientToken, self).save(*args, **kwargs)

    def is_expired(self):
        if dt.datetime.now().timestamp() - self.expires_at  < 60:
            return False
        return True
