from bot_utilities import connect_to_api_endpoint

class Spotify():
    access_token = None

    
    def __init__(self, client_secret):
        client_id = '90d4133dd76d4b2c8adec68c9e302924'
        header = {
            'Content-Type' : 'application/x-www-form-urlencoded',
        }
        request_body = {
            'grant_type' : f'client_credentials',
            'client_id' : client_id,
            'client_secret' : client_secret
        }
        result = connect_to_api_endpoint(http_method='POST', url='https://accounts.spotify.com/api/token',header_dict=header,data=request_body)
        self.access_token = f"Bearer {result.get('access_token')}"

        print(f'works {self.access_token}')
    def get_track_names_and_artist(self, tracks_list):
        result_list = []
        print(f'In the music_spotify: {tracks_list}')
        for track in tracks_list:
            print(f'The current track: {track}')
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
        header_params = {
            'Authorization' : self.access_token
        }
        search_result = connect_to_api_endpoint(http_method='GET', url=url, query_parameters_dict=query_params,header_dict=header_params)
        return search_result['tracks']['items']