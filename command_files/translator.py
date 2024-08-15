import discord
from discord.ext import commands
from discord import app_commands,Embed
from easygoogletranslate import EasyGoogleTranslate
from googletrans import Translator
import discord.utils
from modules import function ,variables as v,switch_ as s
import re
from discord.app_commands import Choice
from discord import app_commands
from googletrans import Translator,LANGUAGES
from typing import List
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

    # ตรวจจับภาษาต้นทางแบบออโต้ และแปลภาษาออกไปตามที่รับค่ามาจาก emoji
    async def auto_trans(self, message: str, lang: str):
        trans = EasyGoogleTranslate(
            source_language='auto',
            target_language=lang,
            timeout=None
        )
        return trans.translate(text=message)
        


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
                if message.content.startswith("!"):return
                translated = await self.translator(message=message.content)
                extracted, remaining = function.message.extract_message(message=translated)
                print(extracted,remaining)
                
                extracted_emoji, remaining_emoji = function.message.extract_custom_emoji(message=remaining)
                if extracted == ":pepost:":
                    return
                else:
                    await message.channel.send(f"{message.author.name}: {extracted} {remaining_emoji}")
    
    #สร้างเหตการณ์ รอ reaction emoji ธงชาติต่างๆเพื่อแปลข้อความเป็นภาษานั้นๆ
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        if user == self.bot.user:
            return

        message = reaction.message
        # ตรวจสอบว่ามีอีโมจิที่เป็นธงชาติทั้งหมดใน Discord
        flag_emojis = {
            '🇦🇫': 'fa', '🇦🇱': 'sq', '🇩🇿': 'ar', '🇦🇸': 'sm', '🇦🇩': 'ca', '🇦🇴': 'pt', '🇦🇮': 'en',
            '🇦🇶': 'es', '🇦🇬': 'en', '🇦🇷': 'es', '🇦🇲': 'hy', '🇦🇼': 'nl', '🇦🇺': 'en', '🇦🇹': 'de',
            '🇦🇿': 'az', '🇧🇸': 'en', '🇧🇭': 'ar', '🇧🇩': 'bn', '🇧🇧': 'en', '🇧🇾': 'be', '🇧🇪': 'nl',
            '🇧🇿': 'en', '🇧🇯': 'fr', '🇧🇲': 'en', '🇧🇹': 'dz', '🇧🇴': 'es', '🇧🇦': 'bs', '🇧🇼': 'en',
            '🇧🇷': 'pt', '🇧🇳': 'ms', '🇧🇬': 'bg', '🇧🇫': 'fr', '🇧🇮': 'fr', '🇨🇻': 'pt', '🇰🇭': 'km',
            '🇨🇲': 'fr', '🇨🇦': 'en', '🇨🇫': 'fr', '🇹🇩': 'fr', '🇨🇱': 'es', '🇨🇳': 'zh', '🇨🇴': 'es',
            '🇰🇲': 'ar', '🇨🇬': 'fr', '🇨🇩': 'fr', '🇨🇷': 'es', '🇨🇮': 'fr', '🇭🇷': 'hr', '🇨🇺': 'es',
            '🇨🇾': 'el', '🇨🇿': 'cs', '🇩🇰': 'da', '🇩🇯': 'fr', '🇩🇲': 'en', '🇩🇴': 'es', '🇪🇨': 'es',
            '🇪🇬': 'ar', '🇸🇻': 'es', '🇬🇶': 'es', '🇪🇷': 'ti', '🇪🇪': 'et', '🇪🇹': 'am', '🇫🇯': 'en',
            '🇫🇮': 'fi', '🇫🇷': 'fr', '🇬🇦': 'fr', '🇬🇲': 'en', '🇬🇪': 'ka', '🇩🇪': 'de', '🇬🇭': 'en',
            '🇬🇷': 'el', '🇬🇩': 'en', '🇬🇹': 'es', '🇬🇳': 'fr', '🇬🇼': 'pt', '🇬🇾': 'en', '🇭🇹': 'fr',
            '🇭🇳': 'es', '🇭🇺': 'hu', '🇮🇸': 'is', '🇮🇳': 'hi', '🇮🇩': 'id', '🇮🇷': 'fa', '🇮🇶': 'ar',
            '🇮🇪': 'en', '🇮🇱': 'he', '🇮🇹': 'it', '🇯🇲': 'en', '🇯🇵': 'ja', '🇯🇴': 'ar', '🇰🇿': 'kk',
            '🇰🇪': 'sw', '🇰🇮': 'en', '🇰🇵': 'ko', '🇰🇷': 'ko', '🇰🇼': 'ar', '🇰🇬': 'ky', '🇱🇦': 'lo',
            '🇱🇻': 'lv', '🇱🇧': 'ar', '🇱🇸': 'en', '🇱🇷': 'en', '🇱🇾': 'ar', '🇱🇮': 'de', '🇱🇹': 'lt',
            '🇱🇺': 'fr', '🇲🇬': 'fr', '🇲🇼': 'en', '🇲🇾': 'ms', '🇲🇻': 'dv', '🇲🇱': 'fr', '🇲🇹': 'mt',
            '🇲🇭': 'en', '🇲🇶': 'fr', '🇲🇷': 'ar', '🇲🇺': 'en', '🇲🇽': 'es', '🇫🇲': 'en', '🇲🇩': 'ro',
            '🇲🇨': 'fr', '🇲🇳': 'mn', '🇲🇪': 'sr', '🇲🇦': 'ar', '🇲🇿': 'pt', '🇲🇲': 'my', '🇳🇦': 'en',
            '🇳🇷': 'en', '🇳🇵': 'ne', '🇳🇱': 'nl', '🇳🇨': 'fr', '🇳🇿': 'en', '🇳🇮': 'es', '🇳🇪': 'fr',
            '🇳🇬': 'en', '🇳🇺': 'ni', '🇳🇫': 'en', '🇲🇰': 'mk', '🇲🇵': 'en', '🇳🇴': 'no', '🇴🇲': 'ar',
            '🇵🇰': 'ur', '🇵🇼': 'en', '🇵🇸': 'ar', '🇵🇦': 'es', '🇵🇬': 'en', '🇵🇾': 'es', '🇵🇪': 'es',
            '🇵🇭': 'en', '🇵🇱': 'pl', '🇵🇹': 'pt', '🇶🇦': 'ar', '🇷🇴': 'ro', '🇷🇺': 'ru', '🇷🇼': 'rw',
            '🇼🇸': 'sm', '🇸🇲': 'it', '🇸🇦': 'ar', '🇸🇳': 'fr', '🇷🇸': 'sr', '🇸🇨': 'fr', '🇸🇱': 'en',
            '🇸🇬': 'en', '🇸🇰': 'sk', '🇸🇮': 'sl', '🇸🇧': 'en', '🇸🇴': 'so', '🇿🇦': 'af', '🇪🇸': 'es',
            '🇱🇰': 'si', '🇸🇩': 'ar', '🇸🇷': 'nl', '🇸🇿': 'en', '🇸🇪': 'sv', '🇨🇭': 'de', '🇸🇾': 'ar',
            '🇹🇼': 'zh', '🇹🇯': 'tg', '🇹🇿': 'sw', '🇹🇭': 'th', '🇹🇬': 'fr', '🇹🇴': 'to', '🇹🇹': 'en',
            '🇹🇳': 'ar', '🇹🇷': 'tr', '🇹🇲': 'tk', '🇹🇻': 'en', '🇺🇬': 'en', '🇺🇦': 'uk', '🇦🇪': 'ar',
            '🇬🇧': 'en', '🇺🇸': 'en', '🇺🇾': 'es', '🇺🇿': 'uz', '🇻🇺': 'bi', '🇻🇦': 'it', '🇻🇪': 'es',
            '🇻🇳': 'vi', '🇾🇪': 'ar', '🇿🇲': 'en', '🇿🇼': 'en'
        }
        
        if reaction.emoji in flag_emojis:
            lang = flag_emojis[reaction.emoji]
            translated_text = await self.auto_trans(
                message=message.content,
                lang=lang
            )
            await message.channel.send(f'{reaction.emoji}: {translated_text} ')


    @commands.hybrid_command()
    async def switch_button_for_translator(self,ctx:commands.Context):
        if not await function.check_role(self=self,ctx=ctx):
            return
        
        await ctx.send(view=switch_button())

 

    async def rps_autocomplete(self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        all_languages = LANGUAGES
        
        choices = all_languages
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices if current.lower() in choice.lower()
        ][:25]

    
    @app_commands.command()
    @app_commands.autocomplete(output_lang = rps_autocomplete)
    @app_commands.describe(output_lang='Select lang code or type your lang code like en or de', texts='Type anything to translate to')
    async def translate(self, i: discord.Interaction,  output_lang:str,texts:str):
        """Translate command that allows selecting output language"""
        
        if i:
            await i.response.defer(thinking=True, ephemeral=True)

        def translate(text):
            tl = EasyGoogleTranslate(source_language='auto', target_language=output_lang)
            detect_source_lang = Translator()
            detected_source = detect_source_lang.detect(text).lang
            detected_target = detect_source_lang.detect(output_lang).lang
            translated_text = tl.translate(text)
            return translated_text, detected_source, detected_target
        
        if texts:
            translated_text, detected_source, detected_target = translate(text=texts)
            embed_created = discord.Embed(title=f'{detected_source} to {detected_target}')
            embed_created.add_field(name='Source text', value=f'{texts}', inline=False)
            embed_created.add_field(name='Translated text', value=f'{translated_text}', inline=False)

            def check_pfp():
                if i.user.avatar.url is None:
                    return 'https://static.vecteezy.com/system/resources/previews/024/983/914/original/simple-user-default-icon-free-png.png'
                else:
                    i.user.avatar.url

            check_pfp_ = check_pfp()
            embed_created.set_author(name=f'{i.user.name}', url=f'https://discord.com/users/{i.user.id}', icon_url=check_pfp_)
            await i.followup.send(embed=embed_created, ephemeral=True)

    
        
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