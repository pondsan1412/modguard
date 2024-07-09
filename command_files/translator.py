import discord
from discord.ext import commands

class translator(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name='test')
    async def test(self,variables:commands.Context):
        await variables.send('hello world')


async def setup(bot):
    await bot.add_cog(translator(bot))