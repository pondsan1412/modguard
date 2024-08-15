import discord
from discord.ext import commands
import shlex
import random
import asyncio
from modules import variables as v

class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command()
    async def random_things(self, ctx: commands.Context, *, things: str):
        """Random anything you want sorted by ',' or '|' """

        if "|" in things:
            delimiter = "|"
        elif "," in things:
            delimiter = ","
        else:
            delimiter = None

        if delimiter is not None:
            thing = things.split(delimiter)
        else:
            thing = shlex.split(things)

        random_thing = random.choice(thing)  # Choose randomly from the list of things

        def random_time():
            time_ = [ 2, 3, 4, 5,6]
            return random.choice(time_)

        if ctx:
            message = await ctx.send(content=f'{v.loading_system}')
            await asyncio.sleep(random_time())
            await message.edit(content=f'{random_thing}')
    @commands.command(name='invite')
    async def invite(self,ctx:commands.Context):
        guild = discord.utils.get(self.bot.guilds, name='Network Community')
        guildid = self.bot.get_guild(guild.id)
        if guildid is None:
            return
        
        channel = guildid.text_channels[0]
        invite = await channel.create_invite(max_age=0,max_uses=0)

        await ctx.send(f"{invite.url}")
async def setup(bot):
   await bot.add_cog(General(bot))
