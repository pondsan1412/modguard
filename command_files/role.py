import discord
from discord.ext import commands
from modules.variables import reactions_roles
from modules import function,variables

class ReactionRole(commands.Cog):
    def __init__(self, bot: commands.Bot,message_id=0):
        self.bot = bot
        self.message_id = message_id
        
    @commands.hybrid_command()
    async def add_single_emoji(self, ctx:commands.Context,message_id:int, *,which_emoji:str ):
        role_guild = discord.utils.get(ctx.guild.roles, name="Admin")
        if role_guild is None or role_guild not in ctx.author.roles:
            return
        
        message = await ctx.fetch_message(message_id)
        await message.add_reaction(which_emoji)

    @commands.hybrid_command()
    async def set_emoji(self, ctx: commands.Context, message_id: int):
        """
        Setup reaction roles for a specific message.
        Example usage: !emoji 1234567890
        """
        role_guild = discord.utils.get(ctx.guild.roles, name='Admin')
        if role_guild is None or role_guild not in ctx.author.roles:
            return

        try:
            message = await ctx.fetch_message(message_id)
        except discord.NotFound:
            await ctx.send("Message not found. Please provide a valid message ID.")
            return

        for emoji, role_name in reactions_roles.items():
            role = discord.utils.get(ctx.guild.roles, name=role_name)

            if role is None:
                try:
                    role = await ctx.guild.create_role(name=role_name, reason=None)
                except discord.HTTPException:
                    continue

            try:
                await message.add_reaction(emoji)
                self.message_id = message_id  # Set message_id for this cog instance
            except discord.HTTPException:
                continue
            
        await ctx.send("Reaction roles setup complete.")


    async def check_channel(self, payload: discord.RawReactionActionEvent) -> bool:
        reaction_channel_id = function.role_class.callback_integer_from_dic(variables.discord_channel_network_community['reques_role'])
        if payload.channel_id != reaction_channel_id:
            return False
        
        return True
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if not await self.check_channel(payload):
            return
        
        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return
        
        emoji = str(payload.emoji)
        role_name = reactions_roles.get(emoji)
        
        if role_name is None:
            return
        
        role = discord.utils.get(guild.roles, name=role_name)
        if role is None:
            try:
                role = await guild.create_role(name=role_name, reason="Reaction role setup")
                print(f"Created role: {role_name}")
            except discord.HTTPException as e:
                print(f"Failed to create role: {e}")
                return
        
        member = guild.get_member(payload.user_id)
        if member is None:
            try:
                member = await guild.fetch_member(payload.user_id)
            except discord.HTTPException as e:
                print(f"Failed to fetch member: {e}")
                return
        
        
        try:
            await member.add_roles(role)
            print(f"Added role {role.name} to {member.display_name}")
        except discord.HTTPException as e:
            print(f"Failed to add role {role.name} to {member.display_name}: {e}")

    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if not await self.check_channel(payload):
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return

        emoji = str(payload.emoji)
        role_name = reactions_roles.get(emoji)

        if role_name is None:
            return

        role = discord.utils.get(guild.roles, name=role_name)
        if role is None:
            return

        member = guild.get_member(payload.user_id)
        if member is None:
            try:
                member = await guild.fetch_member(payload.user_id)
            except discord.HTTPException as e:
                print(f"Failed to fetch member: {e}")
                return

        
        try:
            await member.remove_roles(role)
            print(f"Removed role {role.name} from {member.name}")
        except discord.HTTPException as e:
            print(f"Failed to remove role {role.name} from {member.name}: {e}")

async def setup(bot):
    await bot.add_cog(ReactionRole(bot))