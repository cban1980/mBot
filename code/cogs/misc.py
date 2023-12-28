#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Class for miscellaneous functions called in mBot.py

import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import os
from dotenv import load_dotenv
import platform

load_dotenv()
list_guild_ids = os.getenv("GUILD_ID")

class misc(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
# Function that will return host system information and system load as a nextcord.Embed object, to be used in the /sysinfo slash command.
@nextcord.slash_command(name="sysinfo", description="Shows host system information.", guild_ids=[list_guild_ids])
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

# Function that returns what slash commands the bot has registered.
@nextcord.slash_command(name="show_commands", description="Shows registered slash commands.", guild_ids=[list_guild_ids])
async def show_commands(self, ctx: nextcord.Interaction):
    # Get the slash commands registered to the bot
    commands = bot.slash_commands
    # Create an embed with the slash commands
    embed = nextcord.Embed(title="Slash Commands", color=0x00ff00)
    for command in commands:
        embed.add_field(name=command.name, value=command.description, inline=False)
    await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(misc(bot))