
from .methods.connect_to_endpoint import connect_to_api_endpoint
from datetime import datetime, timedelta
from utility.secret_manager import get_secret

client_id = '90d4133dd76d4b2c8adec68c9e302924'
client_secret = None

access_token_cache = None
access_token_cache_exp = None

access_token_duration_mins = 60

def store_cache(secret):
    global access_token_cache
    global access_token_cache_exp

    access_token_cache = secret
    access_token_cache_exp = datetime.now() + timedelta(minutes=access_token_duration_mins)

def get_access_token():
    '''
    Returns the access_token for spotify stored in AWS secret manager
    '''
    global client_secret
    client_secret = get_secret('client_secret_spotify','client_secret')
    #insert debug logger
    header = {
        'Content-Type' : 'application/x-www-form-urlencoded',
    }
    request_body = {
        'grant_type' : f'client_credentials',
        'client_id' : client_id,
        'client_secret' : client_secret
    }
    print(request_body)
    response, response_metadata = connect_to_api_endpoint(method='POST', url='https://accounts.spotify.com/api/token',header_params=header,data=request_body)

    if not response:
        print(f'Error occurred when getting access token for spotify API: {response_metadata}')
    
    access_token_cache = f"Bearer {response.get('access_token')}"
    store_cache(access_token_cache)

    return response_metadata

def get_search_results_info(query:str):
    '''
    Using the arg 'query' it uses a Spotify API endpoint to get related search results
    '''
    url = 'https://api.spotify.com/v1/search'
    query_params = {
        'q' : query,
        'limit' : '6',
        'offset' : '5',
        'type' : 'track'
    }
    if access_token_cache_exp:
        access_token_expired = True if access_token_cache_exp >= datetime.now() else False
    elif access_token_cache is None or access_token_cache_exp is None:
        access_token_expired = True

    if access_token_expired:
        get_access_token()
    print(f'{access_token_cache=}')
    header_params = {
        'Authorization' : access_token_cache
    }
    response, response_metadata  = connect_to_api_endpoint(method='GET', url=url, query_params=query_params,header_params=header_params)
    if not response:
        print(f'{response_metadata=}')
    return response