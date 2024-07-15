import aiohttp
import asyncio

async def find_player_names():
    url = 'https://www.mk8dx-lounge.com/api/player/list'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                player_data = await response.json()
                for player in player_data['players']:
                    if player['name'] == 'Sky_2k':
                        print(player['discordId'])
                        
asyncio.run(find_player_names())
