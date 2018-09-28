from .models import ClientToken


class SpotifyAPI(object):

    def __init__(self, session):
        self.session = session

    def init_session(self):
        if ClienToken.load()
    def get(self, url, query, **kwargs):

        response = self.session.request(url, )

    def search_track(self, query, max_results=10):
        q = prepaire_query(query)
        type = 'track'

        self.session.request(method='GET', url='https://api.spotify.com/v1/search', query)


    def prepare_query(query):
        query = query.replace(' ', '%20')
        return query
