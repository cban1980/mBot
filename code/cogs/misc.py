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
  
def setup(bot):
    bot.add_cog(misc(bot))