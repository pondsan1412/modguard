import discord
from discord.ext import commands
from modules import function as f
import datetime

class count_sleep_time:
    def __init__(self):
        self.sleep_times = {}

    def start_sleep(self, user_id):
        start_time = datetime.datetime.now().replace(microsecond=0)
        self.sleep_times[user_id] = {'start_time': start_time, 'end_time': None}
        print(f"User {user_id} sleep started at {self.sleep_times[user_id]['start_time']}")

    def end_sleep(self, user_id):
        if user_id in self.sleep_times and self.sleep_times[user_id]['start_time'] is not None:
            end_time = datetime.datetime.now().replace(microsecond=0)
            self.sleep_times[user_id]['end_time'] = end_time
            print(f"User {user_id} sleep ended at {self.sleep_times[user_id]['end_time']}")

    def get_sleep_duration(self, user_id):
        if user_id in self.sleep_times:
            start_time = self.sleep_times[user_id]['start_time']
            end_time = self.sleep_times[user_id]['end_time']
            if start_time and end_time:
                return end_time - start_time
        return None

    def reset_sleep(self, user_id):
        if user_id in self.sleep_times:
            self.sleep_times[user_id] = {'start_time': None, 'end_time': None}

class healthy_context(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.sleep_tracker = count_sleep_time()

    @commands.hybrid_command()
    async def healthy_button(self, ctx: commands.Context):
        """for admin"""
        if not await f.check_role(ctx=ctx):
            return
        view = healthy_button(self.sleep_tracker)
        await ctx.send("Press the button to start or stop sleep tracking.", view=view)

class healthy_button(discord.ui.View):
    def __init__(self, sleep_tracker):
        super().__init__(timeout=None)
        self.sleep_tracker = sleep_tracker
        self.message = None
        self.start_button = None
        self.stop_button = None

    async def update_message(self, user_id):
        while user_id in self.sleep_tracker.sleep_times and not self.sleep_tracker.sleep_times[user_id]['end_time']:
            duration = datetime.datetime.now().replace(microsecond=0) - self.sleep_tracker.sleep_times[user_id]['start_time']
            if self.message:
                await self.message.edit(content=f"Sleep tracking for <@{user_id}>: {duration}")
            await discord.utils.sleep_until(datetime.datetime.now() + datetime.timedelta(minutes=0.05))

    @discord.ui.button(label='Start', style=discord.ButtonStyle.blurple)
    async def start(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        self.sleep_tracker.start_sleep(user_id)
        start_time = datetime.datetime.now().replace(microsecond=0)
        await interaction.response.send_message(f"Sleep tracking started for <@{user_id}> at {start_time}.")
        self.message = await interaction.original_response()
        await self.update_message(user_id=user_id)
        if self.stop_button:
            self.stop_button.disabled = False
        if self.start_button:
            self.start_button.disabled = True

    @discord.ui.button(label='Stop', style=discord.ButtonStyle.gray)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        user_id = interaction.user.id
        self.sleep_tracker.end_sleep(user_id)
        duration = self.sleep_tracker.get_sleep_duration(user_id)
        if duration:
            await self.message.edit(content=f"Sleep tracking stopped for <@{user_id}>. Duration: {duration}.")
        else:
            await interaction.response.send_message(f"Sleep tracking has not started for <@{user_id}>.", ephemeral=True)
        if self.start_button:
            self.start_button.disabled = False
        if self.stop_button:
            self.stop_button.disabled = True

async def setup(bot):
    await bot.add_cog(healthy_context(bot))
