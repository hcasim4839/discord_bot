from discord import Intents, Client
from my_client import MyClient
from bot_utilities import get_secret, check_if_elapsed_time_passed
from datetime import datetime
from discord.ext import commands
import discord
import os
access_token_cache = {
    'access_token_discord': None
}
client_secrets_cache = {
    'client_secret_spotify': None
}


intents = discord.Intents.default()
intents.message_content = True
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

bot = commands.Bot(command_prefix="!", intents=intents)

# Dynamically load cogs
async def load_cogs():
    for filename in os.listdir("./cogs/music"):
        print(f'{filename=}')
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"cogs.music.{filename[:-3]}")

@bot.event
async def on_ready():
    await load_cogs()
    print(f"Logged in as {bot.user}")

bot.run(access_token_cache.get('access_token_discord'))