from discord.ext import commands
from discord import app_commands
import discord
import subprocess

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='start_minecraft', description='Starts the minecraft server and returns the server IP address')
    async def start_minecraft(self, interaction: discord.Interaction):
        await interaction.response.send_message('Server is starting...')
        start_cmd = 'sudo systemctl start minecraft'.split()
        subprocess.run(start_cmd)
        # get bot to return ip address
        await interaction.followup.send(f'Server has started!')
                                                
    @app_commands.command(name='stop_minecraft', description='stops the minecraft server')
    async def stop_minecraft(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Server is closing...')

        stop_cmd = 'sudo systemctl stop minecraft'.split()
        subprocess.run(stop_cmd)
        await interaction.followup.send('Server is closed!')

    
async def setup(bot):
    await bot.add_cog(Minecraft(bot))