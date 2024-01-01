import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import os

class admin(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # list of bot admins by user id read from .admins file, this is read from the config/.admins file
    def get_admins(self):
        admins = []
        admins_file_path = os.path.join(self.script_dir, "/config/.admins")
        with open("admins_file_path", "r") as f:
            for line in f:
                admins.append(int(line.strip()))
        return admins
        return admins
    
    # checks if user is admin by comparing user id to list of admins
    def is_admin(self, user):
        if user.id in self.get_admins():
            return True
        else:
            return False
    
    # nextcord slashcommand that prints out the list of admin id and their matching and their matching username and sends it to channel
    # as an embed, admins are colorized green. And their id's white.
    @nextcord.slash_command(name="admin_list", description="List of bot admins")
    async def admin_list(self, interaction: Interaction):
        admins = self.get_admins()
        embed = nextcord.Embed(title="admin_list", description="List of mBot admins", color=nextcord.Color.green())
        for admin in admins:
            embed.add_field(name=f"{admin}", value=f"{self.bot.get_user(admin)}", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)
  
def setup(bot):
    bot.add_cog(admin(bot))s