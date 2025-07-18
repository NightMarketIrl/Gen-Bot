import discord
from discord.ext import commands
from discord.ui import View, Button
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

account_files = {
    "discord": "discord.txt",
    "steam": "steam.txt",
    "fivem": "fivem.txt"
}

def get_and_remove_first_line(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as f:
        lines = f.readlines()
    if not lines:
        return None
    first_line = lines[0].strip()
    with open(file_path, "w") as f:
        f.writelines(lines[1:])
    return first_line

class AccountView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get Discord Account", style=discord.ButtonStyle.blurple)
    async def get_discord_account(self, interaction: discord.Interaction, button: Button):
        await self.send_account(interaction, "discord")

    @discord.ui.button(label="Get Steam Account", style=discord.ButtonStyle.green)
    async def get_steam_account(self, interaction: discord.Interaction, button: Button):
        await self.send_account(interaction, "steam")

    @discord.ui.button(label="Get FiveM Account", style=discord.ButtonStyle.red)
    async def get_fivem_account(self, interaction: discord.Interaction, button: Button):
        await self.send_account(interaction, "fivem")

    async def send_account(self, interaction: discord.Interaction, category: str):
        account = get_and_remove_first_line(account_files[category])
        if account:
            try:
                await interaction.user.send(f"Here is your {category} account:\n`{account}`")
                await interaction.response.send_message("Check your DMs! ✅", ephemeral=True)
            except discord.Forbidden:
                await interaction.response.send_message("Enable DMs so I can send you the account!", ephemeral=True)
        else:
            await interaction.response.send_message(f"No more {category} accounts left. ❌", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
@commands.has_permissions(administrator=True)
async def post_buttons(ctx):
    view = AccountView()
    await ctx.send("Click a button to get an account:", view=view)

bot.run(os.getenv("BOT_TOKEN"))
