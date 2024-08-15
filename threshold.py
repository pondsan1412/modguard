import discord
from googletrans import Translator

bot = discord.Client(intents=discord.Intents.all())
@bot.event
async def on_ready():
    print(bot.user.name)

async def src_to_en(message: str, src: str):
        try:
            trans = Translator()
            translator = trans.translate(
                text=message,
                src=src,
                dest='en'
            )
            return translator.text
        except Exception as e:
            print(f"Translation error: {e}")
            return None
def src_to_flag(src: str) -> str:
    # แปลงตัวอักษร ISO 3166-1 alpha-2 ไปเป็นอิโมจิธงชาติ
    if len(src) != 2:
        return '🏳️'  # คืนค่าเป็นธงขาวถ้ารหัสไม่ถูกต้อง

    # แปลง src ให้เป็นตัวอักษรตัวใหญ่
    src = src.upper()

    # แปลงตัวอักษร A-Z ไปเป็นอิโมจิธงชาติ
    flag_offset = ord('🇦') - ord('A')
    return chr(ord(src[0]) + flag_offset) + chr(ord(src[1]) + flag_offset)

@bot.event
async def on_message(message:discord.Message):
    if message.author == bot.user:
        return
    if message.content.startswith('!'):
        src, _, trans = message.content[1:].partition(' ')  # ตัดจุดนำหน้าออกและแบ่ง src กับข้อความ

        if not src or not trans:  # ตรวจสอบว่าคำสั่งถูกต้อง
            await message.channel.send("Invalid command format. Please use .<language_code> <text>.")
        else:
            translated_text = await src_to_en(message=trans, src=src)
            if translated_text:
                flag = src_to_flag(src)
                embed = discord.Embed(title=f"{src} to en",color=discord.Color.yellow())
                embed.add_field(name=f"{flag}",value=f"```{trans}```",inline=False)
                embed.add_field(name=f":flag_us: ",value=f"```{translated_text}```",inline=False)
                embed.set_footer(text='google translate reverse engineering',  icon_url='https://cdn-icons-png.flaticon.com/512/281/281776.png')
                await message.channel.send(embed=embed)
            else:
                await message.channel.send("Translation failed or language not supported.")

import secret_stuff
bot.run(secret_stuff.debug)