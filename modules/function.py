import random
import discord
from discord.ext import commands
import secret_stuff
import variables 
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