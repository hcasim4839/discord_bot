from bot_utilities import connect_to_api_endpoint,check_if_elapsed_time_passed
from datetime import datetime

class Spotify():
    client_id = '90d4133dd76d4b2c8adec68c9e302924'
    client_secret = None

    access_token = None
    access_token_datetime = None

    
    def __init__(self, client_secret):
        self.client_secret = client_secret
        self.get_access_token()

    def get_access_token(self):
        header = {
            'Content-Type' : 'application/x-www-form-urlencoded',
        }
        request_body = {
            'grant_type' : f'client_credentials',
            'client_id' : self.client_id,
            'client_secret' : self.client_secret
        }
        result = connect_to_api_endpoint(http_method='POST', url='https://accounts.spotify.com/api/token',header=header,data=request_body)
        self.access_token = f"Bearer {result.get('access_token')}"
        self.access_token_datetime = datetime.now()
    
    def get_track_names_and_artist(self, tracks_list):
        result_list = []
        print(f'In the music_spotify: {tracks_list}')
        for track in tracks_list:
            new_entry = [
                track['album']['artists'][0]['name'],
                track['name'],
                ]
            result_list.append(new_entry)
        return result_list


    def get_track_info(self,keyword):

        url = 'https://api.spotify.com/v1/search'
        query_params = {
            'q' : keyword,
            'limit' : '6',
            'offset' : '5',
            'type' : 'track'
        }
        access_token_expired = check_if_elapsed_time_passed(self.access_token_datetime,datetime.now(), 60)
        if access_token_expired:
            self.get_access_token()
        header_params = {
            'Authorization' : self.access_token
        }
        search_result = connect_to_api_endpoint(http_method='GET', url=url, query_parameters=query_params,header=header_params)
        return search_result['tracks']['items']