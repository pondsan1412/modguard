import discord
from discord.ext import commands
import shlex

def to_keycap(c):
    return str(c) + '\u20e3'  # แปลงตัวเลขเป็น Unicode keycap

class Poll(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.poll_message = None  # เก็บข้อความของ poll ที่สร้างไว้เพื่อให้สามารถแก้ไขได้

    @commands.command()
    async def poll(self, ctx, *, questions_and_choices: str):
        """
        Create a quick poll with delimited questions and choices.
        """
        # ตรวจสอบ delimiter ของคำถามและตัวเลือก
        if "|" in questions_and_choices:
            delimiter = "|"
        elif "," in questions_and_choices:
            delimiter = ","
        else:
            delimiter = None
        
        # แยกคำถามและตัวเลือกออกจากกัน
        if delimiter is not None:
            questions_and_choices = questions_and_choices.split(delimiter)
        else:
            questions_and_choices = shlex.split(questions_and_choices)

        # ตรวจสอบจำนวนข้อความที่ถูกแบ่งออกมา
        if len(questions_and_choices) < 3:
            return await ctx.send('Need at least 1 question with 2 choices.')
        elif len(questions_and_choices) > 11:
            return await ctx.send('You can only have up to 10 choices.')

        # ตรวจสอบสิทธิ์การใช้งานของบอท
        perms = ctx.channel.permissions_for(ctx.guild.me)
        if not (perms.read_message_history or perms.add_reactions):
            return await ctx.send('Need Read Message History and Add Reactions permissions.')

        # แยกคำถามและตัวเลือก
        question = questions_and_choices[0]
        choices = [(to_keycap(e), v)
                   for e, v in enumerate(questions_and_choices[1:], 1)]

        try:
            await ctx.message.delete()
        except:
            pass

        # สร้างข้อความ poll
        fmt = '{0} asks: {1}\n\n{2}'
        answer = '\n'.join('%s: %s' % t for t in choices)
        poll = await ctx.send(fmt.format(ctx.message.author, question.replace("@", "@\u200b"), answer.replace("@", "@\u200b")))

        # เพิ่ม emoji ตัวเลขเป็นตัวเลือกใน poll
        for emoji, _ in choices:
            await poll.add_reaction(emoji)

        # เก็บข้อความ poll ที่สร้างไว้ในตัวแปร self.poll_message เพื่อให้สามารถใช้ใน on_raw_reaction_add
        self.poll_message = poll

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if not self.poll_message:
            return
        
        # ตรวจสอบว่า reaction เกี่ยวข้องกับ poll_message ที่สร้างไว้หรือไม่
        if payload.message_id != self.poll_message.id:
            return
        
        # นับจำนวน reactions ทั้งหมดบน poll_message
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction_count = sum([reaction.count for reaction in message.reactions])

        # ถ้ามีการโหวตอย่างน้อย 3 ครั้ง
        if reaction_count >= 3:
            # หาตัวเลือกที่มี reactions มากที่สุด
            max_reactions = max(message.reactions, key=lambda r: r.count)
            winning_option = max_reactions.emoji  # ตัวเลือกที่ชนะ

            # แก้ไข embed ของ poll_message เพื่อแสดงผลผู้ชนะ
            
            await message.edit(content=f"Vote result: {winning_option} is the winner!")
            

async def setup(bot):
   await bot.add_cog(Poll(bot))
