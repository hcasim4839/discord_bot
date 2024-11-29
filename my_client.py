import discord
from discord.ext import commands
import bot_utilities 
from dotenv import load_dotenv
import os
import datetime
import random 
from music_spotify import Spotify
from music_spotify import Youtube
from discord import FFmpegPCMAudio

class MyClient(discord.Client):
    load_dotenv()
    issuer = os.getenv("Issuer")
    spotify_player = None
    youtube = None
    spotify_player_dict = {
        'bots_table_message_id': None,
        'client_id': None,
        'initiated_datetime': None,
        'music_search_query_list': None
    }

    start_bot_commands = {}
    spam_list = ['You are going to have to wait three minutes...','Try not to spam that',"It's quite expensive to start the servers you know!","You know this is using AWS resources too right?"]

    last_server_startup = None
    def __init__(self,client_secret_cache, intents, *args, **kwargs):
        super().__init__(*args, **kwargs, intents=intents)
        spotify_client_secret = client_secret_cache['client_secret_spotify']
        self.spotify_player = Spotify(spotify_client_secret)
        self.youtube = Youtube()
        

        
    async def on_raw_reaction_add(self, payload):
        
        url = await self.check_spotify_player(payload)
        voice_channel = self.guilds[0].voice_channels[0]
        vc = await voice_channel.connect()
        vc.play(FFmpegPCMAudio(url))

    async def on_ready(self):
        print("Bot is ready")
    def insert_music_search_query_to_player(self, tracks_and_artist_list):
        search_query_list = []
        for artist_and_track in tracks_and_artist_list:
            new_music_query = f'{artist_and_track[1]} song by "{artist_and_track[0]}"'
            search_query_list.append(new_music_query)
        
        self.spotify_player_dict['music_search_query_list'] = search_query_list

    async def on_message(self, message):
        
        user_text = message.content
        print(f'Message from {message.author}: {user_text}')
        if message.author.id in self.start_bot_commands and self.start_bot_commands[message.author.id] == 'find_track' and user_text:
            self.start_bot_commands[message.author.id] = None
            tracks_list = self.spotify_player.get_track_info(user_text)
            tracks_and_artist_list = self.spotify_player.get_track_names_and_artist(tracks_list)
            amt_of_row = len(tracks_and_artist_list)

            table = bot_utilities.create_ascii_table(amt_of_rows=amt_of_row, row_list=tracks_and_artist_list,header_list=['Artist Name', 'Track Name'])
            bot_message = f'Soo, I\'m getting these song results:`\n{table}`'
            reaction_list = ['1️⃣','2️⃣','3️⃣', '4️⃣', '5️⃣', '6️⃣']

            self.insert_music_search_query_to_player(tracks_and_artist_list)
            sent_bot_message = await message.channel.send(bot_message)
            
            self.spotify_player_dict['bots_table_message_id'] = sent_bot_message.id 
            self.spotify_player_dict['client_id'] = message.author.id
            self.spotify_player_dict['initiated_datetime'] = datetime.datetime.now()

            await bot_utilities.insert_reactions_to_message(sent_bot_message,reaction_list)
            


        if message.author.id in self.start_bot_commands and self.start_bot_commands[message.author.id] == 'start_server' and user_text.lower() == 'ya':
            informing_issuer_msg = f'I\'ll ping {self.issuer}'

            await message.channel.send(f'alright, starting it up.')

            responseType, responseMessage = bot_utilities.start_server("Minecraft")

            if isinstance(responseType, Exception):
                await message.channel.send(f'Seems like some coding issue:\n{responseMessage}\n{informing_issuer_msg}')
                await message.channel.send(f'Feel free to help him with the issue')
                await self.ping_issuer_error(message=message,responseType=responseType, responseMessage=responseMessage)

            if isinstance(responseType, int) and responseType == 200:
                await message.channel.send(f'Server has started!')
            else:
                await message.channel.send(f'Something went wrong in the pipeline!\n{informing_issuer_msg}')
                await self.ping_issuer_error(message=message,responseType=responseType, responseMessage=responseMessage)

        is_last_server_cmd_usage_under_three = self.last_server_startup == None or bot_utilities.check_if_elapsed_time_passed(self.last_server_startup,datetime.datetime.now(), 3)

        if user_text.lower() == 'play':
            await message.channel.send(f'So you want to play music?\nName the track, thanks!')
            self.start_bot_commands[message.author.id] = "find_track"
        elif user_text.lower() == 'start' and is_last_server_cmd_usage_under_three:
            await message.channel.send(f'uh, hey! Do you want me to start the server?')
            self.start_bot_commands[message.author.id] = 'start_server'
            self.last_server_startup = datetime.datetime.now()
        if user_text.lower() == 'start' and not is_last_server_cmd_usage_under_three:
            message_index = random.randint(0,2)
            response = self.spam_list[message_index]
            await message.channel.send(response)
    
    async def check_spotify_player(self, payload):
        channel = self.get_channel(payload.channel_id)
        is_spotify_player_off = bot_utilities.check_if_elapsed_time_passed(self.spotify_player_dict['initiated_datetime'], datetime.datetime.now(), 1)

        if is_spotify_player_off:
            await channel.send(f'The player has shut down, you took too long.')
        else:
            user = payload.user_id
            is_reaction_on_music_player_table = True if payload.message_id == self.spotify_player_dict.get('bots_table_message_id') else False
            is_reaction_by_appropriate_user = True if user == self.spotify_player_dict.get('client_id') else False

            if is_reaction_on_music_player_table and is_reaction_by_appropriate_user:
                await channel.send(f'You reacted! Great, I\'ll be on the voice channel')
                #check what the reaction was and transform to int and then query youtube class with that search 
                user_choice = self.spotify_player_dict.get('music_search_query_list')[2]

                id = self.youtube.get_first_search_result_video_id(user_choice)
                audio_url = self.youtube.get_audio_stream_url(id)

                await channel.send(f'The audio url is: {audio_url}, enjoy!')
                return audio_url
                
                

    async def ping_issuer_error(self,message, responseType, responseMessage):

        user_id = bot_utilities.get_secret('client_id_discord_user_id','client-id')
        user_id = int(user_id)
        user = self.client.get_user(user_id)
        
        if user:
            sub_message = f'the status code was: {responseType}' if responseType == int else 'it was an Exception error...'
            await user.send(f'Hey {self.issuer}, an issue occurred, The response message was: {responseMessage}\n Also {sub_message}')
        else:
            await message.channel.send(f'I could not send him the message...')