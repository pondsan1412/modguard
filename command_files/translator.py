import discord
from discord.ext import commands
from discord import app_commands,Embed
from easygoogletranslate import EasyGoogleTranslate
from googletrans import Translator
import discord.utils
from modules import switch_,function
from modules import variables
import re
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

    async def translator(self, message: str) -> str:
        cleaned_message = re.sub(r'<[@#]\d+>', '', message)
        trans = EasyGoogleTranslate(source_language='auto', target_language='en', timeout=None)
        translated = trans.translate(text=cleaned_message)
        return translated

    
        

    @commands.Cog.listener()
    async def on_message(self,message:discord.Message):
        if message.author == self.bot.user: return
        
        def detect_lang(message_content:str)->str:
            trans = Translator()
            lang_detected = trans.detect(message_content).lang
            if lang_detected == 'en':
                return
            else:
                return lang_detected
        
        #feature tracking message to translate
        

        language_ch = "「🌏💬」𝓛𝓪𝓷𝓰𝓾𝓪𝓰𝓮"
        if message.channel.name == language_ch:
            if function.switch_button.check_switch() != True:
                return
            else:
                if not detect_lang(message.content):
                    return
                # ลบอีโมจิที่อยู่ในรูปแบบ :emoji_name:
                cleaned_message = re.sub(r':[a-zA-Z0-9_]+:', '', message.content)
                translated = await self.translator(message=cleaned_message)
                cleaned_message = re.sub(r'<[@#]\d+>', '', cleaned_message)
                await message.channel.send(f"`{cleaned_message}: {translated}`")



    @commands.hybrid_command()
    async def switch_button_for_translator(self,ctx:commands.Context):
        await ctx.send(view=switch_button())
        
class switch_button(discord.ui.View):
    def __init__(self,superbot):
        super().__init__(timeout=None)
        self.bot = superbot

    def embed_update(self):
        embed = discord.Embed(title='Auto Translate',color=discord.Colour.blue())
        embed.add_field(name='Switch on-off for auto translate in channel',value=f'<#1260062822285709433>')
        embed.add_field(name=f' ',value=f'Recent switch: **{function.switch_button.switch_return_string()}**',inline=False)
        return embed

    @discord.ui.button(label='on', style=discord.ButtonStyle.green)
    async def setup_button_on(self, ctx: discord.Interaction, button: discord.ui.Button):
        function.switch_button.switch_tracking_translator(button='on')
        await ctx.response.edit_message(embed=self.embed_update(),content='True')

    @discord.ui.button(label='off', style=discord.ButtonStyle.red)
    async def setup_button_off(self, ctx: discord.Interaction, button: discord.ui.Button):
        function.switch_button.switch_tracking_translator(button='off')
        await ctx.response.edit_message(embed=self.embed_update(),content='False')


async def setup(bot):
    await bot.add_cog(
        context(bot)
    )