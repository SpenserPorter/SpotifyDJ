from .models import ClientToken, UserToken
from api.oauth2 import SpotifyClientCredentials, SpotifyUserAuth
import json

class SpotifyAPI(object):

    def __init__(self, user):
        self.session = SpotifyUserAuth(user, token=UserToken.get_token(user))
        self.prefix = 'https://api.spotify.com/v1/'

    @staticmethod
    def prepare_params(values):
        query_params = ''
        for name, value in values.items():
            if name == 'type':
                value = ','.join(value)
            query_params += '&' + name + '=' + str(value)
        return query_params

    @staticmethod
    def prepare_query(query):
        query = query.replace(' ', '+')
        query = 'q=' + query
        return query

    def search_track(self, query, **kwargs):
        if kwargs:
            params = self.prepare_params(kwargs)
        else:
            params = ''
        q = self.prepare_query(query)
        url = self.prefix + 'search?' + q + params
        response = self.session.request(method='GET', url=url)
        json_string = response.text
        return json.loads(json_string)
