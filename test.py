import aiohttp
import asyncio

async def lounge_api_full():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.mk8dx-lounge.com/api/player/list") as response:
            if response.status == 200:
                players_data = await response.json()
                return [player['name'] for player in players_data['players'] if 'name' in player]

async def main():
    discord_ids = await lounge_api_full()
    print(discord_ids)

if __name__ == "__main__":
    asyncio.run(main())
