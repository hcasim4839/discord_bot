from bot_utilities import connect_to_api_endpoint,check_if_elapsed_time_passed
from datetime import datetime
from youtube_dl import YoutubeDL
from bot_utilities import get_secret, connect_to_api_endpoint
import json
from typing import Optional
import yt_dlp
import logging

logging.basicConfig(filename="app.log",
                    filemode="w", level=logging.DEBUG)

logger = logging.getLogger()

class Youtube():
    api_endpoint = {
        'search' : 'https://www.googleapis.com/youtube/v3/search'
    }
    def __init__(self):
        self.api_key = get_secret('youtube_api_key', 'api_key')
    
    #seems we need to use youtube data api to make the search and get the video id
    #and then use youtube_dl to download the file as an mp3 file
    def get_search_results_dict(self, search_query:str) -> dict:
        url = self.api_endpoint.get('search')
        query_param = {
            'key': self.api_key,
            'part': 'snippet',
            'type': 'video',
            'q': search_query
        }

        search_results_dict = connect_to_api_endpoint(url=url, query_parameters=query_param, http_method='GET')
        return search_results_dict
    
    def get_first_search_result_video_id(self, search_query: str) -> Optional[str]:
        search_results_dict = self.get_search_results_dict(search_query)
        print(search_results_dict)
        try:
            first_video_id = search_results_dict['items'][0]['id']['videoId']

            return first_video_id
        except Exception as e:
            return None
    def get_format_in_formats_dict(self, format, format_dict):
        result_list = []
        for entry in format_dict:
            if entry.get('format') == format:
                result_list.append(entry.get('url'))

        return result_list
    
    def get_audio_stream_url(self, video_id: str) -> Optional[str]:
        youtube_dl_options = {'format': 'bestaudio'}
        youtube_url = f'https://www.youtube.com/watch?v={video_id}'
        
        with yt_dlp.YoutubeDL(youtube_dl_options) as youtube_dl_manager:
            info = youtube_dl_manager.extract_info(url=youtube_url, download=False)
            logger.debug(f'The info: {info}')

            audio_url = self.grab_best_quality_sound(info)
            logger.debug(f"The audio url: {audio_url}")
            

        return audio_url
    def grab_best_quality_sound(self, json_obj) -> str:
        '''
        Returns the best possible sound quality found in the results from json obj
        '''


        best_format = json_obj.get("format")
        logger.debug(f"Best audio format: {best_format}")

        if best_format == None: return None

        formats_list = json_obj.get("formats")

        for entry in formats_list:
            if entry.get("format") == best_format:
                return entry.get("url")
        
        logger.error("Best audio URL was not found in format list")
        return None

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