from django.conf import settings
from django.urls import include, path
from api import views

urlpatterns = [
    path("callback/", views.callback, name="callback"),
    path("authorize/", views.authorize, name="authorize"),
    path("search/", views.search, name="search"),
    path("search/<uuid:party_id>", views.search, name="search"),
    path("add/<uuid:party_id>/<slug:uri>", views.add_song_to_party, name="add"),
    path("party/", views.party, name="party"),
    path("party/new/", views.party, name="new_party"),
    path("party/<uuid:party_id>/", views.party, name="join_party"),
    path("party/<uuid:party_id>/<int:song_id>", views.vote, name="vote")
]
