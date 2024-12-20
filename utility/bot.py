import discord

def get_voice_channels(guild:discord.guild):
    voice_channels = [channel for channel in guild.channels if isinstance(channel, discord.VoiceChannel)]
    return voice_channels