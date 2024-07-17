import discord
from discord import app_commands
from discord.ext import commands
from typing import List
from modules.function import fetch_player_stats_short as fetch_stats
import aiohttp

class mk8dx(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    async def player_load(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.mk8dx-lounge.com/api/player/list") as response:
                if response.status == 200:
                    players_data = await response.json()
                    player_names = [player['name'] for player in players_data['players']]
                    filtered_names = [name for name in player_names if current.lower() in name.lower()]
                    return [app_commands.Choice(name=name, value=name) for name in filtered_names][:25]
                else:
                    # Handle API error response
                    return []
                
    async def player_load_full(self,discord_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://www.mk8dx-lounge.com/api/player?discordId={discord_id}') as response:
                if response.status == 200:
                    player_load = await response.json()
                    registryid = player_load.get('registryId')
                    countrycode = player_load.get('countryCode')
                    switchfc = player_load.get('switchFc')
                    mmr = player_load.get('mmr')
                    maxmmr = player_load.get('maxMmr')
                    return registryid,countrycode,switchfc,mmr,maxmmr
                
    @app_commands.command()
    @app_commands.describe(player="input player's mk8dx lounge name")
    @app_commands.autocomplete(player=player_load)
    async def stats(self, interaction: discord.Interaction, player: str = None):
        await interaction.response.defer(thinking=True)

        if interaction:
            nameplayer,discord_id,mkcId,mmr,eventsplayed = await fetch_stats(nameplayer=player)
            registryid,countrycode,switchfc,mmr,maxmmr = await self.player_load_full(discord_id=discord_id)

            def check_mmr() -> tuple[str, discord.Colour]:
                if nameplayer == player:
                    if mmr < 2999:
                        check_noob = 'NOOB'
                        color = None
                    elif mmr < 4000:
                        check_noob = 'seems good'
                        color = None
                    elif mmr < 5000:
                        check_noob = 'great player'
                        color = discord.Colour.green()
                    else:
                        check_noob = 'strong player!'
                        color = discord.Colour.red()
                else:
                    check_noob = 'Player not found'
                    color = None

                return check_noob, color


                
                

            check_player = check_mmr()
            check_noob, color = check_player
            fetch_user = await self.bot.fetch_user(discord_id)
            
            embed = discord.Embed(title=f'{fetch_user.global_name} is {check_noob} confirm!', color=color)
            embed.add_field(
                name=f'{player} is from {countrycode}!',
                value=f"""

[player's mario kart central profile:](https://www.mariokartcentral.com/mkc/registry/players/{registryid})

current mmr: __{mmr}__
Max MMR: __{maxmmr}__ 
switch_fc: __{switchfc}__

"""
            )
            
            embed.set_author(name=f'{player}', url=f'https://discord.com/users/{discord_id}',icon_url=fetch_user.avatar.url)
            await interaction.followup.send(embed=embed)
    
async def setup(bot):
    await bot.add_cog(mk8dx(bot))