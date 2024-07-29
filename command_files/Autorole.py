import discord
from discord.ext import commands

#@made class for autorole
class Autorole(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self,member:discord.Member):
        """keep an eyes when people join server and autorole 'Member' to them"""
        bot_guild = discord.utils.get(self.bot.guilds, name='Network Community')
        for guild in self.bot.guilds:
            if guild.name == 'Network Community':
                
        
        role_check = discord.utils.get(self.bot.)