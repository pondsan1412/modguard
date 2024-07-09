import discord
from discord.ext import commands

class event(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        debugging_ch = discord.utils.get(self.bot.get_all_channels(), name="debugging")
        await debugging_ch.send('hello world')

async def setup(bot):
    await bot.add_cog(event)
    