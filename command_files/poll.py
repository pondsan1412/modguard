import discord
from discord.ext import commands

class Poll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command()
    async def poll(self, ctx: commands.Context, question, *choices: str):
        if len(choices) > 10:
            await ctx.send("ตัวเลือกต้องไม่เกิน 10 ตัวเลือก")
            return
        
        emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        
        embed = discord.Embed(title="โปรดโหวต", description=question, color=discord.Color.blue())
        
        for i in range(len(choices)):
            embed.add_field(name=f"{emojis[i]} {choices[i]}", value="\u200b", inline=False)
        
        message = await ctx.send(embed=embed)
        
        for i in range(len(choices)):
            await message.add_reaction(emojis[i])
        
        def check(reaction, user):
            return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in emojis[:len(choices)]
        
        while True:
            reaction, user = await self.bot.wait_for('reaction_add', check=check)
            if reaction.count >= 3:
                winner_index = emojis.index(str(reaction.emoji))
                await ctx.send(f"ตัวเลือก `{choices[winner_index]}` ชนะ!")
                break

async def setup(bot):
    await bot.add_cog(Poll(bot))
