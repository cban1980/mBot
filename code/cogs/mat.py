import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import os

list_guild_ids = os.getenv("GUILD_ID").split(",")
list_guild_ids = [int(id) for id in list_guild_ids]

class MatCog(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @nextcord.slash_command(name="resturanger", description="Lista av resturanger i Mjärdevi", guild_ids=list_guild_ids)
    async def resturanger(self, ctx: nextcord.Interaction):
        restaurants = ["Restaurant 1", "Restaurant 2", "Restaurant 3"]
        restaurant_list = "\n".join([f"• {r}" for r in restaurants])
        await ctx.send(f"Here are the restaurants in Mjärdevi, Linköping:\n{restaurant_list}")

def setup(bot):
    bot.add_cog(MatCog(bot))