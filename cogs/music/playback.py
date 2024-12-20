from discord.ext import commands
from discord import FFmpegPCMAudio
from cogs.music.utility.spotify import get_spotify_title_options
from utility.table_exporter import create_single_col_ascii_table
from cogs.music.utility.youtube import get_sound_url
from utility.text import add_multiple_reactions_to_message
from utility.bot import get_voice_channels
from discord.ext import commands
import time 
import asyncio

class MusicPlayback(commands.Cog):
    recent_requester_id = None
    song_choices_message_id = None
    title_options = None

    events_list = []
    events_list_max_size = 16
    reaction_mapping = {
        '1️⃣':0, '2️⃣':1, '3️⃣':2, '4️⃣':3, '5️⃣':4
    }

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='play',aliases=[],brief='Helps play music on the voice channel! Check details')
    async def play(self, ctx, *, song_title: str):
        'Command structure ex: !play Pokemon\n A list of music options will be sent with Pokemon as the topic.\n To choose the option click the appropriate numbered reaction.\n Option will be played on the music channel.'
        if self.events_list and ctx.author.id != self.recent_requester_id:
            await ctx.send('You\'ll have to wait your turn.')
        else:    
            self.recent_requester_id = ctx.author.id
            await self.playback_event_list_handler(ctx, {'eventName': 'play', 'requester_id': self.recent_requester_id})

            self.title_options = await self.get_song_choices(ctx, song_title=song_title)
            music_option_table = create_single_col_ascii_table(amt_of_rows=len(self.title_options), row_list=self.title_options,header_list=['Music Title'])
            print(music_option_table)
            music_option_table_message = await ctx.send(music_option_table)
            self.song_choices_message_id = music_option_table_message.id

            music_option_table = await add_multiple_reactions_to_message(music_option_table_message, ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣'])
            
        

    @commands.command(name='stop',aliases=[],brief='Stops playing music on the voice channel')
    async def stop(self, ctx):
        'Simply stops the track being played on the music channel if the requester is the same last requester for the !play command'
        stop_requester_id = ctx.author.id
        if stop_requester_id == self.recent_requester_id and ctx.voice_client:
            await self.playback_event_list_handler(ctx, {'eventName': 'stop', 'requester_id': self.recent_requester_id})
            await ctx.voice_client.disconnect()
        else:
            requester_message = ctx.message
            await add_multiple_reactions_to_message(requester_message,['😡'])
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.id == self.song_choices_message_id:
            # Retrieve the context from the message's channel
            ctx = await self.bot.get_context(reaction.message)
            last_index = len(self.events_list) - 1
            is_recent_requester = True if self.recent_requester_id == user.id else False
            
            if is_recent_requester:
                is_reaction_event = True if self.events_list[last_index].get('eventName') == 'reaction' else False
                if is_reaction_event:
                    await ctx.send('I\'m already playing a song on the voice channel, request to stop the music first')
                    return
            if user.id == self.recent_requester_id:
                song_title_index = self.reaction_mapping.get(reaction.emoji)
                song_title = self.title_options[song_title_index]
                await self.playback_event_list_handler(ctx, {'eventName': 'reaction', 'requester_id': self.recent_requester_id})
                await self.play_song_choice(ctx, song_title=song_title)

    async def playback_event_list_handler(self, ctx, event_dict: dict):
        
        print(f'The event {event_dict} is being added')
        self.events_list.append(event_dict)
        
        print(f'playback_event_list_handler is being called; event list:{self.events_list}')
        if event_dict.get('eventName') == 'stop':
            self.events_list.clear()
            return
        elif self.events_list and len(self.events_list) >= 2:
            essential_events = await self.get_essential_events()
            essential_events_last_index = len(essential_events) - 1
            print(f'{essential_events=}')
            if (essential_events[essential_events_last_index] == 'play' and essential_events[essential_events_last_index - 1] == 'play'):
                print(f"Last index: {essential_events_last_index}")
                latest_event = self.events_list[essential_events_last_index]
                if latest_event.get('requester_id') == self.recent_requester_id:
                    print(f'Stopping music')
                    self.stop(ctx)
        print(self.events_list)
        

    async def get_essential_events(self):
        essential_events = [essential_event for essential_event in self.events_list if essential_event != 'reaction']
        return essential_events
        

    async def event_list_size_handler(self, events_list: list):
        if len(self.events_list) > self.events_list_max_size:
            self.events_list.pop(0)



    async def get_song_choices(self, ctx, *, song_title):
        await ctx.send(f'This is the best that\'s available at this time for {song_title}:')
        title_options = get_spotify_title_options(song_title=song_title)
        return title_options

        
    async def play_song_choice(self, ctx, *, song_title: str):
        # Your Spotify integration logic here
        await ctx.send(f"Searching for {song_title}...")
        # Simulate getting a track URL and playing it
        url = get_sound_url(song_title)
        
        try:
            voice_channel = ctx.author.voice.channel
            vc = await voice_channel.connect()
        except AttributeError as e:
            time.sleep(1)
            await ctx.send("I'll go to the first audio channel")
            voice_channel = get_voice_channels(ctx.guild)[0]
            vc = await voice_channel.connect()

        async def after_playing(error):
            if error:
                print(f'An error occured: {error}')
            await self.playback_event_list_handler(ctx, {'eventName': 'stop', 'requester_id': self.recent_requester_id})
            await vc.disconnect()
            
        options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -vn'
        }
        loop = asyncio.get_event_loop()

        vc.play(FFmpegPCMAudio(url, **options), after=lambda e: loop.create_task(after_playing(e)))
        time.sleep(1)
        await ctx.send(f"Now playing: {song_title}")
    
    



async def setup(bot):
    await bot.add_cog(MusicPlayback(bot))