from django.shortcuts import render
from django.http import HttpResponse
from .models import UserToken, UserGrant
from api import oauth2

def callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    grant = UserGrant.objects.filter(user=request.user).get()
    if validate_grant(grant, state):
        scope = grant.scope
        session = oauth2.SpotifyUserAuth(user=request.user, scope=scope)
        session.get_token_from_code(code)
        session.save_token()
        context = {
            'status': 'succesfully authorized'
        }
    else:
        context = {
            'status': 'Validation Failed'
        }
    return render(request,'api/authflow.html', context)

def validate_callback(grant, state):
    if state == grant.state:
        return True
    return False

def authorize(request):
    scope = ['user-modify-playback-state','playlist-modify-public']
    session = oauth2.SpotifyUserAuth(user=request.user, scope=scope)
    auth_url, state = session.get_auth_url_and_state()
    grant = UserGrant.create(request.user, state, scope)
    grant.save()
    context = {
        'auth_url': auth_url
    }
    return render(request, 'api/authflow.html', context)

def spotify_search(request, query=None):
    session = oauth2.SpotifyClientCredentials()
    token = session.get_new_token()
    context = {}
    return render(request, 'api/search.html', context)
