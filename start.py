from discord import Intents, Client
from my_client import MyClient
from bot_utilities import get_secret


intents = Intents.default()
intents.message_content = True

client = Client(intents=intents)

token = get_secret('access_token_discord',"access-token")

client = MyClient(intents=intents)
client.run(token=token)