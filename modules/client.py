import discord
from discord.ext import commands, tasks
import os
import aiosqlite
from modules import variables,function,switch_
from command_files.translator import switch_button
from command_files.translator import embed as e
from command_files.healthy import button_sleeptimer


    
class intents:
    def call_intents():
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True
        return intents

class modguard(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or("!"), intents=intents.call_intents())
        self.embed_instance = e()
        

    async def check_old_switch(self):
        channel = self.get_channel(variables.switch_translate_ch)
        message = await channel.fetch_message(variables.default_switch_message_id)
        if message.content == '||False||':
            switch_.tracking_message = False
            
        elif message.content =='||True||':
           switch_.tracking_message = True
           
    async def update_recent_button(self):
        channel = self.get_channel(variables.switch_translate_ch)
        message = await channel.fetch_message(variables.default_switch_message_id)
        switch_color = await self.embed_instance.check_switch_and_return_color()
        switch_switch = await self.embed_instance.check_bool_return_switch()
        new_embed = discord.Embed(title='Auto Translate',color=switch_color)
        new_embed.add_field(name='Automatic translates Toggle switch',value=f'<#1260062822285709433>')
        new_embed.set_image(url=f"{switch_switch}")
        await message.edit(content=f'||{switch_.tracking_message}||',embed=new_embed,view=switch_button(superbot=self))
        switch_button(superbot=self)
        

    async def on_ready(self):
        await self.tree.sync()
        await self.check_old_switch()
        await self.update_recent_button()
        
        #await self.update_sleep_button()
        print(f'Logged in as {self.user}')
        print('coution: please use command !reset everytime you re-online bot. this is for update every button to not make it messed up')
        debugging_ch = discord.utils.get(self.get_all_channels(), name="「👾🛠」𝓓𝓮𝓫𝓾𝓰𝓰𝓲𝓷𝓰")
        if debugging_ch:
            await debugging_ch.send('hello world')

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
from keep_alive import keep_alive
run_client = modguard()
import secret_stuff
keep_alive()
keep_alive
modguard_token = modules.function.pull_variables.fetch_token()
run_client.run(reconnect=True, root_logger=False, token=secret_stuff.debug)