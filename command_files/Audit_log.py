import discord
from discord.ext import commands
from datetime import datetime
class Audit_log(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
        self.logs_ch = self.bot.get_channel(1267379950877671496) 

    #@even
    @commands.Cog.listener()
    async def on_message_delete(self,message:discord.Message):

        #save message log
        e_log = discord.Embed(title='Deleted message',color=discord.Color.red())
        e_log.add_field(name='Content',value=f"{message}")
        e_log.set_author(
            name=message.author.name if message.author.name else None,
            url = None,
            icon_url=message.author.avatar.url if message.author.avatar.url else None,
        )

        e_log.set_footer(text=f'time: {datetime.now()}')
        
        await self.logs_ch.send(embed=e_log)
    
    #@even on edit
    @commands.Cog.listener()
    async def on_message_edit(self,before:discord.Message,after:discord.Message):
        
        e_log = discord.Embed(title='Editted message', color=discord.Color.yellow())
        e_log.add_field(
            name=before.author.name,
            value=f"before edit: `{before.content}`\n after editted: {after.content}"
        )
        e_log.set_author(
            name=before.author.name,
            url=None,
            icon_url=before.author.avatar.url if before.author.avatar.url else None        )
        await self.logs_ch.send(embed=e_log)
    
async def setup(bot):
    await bot.add_cog(Audit_log(bot))