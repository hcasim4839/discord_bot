from utility.api.spotify import get_search_results_info

def get_spotify_title_options(song_title: str):
    '''
    song_title arg is used to check an endpoint in Spotify API to check relevant songs using arg
    '''
    results = get_search_results_info(song_title)
    print(f'{results=}')
    title_list = format_spotify_title_dict(results)

    return title_list

def format_spotify_title_dict(spotify_response):
    album_items = spotify_response.get('tracks').get('items')
    title_list = []

    for album in album_items:
        title_list.append(album.get('album').get('name'))
    
    return title_list

