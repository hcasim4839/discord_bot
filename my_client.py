import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.users}')
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

        if message.content.startswith ("minecraft"):
            await message.channel.send("Do you want me to start the server?")