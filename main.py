import discord
from discord.ext import commands
import os
#call intents
def call_intents():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.presences = True
    return intents

class modguard(discord.Client):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
    
    async def setup_hook(self):
        self.bot.remove_command('help')
        cog_folder = "commands" 
        for filename in os.listdir(cog_folder):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = f"{cog_folder}.{filename[:-3]}"
                try:
                    await self.bot.load_extension(module_name)
                    print(f"Loaded extension: {module_name}")
                except Exception as e:
                    print(f"Failed to load extension {module_name}: {e}")

import secret_stuff
run_client = modguard
modguard_token = secret_stuff.pull_variables.fetch_token()
run_client.run(reconnect=True,root_logger=False,token=modguard_token)