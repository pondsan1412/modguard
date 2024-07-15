import random
from discord.ext import commands
import secret_stuff
from modules import switch_,variables
import re
import discord

def check_string(variable):
    if isinstance(variable, str):
        return True
    else:
        return False
    
class pull_variables():
    def __init__(self,token:str):
        self.token = token

    def fetch_token()-> str:
        return secret_stuff.token
    
    def fetch_boolean(bool)-> bool:
        return bool

class role_class:
    def __init__(self):
        pass
    
    def callback_integer_from_dic(integer)-> int:
        return integer
    
class switch_button:
    def __init__(self):
        pass

    def switch_tracking_translator(button)->bool:
        switch_.tracking_message
        if button=='on' and switch_.tracking_message != True:
            switch_.tracking_message = True
            return switch_.tracking_message
        elif button=='off' and switch_.tracking_message != False:
            switch_.tracking_message = False
            return switch_.tracking_message

    def check_switch()->bool:
        return switch_.tracking_message
    
    def switch_return_string()->str:
        if switch_.tracking_message == True:
            return "ON"
        else:
            return "Off"
def convert_boolean(text)->bool:
    if isinstance(text,str):
        return True
    else:
        return False

class message():
    @staticmethod
    def extract_message(message):
        try:
            pattern = r'<@(\d+)>'
            match = re.search(pattern, message)
            if match:
                extracted_value = match.group(0)
                remaining_message = re.sub(pattern, '', message)
                return extracted_value, remaining_message
            else:
                return message, ''  # คืนค่าเป็นข้อความทั้งหมดและสตริงว่างเพื่อความถูกต้อง
        except TypeError as e:
            print(e)

    @staticmethod
    def extract_custom_emoji(message):
        try:
            pattern = r'<:(\w+):(\d+)>'
            match = re.search(pattern, message)
            if match:
                emoji_name = match.group(1)
                emoji_id = match.group(2)
                extracted_value = f'<:{emoji_name}:{emoji_id}>'
                remaining_message = re.sub(pattern, '', message)
                return extracted_value, remaining_message.strip()
            else:
                return None, message
        except TypeError as e:
            pass



async def check_channel(self, payload: discord.RawReactionActionEvent) -> bool:
    reaction_channel_id = role_class.callback_integer_from_dic(variables.discord_channel_network_community['reques_role'])
    if payload.channel_id != reaction_channel_id:
        return False
    return True

async def check_role(ctx):
    role_guild = discord.utils.get(ctx.guild.roles, name="Admin")
    if role_guild is None or role_guild not in ctx.author.roles:
        await ctx.reply(f'You do not have permission: {ctx.author.id}')
        return False
    return True