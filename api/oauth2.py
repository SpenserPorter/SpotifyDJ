from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import datetime as dt
import os

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
redirect_uri = 'http://127.0.0.1:8000/callback/'

class SpotifyClientCredentials(object):
    TOKEN_URL = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id=client_id, client_secret=client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = self.create_oauth_session()
        self.get_new_token()

    def get_new_token(self):
        auth = self.create_auth()
        client = self.create_client()
        self.token = self.session.fetch_token(
                                    token_url=self.TOKEN_URL,
                                    auth=auth,
                                    client=client
                                    )
        return self.token

    def create_oauth_session(self):
        client = self.create_client()
        return OAuth2Session(client=client)

    def create_client(self):
        client = BackendApplicationClient(client_id=self.client_id)
        return client

    def create_auth(self):
        auth = HTTPBasicAuth(self.client_id, self.client_secret)
        return auth

    def request(self, method, url):
        method = method.upper()
        if self.is_token_expired():
            self.get_new_token()
        response = self.session.request(method=method, url=url)
        return response

    def is_token_expired(self):
        if self.session.token['expires_at'] <= dt.datetime.utcnow().timestamp():
            return True
        return False

class SpotifyUserAuth(object):
    AUTHORIZE_URL_BASE = 'https://accounts.spotify.com/authorize'
    TOKEN_URL = 'https://accounts.spotify.com/api/token'

    def __init__(self, user, client_id=client_id, client_secret=client_secret,
                redirect_uri=redirect_uri, scope=['']):
        self.user = user
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.session = self.create_session()

    def create_session(self):
        auth = self.create_auth()
        session = OAuth2Session(
                            client_id=self.client_id,
                            redirect_uri=self.redirect_uri,
                            scope=self.scope,
                            )
        return session

    def get_token(self):
        return self.session.token

    def get_auth_url_and_state(self):
        authorization_url, state = self.session.authorization_url(self.AUTHORIZE_URL_BASE)
        return authorization_url, state

    def get_token_from_code(self, code):
        auth = self.create_auth()
        token = self.session.fetch_token(
                                    token_url=self.TOKEN_URL,
                                    auth=auth,
                                    code=code
                                    )
        return token

    def create_auth(self):
        auth = HTTPBasicAuth(self.client_id, self.client_secret)
        return auth
