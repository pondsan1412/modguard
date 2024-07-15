from modules import variables as v
import requests
import json

def fetch_player_data(player_name):
    url = v.mk8dx_api_url_name + player_name
    respone = requests.get(url)
    if respone.status_code == 200:
        player_data = respone.json()
        player_data["discordId"]
        return player_data["discordId"]
    
print(fetch_player_data(player_name='nissan'))