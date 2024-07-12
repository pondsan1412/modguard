import discord
from discord.ext import commands, tasks
import os
import aiosqlite

# call intents
def call_intents():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.presences = True
    return intents

async def get_prefix(bot, message):
    async with aiosqlite.connect('prefixes.db') as db:
        async with db.execute('SELECT prefix FROM prefixes WHERE guild_id = ?', (message.guild.id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else '!'

class modguard(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=get_prefix, intents=call_intents())

    async def on_ready(self):
        await self.tree.sync()
        async with aiosqlite.connect('prefixes.db') as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS prefixes (
                    guild_id INTEGER PRIMARY KEY,
                    prefix TEXT NOT NULL
                )
            ''')
            await db.commit()
        self.check_prefix_channels.start()
        print(f'Logged in as {self.user}')
        debugging_ch = discord.utils.get(self.get_all_channels(), name="「👾🛠」𝓓𝓮𝓫𝓾𝓰𝓰𝓲𝓷𝓰")
        if debugging_ch:
            await debugging_ch.send('hello world')

    @tasks.loop(minutes=1)
    async def check_prefix_channels(self):
        for guild in self.guilds:
            await self.check_prefix_channel_for_guild(guild)

    async def check_prefix_channel_for_guild(self, guild):
        channel = discord.utils.get(guild.text_channels, name='prefix_ch')
        if channel:
            async for message in channel.history(limit=1):
                new_prefix = message.content.strip()
                async with aiosqlite.connect('prefixes.db') as db:
                    await db.execute('REPLACE INTO prefixes (guild_id, prefix) VALUES (?, ?)', (guild.id, new_prefix))
                    await db.commit()
                print(f'Updated prefix for {guild.name} to {new_prefix}')

    async def on_guild_join(self, guild):
        await self.check_prefix_channel_for_guild(guild)

    async def setup_hook(self):
        self.remove_command('help')
        cog_folder = "command_files"
        for filename in os.listdir(cog_folder):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = f"{cog_folder}.{filename[:-3]}"
                try:
                    await self.load_extension(module_name)
                    print(f"Loaded extension: {module_name}")
                except Exception as e:
                    print(f"Failed to load extension {module_name}: {e}")

import modules.function
run_client = modguard()
modguard_token = modules.function.pull_variables.fetch_token()
run_client.run(reconnect=True, root_logger=False, token=modguard_token)
