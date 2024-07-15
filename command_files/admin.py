import discord
from discord.ext import commands
import aiohttp
from modules import variables as v
import requests
import base64
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
    async def steal_pfp(self,ctx:commands.Context,user:discord.User):
        if not await self.check_role(ctx=ctx):return
        steal = user.avatar.url
        await ctx.send(content=f'{steal}')

    
    @commands.hybrid_command()
    async def pfp_mk(self,ctx:commands.Context,player:str=None):
        """steal player's pfp from mk8dx lounge"""
        def fetch_player_data(player_name):
            url = v.mk8dx_api_url_name + player_name
            respone = requests.get(url)
            if respone.status_code == 200:
                player_data = respone.json()
                player_data["discordId"]
                return player_data["discordId"]
            
        mk9dx = fetch_player_data(player_name=player)
        dc_pfp = await self.bot.fetch_user(mk9dx)
        embed_god = discord.Embed(title=f' ')
        embed_god.add_field(name=' ',value=f'{dc_pfp.name}\n id:{dc_pfp.id}')
        embed_god.set_image(url=f'{dc_pfp.avatar.url}')
        
        
        await ctx.send(embed=embed_god,view=steal_users_pfp_and_change_self_pfp(pfp_url=dc_pfp.avatar.url,bot=self.bot,name=dc_pfp.name))

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
class steal_users_pfp_and_change_self_pfp(discord.ui.View):
    def __init__(self,pfp_url,bot,name):
        super().__init__(timeout=60)
        self.user_pfp = pfp_url
        self.bot = bot
        self.name = name
    async def console_log(self,ctx:discord.Interaction,username):
        await ctx.response.send_message(f'seccessful bot change pfp by stealing {username}')

    @discord.ui.button(label='edit_bot_pfp',style=discord.ButtonStyle.gray)
    async def edit_pfp(self,ctx:discord.Interaction,button:discord.Button):
        av = Admin_(self.bot)
    
        steal_user_pfp = await av.fetch_avatar_file(url=self.user_pfp,ctx=ctx)
        if steal_user_pfp:
            await self.bot.user.edit(avatar=steal_user_pfp)
            if not await self.console_log(ctx=ctx,username=self.name):
                return
        else:
            None
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Admin_(bot))
