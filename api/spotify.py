#from .models import ClientToken
from api.oauth2 import SpotifyClientCredentials


class SpotifyAPI(object):

    def __init__(self):
        self.session = SpotifyClientCredentials()
        self.prefix = 'https://api.spotify.com/v1/'
        self.session.get_new_token()

    def get(self, url, query, **kwargs):
        response = self.session.request(url, q=query)
        return response

    def search_track(self, query, types, limit):
        q = self.prepare_query(query, types, limit)
        url = self.prefix + 'search?' + q
        response = self.session.request(method='GET', url=url)
        return response

    @staticmethod
    def prepare_query(query, types, limit):
        query = query.replace(' ', '%20')
        query = 'q=' + query + '&type=' + ','.join(types) + '&limit=' + str(limit)
        return query
