import os
import json
import asyncio
import discord
from discord.ext import commands

# --- CONFIGURATION ---
SPAM_CHANNEL_NAME = "lalamove-spam" 
# ---------------------

intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = "points.json"

def load_points():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {}

def save_points(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@bot.event
async def on_ready():
    print(f'Lalamove Counter Bot is online as {bot.user.name}!')

@bot.event
async def on_message(message):
    if message.author.bot: return
    if message.channel.name == SPAM_CHANNEL_NAME:
        content_clean = message.content.strip().lower()
        if content_clean == "lalamove":
            points_data = load_points()
            user_id = str(message.author.id)
            points_data[user_id] = points_data.get(user_id, 0) + 1
            save_points(points_data)
            try: await message.add_reaction("📦")
            except discord.HTTPException: pass
    await bot.process_commands(message)

@bot.command(name="lalapoints")
async def lalapoints(ctx):
    points_data = load_points()
    user_id = str(ctx.author.id)
    current_points = points_data.get(user_id, 0)
    await ctx.send(f"{ctx.author.mention}, you have {current_points} points! 📦")

@bot.command(name="lalatop")
async def lalatop(ctx):
    points_data = load_points()
    if not points_data:
        await ctx.send("📦 No one has earned any Lalamove points yet!")
        return
    sorted_players = sorted(points_data.items(), key=lambda item: item[1], reverse=True)
    top_5 = sorted_players[:5]
    embed = discord.Embed(
        title="🏆 Lalamove Top Delivery Drivers 🏆",
        description="Here are the top 5 spammers with the most points!",
        color=discord.Color.orange()
    )
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
    leaderboard_text = ""
    for index, (user_id, points) in enumerate(top_5):
        member = ctx.guild.get_member(int(user_id))
        name = member.display_name if member else f"User ID: {user_id}"
        leaderboard_text += f"{medals[index]} **{name}** — `{points}` points\n"
    embed.add_field(name="Leaderboard", value=leaderboard_text, inline=False)
    embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

# Grab the secret token we gave to Render safely
bot.run(os.environ.get('DISCORD_TOKEN'))
