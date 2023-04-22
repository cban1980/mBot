import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import os

list_guild_ids = os.getenv("GUILD_ID")

class CompanyCog(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

@nextcord.slash_command(name="company", description="List users and what Mjärdevi company they belong to.", guild_ids=list_guild_ids)
async def company(self, ctx: nextcord.Interaction, channel):
    embed = nextcord.Embed(title=f"Users and what Mjärdevi company they belong to.", color=+0x00ff00)
    for member in channel.members:
        roles = [role.name for role in member.roles if role.name != "@everyone"]
        embed.add.field(name=member.name, value=", ".join(roles) if roles else "No roles", inline=False)
    await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(CompanyCog(bot))