import discord

async def add_multiple_reactions_to_message(message:discord.message, reactions:list):
    for reaction in reactions:
        await message.add_reaction(reaction)
    return message



