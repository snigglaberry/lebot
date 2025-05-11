import discord
from discord.ext import commands, tasks
import random
import json

TOKEN = 'MTM3MTExODA2MzE1OTg2OTU0Mg.G0XwxK.3_RxAYgeiNOHeBE3MmZY7hHwBcr7vjYgmG1QJU'
LEBRON_ROLE_ID = 1371124034904920184  # The LeBron role
glaze_messages = [
    "LeBron’s ledihh reshaped the NBA timeline.",
    "Even gravity submits to LeBron’s colossal ledihh.",
    "LeBron's ledihh entered the MVP race and won.",
    "The refs don't call travel — they're scared of the ledihh.",
    "Space Jam was actually about LeBron's ledihh saving the universe.",
    "LeBron's ledihh signed a max contract with 30 teams.",
    "You can’t guard what you can’t comprehend. That’s his ledihh.",
    "Jordan walked so LeBron’s **ledihh** could fly.",
    "His jersey number is 6 because the ledihh broke the number 1–5 system.",
    "Scientists tried to measure it and invented a new SI unit: the ledihhon."
]

# Load saved channels
def load_channels():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except:
        return {}

def save_channels(data):
    with open('config.json', 'w') as f:
        json.dump(data, f)

channel_config = load_channels()

intents = discord.Intents.default()
intents.message_content = False
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()
    send_daily_glaze.start()

# /setup – only if user has LeBron role
@bot.tree.command(name="setup", description="Set this channel for daily LeBron glazing")
async def setup(interaction: discord.Interaction):
    user_roles = [r.id for r in interaction.user.roles]
    if LEBRON_ROLE_ID not in user_roles:
        await interaction.response.send_message("🚫 You need the LeBron role to run this command.", ephemeral=True)
        return
    channel_config[str(interaction.guild_id)] = interaction.channel.id
    save_channels(channel_config)
    await interaction.response.send_message("✅ Channel set for daily LeBron glazing.", ephemeral=True)

# /glaze – anyone can use
@bot.tree.command(name="glaze", description="Glaze LeBron instantly")
async def glaze(interaction: discord.Interaction):
    message = random.choice(glaze_messages) + "\n\nLeBron’s **ledihh** is unmatched 💪👑"
    await interaction.response.send_message(message)

# /lebron <user> – only if user has LeBron role
@bot.tree.command(name="lebron", description="Give the LeBron role to a user")
@discord.app_commands.describe(user="The user to give the LeBron role to")
async def lebron(interaction: discord.Interaction, user: discord.Member):
    if LEBRON_ROLE_ID not in [r.id for r in interaction.user.roles]:
        await interaction.response.send_message("🚫 Only fellow glazers can assign the LeBron role.", ephemeral=True)
        return
    role = interaction.guild.get_role(LEBRON_ROLE_ID)
    if role is None:
        await interaction.response.send_message("❌ LeBron role not found.", ephemeral=True)
        return
    try:
        await user.add_roles(role)
        await interaction.response.send_message(f"✅ {user.mention} has been blessed with the LeBron role.")
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to assign that role.", ephemeral=True)

# Daily message loop
@tasks.loop(hours=24)
async def send_daily_glaze():
    await bot.wait_until_ready()
    for guild_id, channel_id in channel_config.items():
        channel = bot.get_channel(channel_id)
        if channel:
            try:
                await channel.send(random.choice(glaze_messages))
            except Exception as e:
                print(f"Failed to send in {guild_id}: {e}")

bot.run(TOKEN)
