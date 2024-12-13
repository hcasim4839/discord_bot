from discord import Intents, Client
from my_client import MyClient
from bot_utilities import get_secret, check_if_elapsed_time_passed
from datetime import datetime

access_token_cache = {
    'access_token_discord': None
}
client_secrets_cache = {
    'client_secret_spotify': None
}

intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

#setting up credentials and caching them
if access_token_cache.get('access_token_discord'):
    has_elapsed_time_passed = check_if_elapsed_time_passed(access_token_cache.get('access_token_discord'), datetime.now(), 360)
    if has_elapsed_time_passed:
        token = get_secret('access_token_discord','access-token')
        access_token_cache['access_token_discord'] = token
    else:
        token = access_token_cache.get('access_token_discord')
else:
    token = get_secret('access_token_discord','access-token')
    access_token_cache['access_token_discord'] = token

for key, value in client_secrets_cache.items():
    if value is None:
        secret = get_secret(key,'client_secret')    
        client_secrets_cache['client_secret_spotify'] = secret



client = MyClient(client_secrets_cache, intents=intents)
client.run(token=token)