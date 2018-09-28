from django.conf import settings
from django.urls import include, path
from api import views

urlpatterns = [
    path("callback/", views.callback, name="callback"),
    path("authorize/", views.authorize, name="authorize")
]
