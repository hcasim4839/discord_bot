import yt_dlp
from utility.api.methods.connect_to_endpoint import connect_to_api_endpoint
from datetime import datetime, timedelta
from utility.secret_manager import get_secret


def get_sound_url(query:str):
    video_id = get_first_search_result_video_id(query)
    print(f'{query=}')
    print(f'{video_id=}')
    return get_audio_stream_url(video_id)

def get_search_results_dict(search_query:str) -> dict:
    
    api_key = get_secret('youtube_api_key', 'api_key')
    print(f'{api_key=}')
    url = 'https://www.googleapis.com/youtube/v3/search'
    query_params = {
        'key': api_key,
        'part': 'snippet',
        'type': 'video',
        'q': search_query
    }

    response, metadata = connect_to_api_endpoint(url=url, query_params=query_params, method='GET')
    print(f'youtube {response=}')
    print(f'youtube {metadata=}')
    if not response:
        print(metadata)
    return response

def get_first_search_result_video_id(search_query: str):
    search_results_dict = get_search_results_dict(search_query)
    try:
        first_video_id = search_results_dict['items'][0]['id']['videoId']

        return first_video_id
    except Exception as e:
        return None
        
def get_format_in_formats_dict(format, format_dict):
    result_list = []
    for entry in format_dict:
        if entry.get('format') == format:
            result_list.append(entry.get('url'))

    return result_list
    
def get_audio_stream_url(video_id: str):
    youtube_dl_options = {'format': 'bestaudio'}
    youtube_url = f'https://www.youtube.com/watch?v={video_id}'
        
    with yt_dlp.YoutubeDL(youtube_dl_options) as youtube_dl_manager:
        info = youtube_dl_manager.extract_info(url=youtube_url, download=False)

        audio_url = grab_best_quality_sound(info)    

    return audio_url

def grab_best_quality_sound(json_obj):
    '''
    Returns the best possible sound quality found in the results from json obj
    '''
    best_format = json_obj.get("format")
    print(f"Best audio format: {best_format}")

    if best_format == None: return None

    formats_list = json_obj.get("formats")

    for entry in formats_list:
        if entry.get("format") == best_format:
            return entry.get("url")
        
    print("Best audio URL was not found in format list")
    return None