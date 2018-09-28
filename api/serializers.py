from rest_framework import serializers
from .models import UserToken, RefreshToken

class TokenSerializer(serializer.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'user',
            'access_token',
            'token_type',
            'scope',
            'expires_at'
        )
        model = models.UserToken
