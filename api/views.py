from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import UserToken, UserGrant, Party, Playlist, Song
from .forms import SearchBox, AddTrack, JoinParty, NewParty
from . import oauth2
from api.spotify import SpotifyAPI

def callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    grant = UserGrant.objects.filter(user=request.user ).latest('timestamp_created')
    if validate_grant(grant, state):
        credential_manager = oauth2.SpotifyUserAuth(user=request.user)
        credential_manager.get_token_from_code(code)
        token = credential_manager.get_token()
        user_token = UserToken.persist(token, user=request.user)
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
    session = oauth2.SpotifyUserAuth(user=request.user)
    auth_url, state = session.get_auth_url_and_state()
    grant = UserGrant.create(request.user, state, session.scope)
    grant.save()
    context = {
        'auth_url': auth_url,
        'user_auth_status': request.user.is_authenticated
    }
    return render(request, 'api/authflow.html', context)

def party(request, party_id=None):
    if party_id == None and request.method == 'GET':
        join_form = JoinParty()
        new_form = NewParty()
        context = {
            'join_party_form': join_form,
            'new_party_form': new_form
        }
    if request.method == 'POST' and party_id == None:
        if 'new' in request.POST:
            form = NewParty(request.POST)
            new_party = Party.create(host=request.user)
            new_party.save()
            new_playlist = Playlist.create(name=request.user.name, party=new_party)
            new_playlist.save()
            party_id = new_party.id
        if 'join' in request.POST:
            form = JoinParty(request.POST)
            if form.is_valid():
                party_id = form.cleaned_data['party_id']
        return redirect(party, party_id=party_id)

    if party_id:
        listening_party = Party.objects.filter(id=party_id).get()
        playlist = listening_party.playlists.get()
        songs_list = []
        if playlist.songs.exists():
            songs_list = list(playlist.songs.all())
        context = {
            'party_id': party_id,
            'party_host': listening_party.host,
            'playlist': playlist,
            'songs_list': songs_list
        }
    return render(request, 'api/party.html', context)

def add(request, uri, party_id):
    party_obj = Party.objects.filter(id=party_id).get()
    playlist = party_obj.playlists.get()
    spotify = SpotifyAPI(user=request.user, token=UserToken.get_token(request.user))
    song_info = spotify.get_tracks(uri)['tracks'][0]
    song_uri = uri
    song_name = song_info['name']
    song_artist = song_info['album']['artists'][0]['name']
    song_album = song_info['album']['name']
    song_added_by = request.user
    song = Song.create(
                song_uri,
                song_name,
                song_artist,
                song_album,
                song_added_by,
                playlist
                )
    song.save()
    return redirect(party, party_id=party_id)

def search(request, query=None, party_id=None):
    context = {}
    if party_id:
        context['party_id'] = str(party_id)
    if request.method == 'POST':
        form = SearchBox(request.POST)
        if form.is_valid():
            add_form = AddTrack()
            context['add_form'] = add_form
            query = form.cleaned_data['query']
            spotify = SpotifyAPI(user=request.user, token=UserToken.get_token(request.user))
            types = ['track', 'artist', 'album']
            results = spotify.search_track(query, type=types, limit=20)
            items = results['tracks']['items']
            context['results'] = items
    form = SearchBox()
    context['form'] = form
    return render(request, 'api/search.html', context)

def play(request, uri):
    spotify = SpotifyAPI(user=request.user, token=UserToken.get_token(request.user))
    response = spotify.play_tracks(uri)
    context = {
        'uri': uri,
        'response': response.text
    }
    return render (request, 'api/test_results.html', context)
