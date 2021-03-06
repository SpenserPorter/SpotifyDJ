from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from api.models import ClientToken, UserGrant, UserToken, Party, Song, Playlist
from spotifydj.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()

admin.site.register(UserToken)
admin.site.register(UserGrant)
admin.site.register(ClientToken)
admin.site.register(Party)
admin.site.register(Song)
admin.site.register(Playlist)

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]
