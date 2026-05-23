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

SHOP_ITEMS = {
    "lalamove bike": {"price": 15, "emoji": "🚲", "display_name": "Lalamove Bike"},
    "lalamove motor": {"price": 50, "emoji": "🛵", "display_name": "Lalamove Motor"},
    "lalamove van": {"price": 150, "emoji": "🚐", "display_name": "Lalamove Van"},
    "lalamove truck": {"price": 300, "emoji": "🚚", "display_name": "Lalamove Truck"},
    "lalamove 12": {"price": 400, "emoji": "🚚", "display_name": "Lalamove 12"},
    "lalamove truck 15": {"price": 500, "emoji": "🚛", "display_name": "Lalamove Truck 15"},
    "lalamove 15": {"price": 600, "emoji": "🚛", "display_name": "Lalamove 15"},
    "lalamove 20": {"price": 900, "emoji": "🛞", "display_name": "Lalamove 20"},
    "lalamove aircraft": {"price": 2500, "emoji": "✈️", "display_name": "Lalamove Aircraft"},
    "lalamove spaceship": {"price": 10000, "emoji": "🚀", "display_name": "Lalamove Spaceship"},
    "lalamove planet": {"price": 50000, "emoji": "🪐", "display_name": "Lalamove Planet"},
}

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_user_profile(data, user_id):
    if user_id not in data:
        data[user_id] = {"points": 0, "inventory": []}
    elif isinstance(data[user_id], int):
        data[user_id] = {"points": data[user_id], "inventory": []}
    elif "inventory" not in data[user_id]:
        data[user_id]["inventory"] = []
    return data[user_id]

@bot.event
async def on_ready():
    print(f'Lalamove Counter Bot is online as {bot.user.name}!')

@bot.event
async def on_message(message):
    if message.author.bot: return
    if message.channel.name == SPAM_CHANNEL_NAME:
        content_clean = message.content.strip().lower()
        if content_clean == "lalamove":
            all_data = load_data()
            user_id = str(message.author.id)
            profile = get_user_profile(all_data, user_id)
            
            profile["points"] += 1
            save_data(all_data)
            try: await message.add_reaction("📦")
            except discord.HTTPException: pass
    await bot.process_commands(message)

@bot.command(name="lalapoints")
async def lalapoints(ctx, member: discord.Member = None):
    target_user = member or ctx.author
    
    all_data = load_data()
    user_id = str(target_user.id)
    profile = get_user_profile(data=all_data, user_id=user_id)
    
    if target_user == ctx.author:
        await ctx.send(f"{ctx.author.mention}, you have **{profile['points']}** points! 📦\nUse `!lalaowned` to view your garage fleet configuration!")
    else:
        await ctx.send(f"📦 **{target_user.display_name}** currently has **{profile['points']}** Lalamove points!")

@bot.command(name="lalaowned")
async def lalaowned(ctx, member: discord.Member = None):
    target_user = member or ctx.author
    
    all_data = load_data()
    user_id = str(target_user.id)
    profile = get_user_profile(all_data, user_id)
    user_inventory = profile["inventory"]

    embed = discord.Embed(
        title=f"🚘 {target_user.display_name}'s Lalamove Garage 🚘",
        description=f"Total active fleet valuation counter.",
        color=discord.Color.orange()
    )
    
    fleet_list = ""
    total_vehicles = 0
    
    for item_id, info in SHOP_ITEMS.items():
        name = info['display_name']
        emoji = info['emoji']
        if name in user_inventory:
            fleet_list += f"✅ {emoji} **{name}** — *Owned*\n"
            total_vehicles += 1
        else:
            fleet_list += f"❌ {emoji} ~~{name}~~ — *Locked*\n"

    if total_vehicles == 0:
        fleet_list += "\n*This garage is currently empty. Buy wheels using `!lalashop`!*"

    embed.add_field(name="Current Fleet Progress", value=fleet_list, inline=False)
    embed.add_field(name="Total Fleet Size", value=f"`{total_vehicles} / {len(SHOP_ITEMS)}` unlocked", inline=True)
    embed.add_field(name="Current Wallet Balance", value=f"`{profile['points']}` points", inline=True)
    
    embed.set_thumbnail(url=target_user.display_avatar.url)
    embed.set_footer(text=f"Requested by {ctx.author.display_name}")
    await ctx.send(embed=embed)

@bot.command(name="lalasendpoints")
async def lalasendpoints(ctx, member: discord.Member = None, amount: int = None):
    if not member or not amount:
        await ctx.send(f"{ctx.author.mention}, you used the command incorrectly! Format: `!lalasendpoints @user [amount]`")
        return
        
    if member.id == ctx.author.id:
        await ctx.send(f"{ctx.author.mention}, you can't send points to yourself! 🤔")
        return
        
    if amount <= 0:
        await ctx.send(f"{ctx.author.mention}, you must send at least 1 point! 📦")
        return

    all_data = load_data()
    sender_id = str(ctx.author.id)
    receiver_id = str(member.id)
    
    sender_profile = get_user_profile(all_data, sender_id)
    
    # Check if sender has enough money
    if sender_profile["points"] < amount:
        await ctx.send(f"{ctx.author.mention}, you don't have enough points! You only have `{sender_profile['points']}` points.")
        return

    receiver_profile = get_user_profile(all_data, receiver_id)
    
    # Perform the transaction
    sender_profile["points"] -= amount
    receiver_profile["points"] += amount
    
    save_data(all_data)
    
    await ctx.send(f"💸 {ctx.author.mention} sent **{amount}** Lalamove points to {member.mention}! 📦")

@bot.command(name="lalashop")
async def lalashop(ctx):
    embed = discord.Embed(
        title="🧡 Lalamove Vehicle Showroom 🧡",
        description="Spend your points to upgrade your delivery fleet! Use `!lalabuy [vehicle name]` to purchase.",
        color=discord.Color.orange()
    )
    for item_id, info in SHOP_ITEMS.items():
        embed.add_field(
            name=f"{info['emoji']} {info['display_name']}",
            value=f"Cost: `{info['price']}` points",
            inline=False
        )
    embed.set_footer(text="Keep spamming 'lalamove' to earn more points!")
    await ctx.send(embed=embed)

@bot.command(name="lalabuy")
async def lalabuy(ctx, *, item_name: str = None):
    if not item_name:
        await ctx.send(f"{ctx.author.mention}, please tell me what you want to buy! Example: `!lalabuy lalamove aircraft`")
        return
    
    item_clean = item_name.strip().lower()
    if item_clean not in SHOP_ITEMS:
        await ctx.send(f"{ctx.author.mention}, that item doesn't exist in the shop! Check `!lalashop` for correct names.")
        return
    
    all_data = load_data()
    user_id = str(ctx.author.id)
    profile = get_user_profile(all_data, user_id)
    
    item_info = SHOP_ITEMS[item_clean]
    item_display = f"{item_info['emoji']} {item_info['display_name']}"
    
    if item_info['display_name'] in profile["inventory"]:
        await ctx.send(f"{ctx.author.mention}, you already own a {item_display}!")
        return
        
    if profile["points"] < item_info["price"]:
        shortage = item_info["price"] - profile["points"]
        await ctx.send(f"{ctx.author.mention}, you need `{shortage}` more points to buy the {item_display}!")
        return
        
    profile["points"] -= item_info["price"]
    profile["inventory"].append(item_info['display_name'])
    save_data(all_data)
    
    await ctx.send(f"🎉 {ctx.author.mention}, you successfully bought a **{item_display}** for `{item_info['price']}` points!")

@bot.command(name="lalatop")
async def lalatop(ctx):
    all_data = load_data()
    if not all_data:
        await ctx.send("📦 No one has earned any Lalamove points yet!")
        return
        
    leaderboard = []
    for user_id, info in all_data.items():
        points = info["points"] if isinstance(info, dict) else info
        leaderboard.append((user_id, points))
        
    sorted_players = sorted(leaderboard, key=lambda item: item[1], reverse=True)
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

bot.run(os.environ.get('DISCORD_TOKEN'))
