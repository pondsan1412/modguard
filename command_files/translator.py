import discord
from discord.ext import commands

class translator(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    async def monitoring_user(self,msg:discord.Message)-> bool:
        pass
    async def tracking_message(self,msg:discord.Message):
        pass

async def setup(bot):
    await bot.add_cog(translator(bot))