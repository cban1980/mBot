import os
from nextcord import Intents
import nextcord
from nextcord.ext import commands
import logging
from dotenv import load_dotenv
import random
import requests
from bs4 import BeautifulSoup as bs
import os


# Set up basic logging.

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Set variable for config directory. which will be used for loading admin list and other configs.
# will be located in the same directory as the mBot.py file.


intents = nextcord.Intents.default()
intents.message_content = True
intents.typing = True
intents.presences = True
bot = commands.Bot(command_prefix='!', intents=intents)
script_dir = os.path.dirname(os.path.abspath(__file__))

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

initial_extensions = []
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        print(f'Loaded Cog: {filename[:-3]}')
        bot.load_extension(f'cogs.{filename[:-3]}')

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

# Bofh function to use for Bot activity upon login.
def bofh():
    """Return random bofh quote"""
    url_data = requests.get('http://pages.cs.wisc.edu/~ballard/bofh/excuses').text
    soup = bs(url_data, 'html.parser')
    for line in soup:
        soppa = line.splitlines()
        soppa = random.choice(soppa)
    return soppa

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    print("Registered slash commands:")
    await bot.change_presence(activity=nextcord.Game(name=bofh()))

# Some bot commands for handling loading and unloading of cogs.
# These commands are pretty much self explainatory.


class mBot(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    
    # list of bot admins by user id read from .admins file, this is read from the config/.admins file
    def get_admins(self):
        admins = []
        admins_file_path = os.path.join(self.script_dir, "..", "config", ".admins")
        with open(admins_file_path, "r") as f:
            for line in f:
                admins.append(int(line.strip()))
        return admins
        
    # checks if user is admin by comparing user id to list of admins
    def is_admin(self, user):
        if user.id in self.get_admins():
            return True
        else:
            return False

    @bot.slash_command(name="admin_list", description="👑Current mBot admins👑")
    async def admin_list(interaction: nextcord.Interaction):
        admins = mBot.get_admins()
        embed = nextcord.Embed(title="👑Current mBot admins👑", description=" ", color=nextcord.Color.green())
        for admin in admins:
            user = await bot.fetch_user(admin)
            embed.add_field(name=" ", value=f"{user.name.strip('{}')}", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def cog_check(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("You lack permissions for this command.")
            return False
        return True

    @bot.slash_command(description="Load cog.")
    async def loadcog(ctx, extension):
        try:
            bot.load_extension(f"cogs.{extension}")
            await ctx.send(f"⚙️ Loaded extension: {extension} ✅")
        except commands.ExtensionNotLoaded:
            await ctx.send(f"⚙️ Extension {extension} was not loaded. ❌")
        except commands.ExtensionNotFound:
            await ctx.send(f"⚙️ Extension {extension} was not found. ❌")
        except Exception as e:
            await ctx.send(f"⚙️ An error occurred while unloading extension {extension}: {e} ❌")

    @bot.slash_command(description="Unload cog.")
    async def unloadcog(ctx, extension):
        try:
            bot.unload_extension(f"cogs.{extension}")
            await ctx.send(f"⚙️ Unloaded extension: {extension} ✅")
        except commands.ExtensionNotLoaded:
            await ctx.send(f"⚙️ Extension {extension} was not loaded. ❌")
        except commands.ExtensionNotFound:
            await ctx.send(f"⚙️ Extension {extension} was not found. ❌")
        except Exception as e:
            await ctx.send(f"⚙️ An error occurred while unloading extension {extension}: {e} ❌")

    @bot.slash_command(description="Reload cogs.")
    async def reloadcogs(ctx, extension):
        try:
            bot.reload_extension(f"cogs.{extension}")
            await ctx.send(f"⚙️ Reloaded extension: {extension} ✅")
        except commands.ExtensionNotLoaded:
            await ctx.send(f"-⚙️ Extension {extension} was not loaded. ❌")
        except commands.ExtensionNotFound:
            await ctx.send(f"⚙️ Extension {extension} was not found. ❌")
        except Exception as e:
            await ctx.send(f"⚙️ An error occurred while unloading extension {extension}: {e} ❌")
    
    @bot.slash_command(name="listcogs", description="List currently loaded cogs.")
    async def listcogs(interaction: nextcord.Interaction):
        loaded_cogs = ", ".join(bot.extensions.keys())
        await interaction.send(f"⚙️ Loaded cogs: {loaded_cogs} ⚙️")

bot.run(TOKEN)
