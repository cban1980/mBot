"""Warhammer 40k commands and functions."""
import random
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import requests
from bs4 import BeautifulSoup as bs

def scrape_thoughts():
    """Scrape the Lexicanum for thoughts of the day."""
    urls = [
    "https://wh40k.lexicanum.com/wiki/Thought_for_the_day_(A_-_H)",
    "https://wh40k.lexicanum.com/wiki/Thought_for_the_day_(I_-_P)",
    "https://wh40k.lexicanum.com/wiki/Thought_for_the_day_(Q_-_Z)"
    ]
    url = random.choice(urls)
    response = requests.get(url,timeout=10)
    soup = bs(response.content, "html.parser")

    # Find all tables under the "mw-content-text" div with class "mw-content-ltr"
    content_text_div = soup.find("div", {"id": "mw-content-text", "class": "mw-content-ltr"})
    tables = content_text_div.find_all("table")

    # Extract quotes and their sources from each table
    thoughts = []
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) > 0:
                quote = cells[0].get_text().strip()
                source = cells[1].get_text().strip() if len(cells) > 1 else ""
                thoughts.append((quote, source))
    return thoughts

def get_random_quote():
    """Return a random quote from the Lexicanum."""
    urls = [
    "https://wh40k.lexicanum.com/wiki/Imperium_Quotes",
    "https://wh40k.lexicanum.com/wiki/Adeptus_Arbites_Quotes",
    "https://wh40k.lexicanum.com/wiki/Officio_Assassinorum_Quotes",
    "https://wh40k.lexicanum.com/wiki/Astra_Militarum_Quotes",
    "https://wh40k.lexicanum.com/wiki/Ecclesiarchy_Quotes",
    "https://wh40k.lexicanum.com/wiki/Inquisition_Quotes",
    "https://wh40k.lexicanum.com/wiki/Adeptus_Mechanicus_Quotes",
    "https://wh40k.lexicanum.com/wiki/Imperial_Navy_Quotes",
    "https://wh40k.lexicanum.com/wiki/Adepta_Sororitas_Quotes",
    "https://wh40k.lexicanum.com/wiki/Space_Marine_Quotes",
    "https://wh40k.lexicanum.com/wiki/Tactica_Imperium_passages",
    "https://wh40k.lexicanum.com/wiki/Chaos_Quotes",
    "https://wh40k.lexicanum.com/wiki/Eldar_Quotes",
    "https://wh40k.lexicanum.com/wiki/Tau_Quotes",
    "https://wh40k.lexicanum.com/wiki/Tyranid_Quotes"
    ]
    url = random.choice(urls)
    response = requests.get(url, timeout=10)
    soup = bs(response.content, 'html.parser')
    table = soup.find("div", {"id": "mw-content-text", "class": "mw-content-ltr"})
    rows = table.find_all('tr')
    quotes = []
    for row in rows[1:]:
        cells = row.find_all('td')
        if len(cells) >= 3:
            speaker = cells[0].text.strip()
            quote = cells[1].text.strip()
            source = cells[2].text.strip()
            if speaker == "Speaker" or not speaker:
                continue
            if quote == "Quote" or not quote:
                continue
            if source == "Source" or not source:
                continue
            quotes.append({"Speaker": speaker, "Quote": quote, "Source": source})
    if not quotes:
        return None
    random_quote = random.choice(quotes)
    return (random_quote["Quote"], random_quote["Speaker"], random_quote["Source"])

class WarhammerCog(commands.Cog):
    """Warhammer 40k commands and functions."""
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    # Define a slash command to send a random thought of the day and its source
    @nextcord.slash_command(name="whthought", description="Warhammer 40k thought of the day")
    async def whthought(self, ctx: nextcord.Interaction):
        """Sends a random Warhammer 40k thought of the day."""
        # Scrape the quotes
        quotes = scrape_thoughts()
        # Get a random quote and its source
        quote, source = random.choice(quotes)
        # Create an embed with the quote and source
        embed = nextcord.Embed(title="Warhammer Thought of the day", color=0x00ff00)
        embed.add_field(name="Quote: ", value=quote, inline=False)
        embed.add_field(name="Source: ", value=source, inline=False)
        # Send the embed
        await ctx.send(embed=embed)

    @nextcord.slash_command(name="whquote")
    async def whquote(self, ctx: nextcord.Interaction):
        """Sends a random Warhammer 40k quote."""
        quote, speaker, source = get_random_quote()
        while (
            not speaker or speaker == "Speaker" or
            not quote or quote == "Quote" or
            not source or source == "Source"
        ):
            quote, speaker, source = get_random_quote()
        embed = nextcord.Embed()
        if quote and quote != "Quote":
            embed.add_field(name="Quote: ", value=quote, inline=True)
        if speaker and speaker != "Speaker":
            embed.add_field(name="Origin: ", value=speaker, inline=False)
        if source and source != "Source":
            embed.add_field(name="Source: ", value=source, inline=False)
        await ctx.send(embed=embed)

    @nextcord.slash_command(name="roll_dice", description="Dice rolling for Warhammer games.")
    async def roll_dice(self, interaction: nextcord.Interaction, dice: str):
        """Rolls a specified number of dice in a Warhammer game."""
        try:
            num_dice, dice_type = dice.split('d')
            num_dice = int(num_dice)
            dice_type = int(dice_type)
        except ValueError:
            await interaction.send(
            'Invalid input format. Please specify the number and type of dice to roll (e.g. 2d6).'
            )
            return

        if num_dice <= 0 or dice_type <= 0:
            await interaction.send(
            'Invalid input. The number and type of dice to roll must be positive integers.'
            )
            return

        rolls = [random.randint(1, dice_type) for _ in range(num_dice)]
        total = sum(rolls)

        await interaction.response.send_message(
            f'Rolling {num_dice}d{dice_type}...\n{rolls}\nTotal: {total}'
        )

def setup(bot):
    """Add the cog to the bot."""
    bot.add_cog(WarhammerCog(bot))
