import discord
from discord.ext import commands
from discord import app_commands,Embed
from easygoogletranslate import EasyGoogleTranslate
import discord.utils

class context(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name="translate to english",
            callback=self.tl,
        )
        self.bot.tree.add_command(self.ctx_menu)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

    async def tl(self,i:discord.Interaction, msg:discord.Message):
        translator = EasyGoogleTranslate(
        source_language='auto',
        target_language='en',
        timeout=None
        )
        result = translator.translate(text=msg.content)
        await i.response.send_message(result)
    
    @commands.hybrid_command()
    async def switch_button_for_translator(self,ctx:commands.Context):
        pass

class switch_button(discord.ui.View):
    def __init__(self,timeout=None):
        super().__init__(timeout=timeout)

    @discord.ui.button(label='on',style=discord.ButtonStyle.green)
    async def setup_button_on(self,ctx:discord.Interaction,button:discord.ui.Button):
        await ctx.response.send_message('hi')

async def setup(bot):
    await bot.add_cog(
        context(bot)
    )