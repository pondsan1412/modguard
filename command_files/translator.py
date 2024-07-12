import discord
from discord.ext import commands
from discord import app_commands,Embed
from easygoogletranslate import EasyGoogleTranslate
import discord.utils

class context(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name="Translate",
            callback=self.tl,
        )
        self.bot.tree.add_command(self.ctx_menu)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

    async def tl(self,i:discord.Interaction,msg:discord.Message):
        await i.response.send_message('hi')
    
    
async def setup(bot):
    await bot.add_cog(
        context(bot)
    )