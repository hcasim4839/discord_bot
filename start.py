from discord import Intents, Client
from my_client import MyClient
from bot_utilities import get_secret, check_if_elapsed_time_passed
from datetime import datetime

cache = {}

intents = Intents.default()
intents.message_content = True

client = Client(intents=intents)

if 'access_token_discord' in cache:
    has_elapsed_time_passed = check_if_elapsed_time_passed(cache.get('access_token_discord'), datetime.now(), 360)
    if has_elapsed_time_passed:
        token = get_secret('access_token_discord','access-token')
        cache['access_token_discord'] = token
    else:
        token = cache.get('access_token_discord')
else:
    token = get_secret('access_token_discord','access-token')
    cache['access_token_discord'] = token

client = MyClient(intents=intents)
client.run(token=token)