import discord
from discord.ext import commands

class translator(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    async def check_bool()-> bool:
        return False
    async def callback_user_id(self) ->int:
        return 0
    
async def setup(bot):
    await bot.add_cog(translator(bot))