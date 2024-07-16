import discord
from discord.ext import commands
from discord import app_commands,Embed
from easygoogletranslate import EasyGoogleTranslate
from googletrans import Translator
import discord.utils
from modules import function ,variables as v,switch_ as s
import re

class embed:
    def __init__(self)->None:
        pass

    async def check_switch_and_return_color(self):
        chk_sw_cl = s.tracking_message
        if chk_sw_cl != True:
            embed_color = discord.Colour.red()
        else:
            embed_color = discord.Colour.green()
        return embed_color
    
    async def check_bool_return_switch(self):
        chk_sw_cl = s.tracking_message
        if chk_sw_cl != True:
            switch_ = v.switch_off
        else:
            switch_ = v.switch_on
        return switch_
    
    async def embed_update(self):
        color = await self.check_switch_and_return_color()
        switch = await self.check_bool_return_switch()
        embed = discord.Embed(title='Auto Translate',color=color)
        embed.add_field(name='Automatic translates Toggle switch',value=f'<#1260062822285709433>')
        embed.set_image(url=f"{switch}")
        return embed
    
class context(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name="translate to english",
            callback=self.tl,
        )
        self.bot.tree.add_command(self.ctx_menu)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.ctx_menu.name,ype=self.ctx_menu.type)

    async def tl(self,i:discord.Interaction, msg:discord.Message):
        translator = EasyGoogleTranslate(
        source_language='auto',
        target_language='en',
        timeout=None
        )
        result = translator.translate(text=msg.content)
        await i.response.send_message(result)

    async def translator(self, message: str) -> str:
        trans = EasyGoogleTranslate(source_language='auto', target_language='en', timeout=None)
        translated = trans.translate(text=message)
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
                # ลบอีโมจิที่อยู่ในรูปแบบ :emoji_name: หรือ :number: หรือ <:number>
                
                translated = await self.translator(message=message.content)
                extracted, remaining = function.message.extract_message(message=translated)
                print(extracted,remaining)
                
                extracted_emoji, remaining_emoji = function.message.extract_custom_emoji(message=remaining)
                if extracted == ":pepost:":
                    return
                else:
                    await message.channel.send(f"{message.author.name}: {extracted} {remaining_emoji}")

    @commands.hybrid_command()
    async def switch_button_for_translator(self,ctx:commands.Context):
        if not await function.check_role(self=self,ctx=ctx):
            return
        
        await ctx.send(view=switch_button())
        
class switch_button(discord.ui.View):
    def __init__(self,superbot):
        super().__init__(timeout=None)
        self.bot = superbot
        self.embed_instance = embed()

    @discord.ui.button(label='on', style=discord.ButtonStyle.green)
    async def setup_button_on(self, ctx: discord.Interaction, button: discord.ui.Button):
        function.switch_button.switch_tracking_translator(button='on')
        embed_update = await self.embed_instance.embed_update()
        await ctx.response.edit_message(embed=embed_update,content='||False||')

    @discord.ui.button(label='off', style=discord.ButtonStyle.red)
    async def setup_button_off(self, ctx: discord.Interaction, button: discord.ui.Button):
        function.switch_button.switch_tracking_translator(button='off')
        embed_update = await self.embed_instance.embed_update()
        await ctx.response.edit_message(embed=embed_update,content='||True||')


async def setup(bot):
    await bot.add_cog(
        context(bot)
    )