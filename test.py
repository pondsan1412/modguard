import aiohttp
import asyncio

async def fetch_player_stats_short(nameplayer):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.mk8dx-lounge.com/api/player/list") as response:
            if response.status == 200:
                players_stats = await response.json()
                for player in players_stats['players']:
                    if 'name' in player and nameplayer.lower() in player['name'].lower():
                        discord_id = player.get('discordId')
                        mkcId = player.get('mkcId')
                        mmr = player.get('mmr')
                        eventsplayed = player.get('eventsPlayed')
                        print( nameplayer,discord_id,mkcId,mmr,eventsplayed)

asyncio.run(fetch_player_stats_short(nameplayer='nissan'))