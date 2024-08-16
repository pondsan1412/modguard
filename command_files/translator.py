import discord
from discord.ext import commands
from discord import app_commands
import deepl
import discord.utils
from modules import function ,variables as v,switch_ as s
from typing import List
import secret_stuff
from googletrans import Translator
trans = deepl.Translator(auth_key=secret_stuff.api_keys)

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
        result = trans.translate_text(
            text=msg.content,
            source_lang='auto',
            target_lang='en-us'
        )

        await i.response.send_message(result.text)

    async def translator(self, message: str) -> str:
        
        translated = trans.translate_text(
            text=message,
            source_lang='auto',
            target_lang='en-us'
        )
        return translated.text
    
    #new function translator
    async def trans(self,message:str) -> str:
       
        translated = trans.translate_text(
            text=message,
            target_lang='en-us',
            source_lang='auto'
        )
        return translated.text

    # ตรวจจับภาษาต้นทางแบบออโต้ และแปลภาษาออกไปตามที่รับค่ามาจาก emoji
    async def auto_trans(self, message: str, lang: str):
        translator = trans.translate_text(
            text=message,
            source_lang='auto',
            target_lang=lang
        )
        return translator.text
    
    #ต้นทางภาษาไปสู่ english
    async def src_to_en(self, message: str, src: str):
        try:
            translator = trans.translate_text(
                text=message,
                source_lang=src,
                target_lang='en-us'
            )
            return translator.text
        except Exception as e:
            print(f"Translation error: {e}")
            return None
        
    async def handle_translation(self, message):
        if message.content.startswith('.'):
            src, _, trans = message.content[1:].partition(' ')  # ตัดจุดนำหน้าออกและแบ่ง src กับข้อความ

            if not src or not trans:  # ตรวจสอบว่าคำสั่งถูกต้อง
                await message.channel.send("Invalid command format. Please use .<language_code> <text>.")
            else:
                translated_text = await self.src_to_en(message=trans, src=src)
                if translated_text:
                    await message.channel.send(translated_text)
                else:
                    await message.channel.send("Translation failed or language not supported.")
    async def embed_trans(self, message:discord.Message):
        if message.content.startswith('!'):
            src, _, trans = message.content[1:].partition(' ')  # ตัดจุดนำหน้าออกและแบ่ง src กับข้อความ

            if not src or not trans:  # ตรวจสอบว่าคำสั่งถูกต้อง
                await message.channel.send("Invalid command format. Please use .<language_code> <text>.")
            else:
                translated_text = await self.src_to_en(message=trans, src=src)
                if translated_text:
                    flag = self.src_to_flag(src)
                    embed = discord.Embed(title=f"{src} to en",color=discord.Color.yellow())
                    embed.add_field(name=f"{flag}",value=f"```{trans}```",inline=False)
                    embed.add_field(name=f":flag_us: ",value=f"```{translated_text}```",inline=False)
                    embed.set_footer(text='google translate reverse engineering',  icon_url='https://cdn-icons-png.flaticon.com/512/281/281776.png')
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send("Translation failed or language not supported.")
    @commands.Cog.listener()
    async def on_message(self,message:discord.Message):
        if message.author == self.bot.user: return
        
        def detect_lang(message_content:str)->str:
            detect = Translator()
            lang_detected = detect.detect(message_content).lang
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
                 #เรียกใช้ฟังชั่น handle message
                await self.handle_translation(message)
                await self.embed_trans(message)
                #embed
                
                if not detect_lang(message.content):
                    return
                
                # ลบอีโมจิที่อยู่ในรูปแบบ :emoji_name: หรือ :number: หรือ <:number>
                match True:
                    case _ if message.content.startswith("!"):return
                    case _ if message.content.startswith("."):return
                

                translated = await self.trans(message=message.content)
                extracted, remaining = function.message.extract_message(message=translated)
                print(extracted,remaining, translated)
                
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
            translated_text = await self.src_to_en(
                message=message.content,
                src=lang
            )
            await message.channel.send(f'{reaction.emoji}: {translated_text} ')

    def src_to_flag(self, src: str) -> str:
        # แปลงตัวอักษร ISO 3166-1 alpha-2 ไปเป็นอิโมจิธงชาติ
        if len(src) != 2:
            return '🏳️'  # คืนค่าเป็นธงขาวถ้ารหัสไม่ถูกต้อง

        # แปลง src ให้เป็นตัวอักษรตัวใหญ่
        src = src.upper()

        # แปลงตัวอักษร A-Z ไปเป็นอิโมจิธงชาติ
        flag_offset = ord('🇦') - ord('A')
        return chr(ord(src[0]) + flag_offset) + chr(ord(src[1]) + flag_offset)
    
    @commands.hybrid_command()
    async def switch_button_for_translator(self,ctx:commands.Context):
        if not await function.check_role(ctx=ctx):
            return
        
        await ctx.send(view=switch_button(superbot=self.bot))

   
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