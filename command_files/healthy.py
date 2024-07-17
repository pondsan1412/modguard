import discord
from discord.ext import commands, tasks
from modules.function import check_role
import datetime
from modules import function,variables as v
class healthy_commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.user_timers = {}
        self.user_messages = {}

    @commands.hybrid_command() 
    async def sleep_button(self, ctx: commands.Context):
        """This command is for admin only"""

        if not await check_role(ctx=ctx):
            return

        view = button_sleeptimer(ctx)
        message = await ctx.send(view=view, content='Press button to start your sleep \nabout sleep result will save in <#1262644348743454740>',delete_after=300)
        view.message = message
    
    @commands.hybrid_command()
    async def reset(self,ctx:commands.Context):
        """**__CAUTION__** this command is for admin only!"""
        if not await check_role(ctx=ctx):
            return
        msg_ch = v.discord_channel_network_community['debugging_channel']
        channel_sleep = ctx.guild.get_channel(1262642481414148106)
        new_button = await channel_sleep.fetch_message(1262699824864690259)
        button = button_sleeptimer(ctx=ctx)
        send_again = await new_button.edit(view=button,content=f'Press button to start your sleep \nabout sleep result will save in <#1262644348743454740>')
        button.message = send_again
        
    
    

class sleep_count:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = datetime.datetime.now().replace(microsecond=0)

    def stop(self):
        self.end_time = datetime.datetime.now().replace(microsecond=0)

    def calculate_sleep_time(self):
        if self.start_time and self.end_time:
            elapsed_time = self.end_time - self.start_time
            hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"Total sleep time: {int(hours)} hours and {int(minutes)} minutes"
        return None

class button_sleeptimer(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx 
        self.message = None
        self.update_message_task.start()

    @discord.ui.button(label='Start', style=discord.ButtonStyle.blurple)
    async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        if user_id not in self.ctx.cog.user_timers:
            self.ctx.cog.user_timers[user_id] = sleep_count()
            self.ctx.cog.user_messages[user_id] = interaction.user.mention
            print(self.ctx.cog.user_timers[user_id])

        self.ctx.cog.user_timers[user_id].start()
        await self.update_message()
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Stop', style=discord.ButtonStyle.red)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        if user_id in self.ctx.cog.user_timers:
            self.ctx.cog.user_timers[user_id].stop()
            sleep_time = self.ctx.cog.user_timers[user_id].calculate_sleep_time()
            await self.ctx.send(f"{interaction.user.mention} {sleep_time} \nthis message will remove within 5 minutes",delete_after=300)
            thread = self.ctx.bot.get_channel(1262644348743454740)
            current_date = datetime.datetime.now()
            formatted_date = current_date.strftime("%d %B %Y")
            embed = discord.Embed(title=f'{interaction.user.name}\'s result (sleep)')
            embed.add_field(name=' ',value=f'{sleep_time}\n history date: {formatted_date}')
            await thread.send(embed=embed)
            del self.ctx.cog.user_timers[user_id]
            del self.ctx.cog.user_messages[user_id]

        await self.update_message()
        await interaction.response.edit_message(view=self)

    @tasks.loop(minutes=1)
    async def update_message_task(self):
        await self.update_message()

    async def update_message(self):
        if not self.message:
            return

        content = []
        for user_id, sleep_timer in self.ctx.cog.user_timers.items():
            elapsed_time = datetime.datetime.now().replace(microsecond=0) - sleep_timer.start_time
            hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            content.append(f"{self.ctx.cog.user_messages[user_id]} is sleeping, duration: {int(hours)} hours and {int(minutes)} minutes")
        
        if content:
            await self.message.edit(content='\n'.join(content))
        else:
            await self.message.edit(content='Press button to start your sleep \nabout sleep result will save in <#1262644348743454740>')

    @update_message_task.before_loop
    async def before_update_message_task(self):
        await self.ctx.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(healthy_commands(bot))
