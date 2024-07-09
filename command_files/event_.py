import discord
from discord.ext import commands

class event(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author == self.bot.user: return
        
    

async def setup(bot):
    await bot.add_cog(event(bot))
    