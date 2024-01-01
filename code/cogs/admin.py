import nextcord
from nextcord.ext import commands
from nextcord import Interaction

class admin(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    # list of bot admins by user id read from .admins file
    def get_admins(self):
        admins = []
        with open('.admins', 'r') as f:
            for line in f:
                admins.append(int(line.strip()))
        return admins
    # check if user is admin, if not return false
    def is_admin(self, user):
        if user.id in self.get_admins():
            return True
        else:
            return False
    # nextcord slashcommand that prints out the list of admin id and their matching and their matching username and sends it to channel
    @nextcord.slash_command(name="admin_list", description="List of bot admins")
    async def admin_list(self, interaction: Interaction):
        admins = self.get_admins()
        admin_list = ""
        for admin in admins:
            admin_list += f"{admin} - {self.bot.get_user(admin).name}\n"
        await interaction.send(admin_list)
  
def setup(bot):
    bot.add_cog(admin(bot))