import discord
from discord.ext import commands
import aiohttp

class Admin_(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def check_role(self, ctx: commands.Context):
        role_guild = discord.utils.get(ctx.guild.roles, name="Admin")
        if role_guild is None or role_guild not in ctx.author.roles:
            await ctx.reply(f'You do not have permission: {ctx.author.id}')
            return False
        return True

    async def fetch_avatar_file(self, url, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    await ctx.send('Failed to fetch image')
                    return None
                image_bytes = await response.read()
                return image_bytes
            
    async def console_log(self,ctx:commands.Context):
        await ctx.send(content=f'successful with command: `{ctx.command.name}`')

    @commands.hybrid_command()
    async def set_pfp(self, ctx: commands.Context, url: str):
        """edit bot's pfp by placing URL """
        if not await self.check_role(ctx):
            return
        image_bytes = await self.fetch_avatar_file(url, ctx)
        if image_bytes is None:
            return
        try:
            await self.bot.user.edit(avatar=image_bytes)
            if not await self.console_log(ctx):return
        except discord.HTTPException as e:
            await ctx.send(f"Failed to update profile picture: {e}")

    @commands.hybrid_command()
    async def client_tracking_user_pfp(self, ctx: commands.Context, user: discord.User):
        """steal user pfp by discord_id, mentioned, username"""
        if not await self.check_role(ctx):
            return
        steal_user_pfp = await self.fetch_avatar_file(url=user.avatar.url,ctx=ctx)
        if steal_user_pfp:
            await self.bot.user.edit(avatar=steal_user_pfp)
            if not await self.console_log(ctx):
                return
        else:
            None

    


async def setup(bot: commands.Bot):
    await bot.add_cog(Admin_(bot))
