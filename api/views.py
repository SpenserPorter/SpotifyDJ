from django.shortcuts import render
from django.http import HttpResponse
from .models import UserToken, UserGrant
from .forms import SearchBox
from . import oauth2
from api.spotify import SpotifyAPI

def callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    grant = UserGrant.objects.filter(user=request.user ).latest('timestamp_created')
    if validate_grant(grant, state):
        scope = grant.scope
        credential_manager = oauth2.SpotifyUserAuth(user=request.user, scope=scope)
        credential_manager.get_token_from_code(code)
        user_token = UserToken.persist(token=credential_manager.get_token(), user=request.user)
        user_token.save()
        context = {
            'status': 'succesfully authorized'
        }
    else:
        context = {
            'status': 'Validation Failed'
        }
    return render(request,'api/authflow.html', context)

def validate_grant(grant, state):
    if state == grant.state:
        return True
    return False

def authorize(request):
    scope = 'user-modify-playback-state playlist-modify-public'
    session = oauth2.SpotifyUserAuth(user=request.user, scope=scope)
    auth_url, state = session.get_auth_url_and_state()
    grant = UserGrant.create(request.user, state, scope)
    grant.save()
    context = {
        'auth_url': auth_url
    }
    return render(request, 'api/authflow.html', context)

def search(request, query=None):
    context = {}
    if request.method == 'POST':
        form = SearchBox(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            spotify = SpotifyAPI()
            types = ['track']
            response = spotify.search_track(query, types, limit=10)
            context['results'] = response.json()
    form = SearchBox()
    context['form'] = form
    return render(request, 'api/search.html', context)
