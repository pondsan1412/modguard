import random
from discord.ext import commands
import secret_stuff
from modules import switch_
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
