import discord
from discord.ext import commands

#@made class for autorole
class Autorole(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self,member:discord.Member):
        """keep an eyes when people join server and autorole 'Member' to them"""
        if member.bot:
            gave_bot = discord.utils.get(member.guild.roles, name="bots")
            if gave_bot:
                await member.add_roles(gave_bot)
            else:
                return
        role = discord.utils.get(member.guild.roles, name="Member")
        if role:
            await member.add_roles(role)
        else:
            return
        
        