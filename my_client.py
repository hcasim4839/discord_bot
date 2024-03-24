import discord
from discord.ext import commands
import bot_utilities 
from dotenv import load_dotenv
import os
import datetime
import random 

class MyClient(discord.Client):
    load_dotenv()
    issuer = os.getenv("Issuer")

    start_bot_commands = {}
    spam_list = ['You are going to have to wait three minutes...','Try not to spam that',"It's quite expensive to start the servers you know!","You know this is using AWS resources too right?"]

    client = discord.Client(intents=discord.Intents.default())
    last_server_startup = None

    async def on_ready(self):
        print("Bot is ready")
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        
        if message.author.id in self.start_bot_commands and self.start_bot_commands[message.author.id] == 'start_server' and message.content.lower() == 'ya':
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

        is_last_server_cmd_usage_under_three = self.last_server_startup == None or datetime.datetime.now() - self.last_server_startup >= datetime.timedelta(minutes=3)

        if message.content.lower() == 'start' and is_last_server_cmd_usage_under_three:
            await message.channel.send(f'uh, hey! Do you want me to start the server?')
            self.start_bot_commands[message.author.id] = 'start_server'
            self.last_server_startup = datetime.datetime.now()
        if message.content.lower() == 'start' and not is_last_server_cmd_usage_under_three:
            message_index = random.randint(0,2)
            response = self.spam_list[message_index]
            await message.channel.send(response)
    
    async def ping_issuer_error(self,message, responseType, responseMessage):

        user_id = bot_utilities.get_secret('client_id_discord_user_id','client-id')
        user = self.client.get_user(user_id)
        
        if user:
            sub_message = f'the status code was: {responseType}' if responseType == int else 'it was an Exception error...'
            await user.send(f'Hey {self.issuer}, an issue occurred, The response message was: {responseMessage}\n Also {sub_message}')
        else:
            await message.channel.send(f'I could not send him the message...')