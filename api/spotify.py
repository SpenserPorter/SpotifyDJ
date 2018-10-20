from api.oauth2 import SpotifyClientCredentials, SpotifyUserAuth
import json

class SpotifyAPI(object):

    def __init__(self, user, token):
        if user:
            self.session = SpotifyUserAuth(user, token=token)
        else:
            self.session = SpotifyClientCredentials(token=token)
        self.prefix = 'https://api.spotify.com/v1/'

    @staticmethod
    def prepare_params(values):
        query_params = ''
        param_count = 0
        for name, value in values.items():
            if isinstance(value, list):
                value = ",".join(value)
            if param_count > 0:
                query_params += '&' + name + '=' + str(value)
            else:
                query_params += '?' + name + '=' + str(value)
            param_count += 1
        return query_params

    @staticmethod
    def prepare_query(query):
        query = query.replace(' ', '+')
        return query

    def search_track(self, query, **kwargs):
        if kwargs:
            kwargs['q'] = self.prepare_query(query)
            params = self.prepare_params(kwargs)
        else:
            query = {'q': self.prepare_query(query)}
            params = self.prepare_params(query)
        url = self.prefix + 'search' + params
        response = self.session.request(method='GET', url=url)
        json_string = response.text
        return json.loads(json_string)

    def get_tracks(self, track_ids):
        params = self.prepare_params({'ids':track_ids})
        url = self.prefix + 'tracks' + params
        response = self.session.request(method='GET', url=url)
        response.raise_for_status()
        json_string = response.text
        return json.loads(json_string)

    @staticmethod
    def prepare_uri(uri, type):
        return 'spotify:' + type + ':' + uri

    @staticmethod
    def add_kwargs_to_payload(kwargs, payload):
        for key, value in kwargs.items():
            payload[key] = value
        return payload

    def play_tracks(self, uris, device_id=None, **kwargs):
        if device_id:
            params = {'device_id': device_id}
            query_params = self.prepare_params(params)
        else:
            query_params = ''
        if isinstance(uris, list):
            track_uri_list = []
            for track_uri in uris:
                track_uri = self.prepare_uri(uri=track_uri, type='track')
                track_uri_list.append(track_uri)
        else:
            track_uri = self.prepare_uri(uris, type='track')
            track_uri_list = [track_uri]
        payload = {
            'uris': track_uri_list
        }
        if kwargs:
            payload = add_kwargs_to_payload(kwargs, payload)

        payload = json.dumps(payload)
        url = self.prefix + "me/player/play" + query_params
        response = self.session.request(method='PUT', url=url, data=payload)
        return response
