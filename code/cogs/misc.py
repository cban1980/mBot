import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import os
from dotenv import load_dotenv
import platform

class misc(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    # Function that will return host system information and system load as a nextcord.Embed object, to be used in the /sysinfo slash command.
    @nextcord.slash_command(name="sysinfo", description="Shows host system information.")
    async def sysinfo(self, ctx: nextcord.Interaction):
        # Get system information
        uname = platform.uname()
        # Get system load
        load = os.getloadavg()
        # Create an embed with the system information and system load
        embed = nextcord.Embed(title="System Information", color=0x00ff00)
        embed.add_field(name="System: ", value=uname.system, inline=False)
        embed.add_field(name="Node Name: ", value=uname.node, inline=False)
        embed.add_field(name="Release: ", value=uname.release, inline=False)
        embed.add_field(name="Version: ", value=uname.version, inline=False)
        embed.add_field(name="Machine: ", value=uname.machine, inline=False)
        embed.add_field(name="Processor: ", value=uname.processor, inline=False)
        embed.add_field(name="System Load: ", value=load, inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(misc(bot))