import os
import json
import discord
from discord.ext import commands

# --- CONFIGURATION ---
SPAM_CHANNEL_ID = 1509782202043465878
# ---------------------

intents = discord.Intents.default()
intents.message_content = True  
intents.members = True 
bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = "points.json"

SHOP_ITEMS = {
    "lalamove bike": {"price": 15, "emoji": "🚲", "display_name": "Lalamove Bike", "multiplier": 2},
    "lalamove motor": {"price": 50, "emoji": "🛵", "display_name": "Lalamove Motor", "multiplier": 4},
    "lalamove van": {"price": 150, "emoji": "🚐", "display_name": "Lalamove Van", "multiplier": 8},
    "lalamove truck": {"price": 300, "emoji": "🚚", "display_name": "Lalamove Truck", "multiplier": 16},
    "lalamove 12": {"price": 400, "emoji": "🚚", "display_name": "Lalamove 12", "multiplier": 32},
    "lalamove truck 15": {"price": 500, "emoji": "🚛", "display_name": "Lalamove Truck 15", "multiplier": 64},
    "lalamove 15": {"price": 600, "emoji": "🚛", "display_name": "Lalamove 15", "multiplier": 128},
    "lalamove 20": {"price": 900, "emoji": "🛞", "display_name": "Lalamove 20", "multiplier": 256},
    "lalamove aircraft": {"price": 2500, "emoji": "✈️", "display_name": "Lalamove Aircraft", "multiplier": 512},
    "lalamove spaceship": {"price": 10000, "emoji": "🚀", "display_name": "Lalamove Spaceship", "multiplier": 1024},
    "lalamove planet": {"price": 50000, "emoji": "🪐", "display_name": "Lalamove Planet", "multiplier": 2048},
    "lalamove sun": {"price": 800000, "emoji": "☀️", "display_name": "Lalamove Sun", "multiplier": 4096},
    "lalamove wormhole": {"price": 1200000, "emoji": "🕳️", "display_name": "Lalamove Wormhole", "multiplier": 6000},
    "lalamove neptune": {"price": 1600000, "emoji": "🔵", "display_name": "Lalamove Neptune", "multiplier": 8192},
    "lalamove jupiter": {"price": 4800000, "emoji": "🟠", "display_name": "Lalamove Jupiter", "multiplier": 16384},
    "lalamove black hole": {"price": 8500000, "emoji": "🔲", "display_name": "Lalamove Black Hole", "multiplier": 24000},
    "lalamove solar system": {"price": 14000000, "emoji": "🌌", "display_name": "Lalamove Solar System", "multiplier": 32768},
    "lalamove solar system 2": {"price": 36000000, "emoji": "🌀", "display_name": "Lalamove Solar System 2", "multiplier": 65536},
    "lalamove constellation": {"price": 55000000, "emoji": "⭐", "display_name": "Lalamove Constellation", "multiplier": 95000},
    "lalamove universe": {"price": 79000000, "emoji": "✨", "display_name": "Lalamove Universe", "multiplier": 131072},
    "lalamove multiverse": {"price": 180000000, "emoji": "🔮", "display_name": "Lalamove Multiverse", "multiplier": 262144},
    "lalamove galaxy": {"price": 350000000, "emoji": "🌌", "display_name": "Lalamove Galaxy", "multiplier": 4194304},
    "lalamove metaverse": {"price": 450000000, "emoji": "🌐", "display_name": "Lalamove Metaverse", "multiplier": 524288},
    "lalamove galaxy cluster": {"price": 950000000, "emoji": "🪐", "display_name": "Lalamove Galaxy Cluster", "multiplier": 8388608},
    "lalamove timeline": {"price": 999000000, "emoji": "⏳", "display_name": "Lalamove Timeline", "multiplier": 1048576},
    "lalamove time machine": {"price": 1500000000, "emoji": "🏎️", "display_name": "Lalamove Time Machine", "multiplier": 1500000},
    "lalamove singularity": {"price": 2500000000, "emoji": "🕳️", "display_name": "Lalamove Singularity", "multiplier": 2097152},
    "lalamove simulation": {"price": 5000000000, "emoji": "💻", "display_name": "Lalamove Simulation", "multiplier": 16777216},
    "lalamove ceo": {"price": 9999999999, "emoji": "👑", "display_name": "The Lalamove CEO", "multiplier": 9999999},
    "lalamove alternate timeline": {"price": 12000000000, "emoji": "🌿", "display_name": "Lalamove Alternate Timeline", "multiplier": 22000000},
    "lalamove omniverse": {"price": 25000000000, "emoji": "🏮", "display_name": "Lalamove Omniverse", "multiplier": 33554432},
    "lalamove board of directors": {"price": 85000000000, "emoji": "💼", "display_name": "The Lalamove Board of Directors", "multiplier": 50000000},
    "lalamove reality core": {"price": 150000000000, "emoji": "👁️", "display_name": "Lalamove Reality Core", "multiplier": 67108864},
    "lalamove matrix": {"price": 500000000000, "emoji": "🟢", "display_name": "Lalamove Matrix", "multiplier": 100000000},
    "lalamove concept of delivery": {"price": 999999999999, "emoji": "🧠", "display_name": "Lalamove Concept of Delivery", "multiplier": 134217728},
    "lalamove complex building": {"price": 1000000000000000, "emoji": "🏢", "display_name": "Lalamove Complex Building", "multiplier": 1000000000}
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
        data[user_id] = {"points": 0, "inventory": {}}
    if not isinstance(data[user_id], dict):
        data[user_id] = {"points": data[user_id], "inventory": {}}
    if "inventory" not in data[user_id] or isinstance(data[user_id]["inventory"], list):
        data[user_id]["inventory"] = {}
    return data[user_id]

@bot.event
async def on_ready():
    print(f'Lalamove Counter Bot is online!')

@bot.event
async def on_message(message):
    if message.author.bot: 
        return
    
    content_clean = message.content.strip().lower()
    
    if message.channel.id == SPAM_CHANNEL_ID and content_clean == "lalamove":
        all_data = load_data()
        user_id = str(message.author.id)
        profile = get_user_profile(all_data, user_id)
        
        total_bonus = 0
        for name, qty in profile["inventory"].items():
            for item_id, info in SHOP_ITEMS.items():
                if info["display_name"] == name:
                    total_bonus += (qty * info["multiplier"])
        
        points_to_add = 1 + total_bonus
        profile["points"] += points_to_add
        save_data(all_data)
        
        try:
            await message.add_reaction("📦")
        except:
            pass
            
    await bot.process_commands(message)

@bot.command(name="lalapoints")
async def lalapoints(ctx, member: discord.Member = None):
    target_user = member or ctx.author
    all_data = load_data()
    user_id = str(target_user.id)
    profile = get_user_profile(data=all_data, user_id=user_id)
    
    if target_user == ctx.author:
        await ctx.send(f"{ctx.author.mention}, you have **{profile['points']:,}** points! 📦\nUse `!lalaowned` to view your garage fleet configuration!")
    else:
        await ctx.send(f"📦 **{target_user.display_name}** currently has **{profile['points']:,}** Lalamove points!")

@bot.command(name="lalaowned")
async def lalaowned(ctx, member: discord.Member = None):
    target_user = member or ctx.author
    all_data = load_data()
    user_id = str(target_user.id)
    profile = get_user_profile(all_data, user_id)
    user_inventory = profile["inventory"]

    embed = discord.Embed(
        title=f"🚘 {target_user.display_name}'s Lalamove Garage 🚘",
        description="Total active fleet valuation counter.",
        color=discord.Color.orange()
    )
    
    unlocked_fleet = ""
    locked_fleet = ""
    total_vehicles = 0
    
    for item_id, info in SHOP_ITEMS.items():
        name = info['display_name']
        emoji = info['emoji']
        qty = user_inventory.get(name, 0)
        
        if qty > 0:
            unlocked_fleet += f"✅ {emoji} **{name}** — *Count: {qty}* (+{(qty * info['multiplier']):,} mult)\n"
            total_vehicles += qty
        else:
            locked_fleet += f"{emoji} ~~{name}~~ | "

    if not unlocked_fleet:
        unlocked_fleet = "*This garage is currently empty. Buy wheels using `!lalashop`!*\n"
    if not locked_fleet:
        locked_fleet = "*All delivery tiers successfully maxed out!*"
    else:
        locked_fleet = locked_fleet[:-3] # Trim final piping character

    embed.add_field(name="Active Fleet Infrastructure", value=unlocked_fleet, inline=False)
    embed.add_field(name="Locked Upgrades", value=locked_fleet, inline=False)
    embed.add_field(name="Total Fleet Size", value=f"`{total_vehicles:,}` elements", inline=True)
    embed.add_field(name="Current Wallet Balance", value=f"`{profile['points']:,}` points", inline=True)
    
    embed.set_thumbnail(url=str(target_user.display_avatar.url))
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
    receiver_profile = get_user_profile(all_data, receiver_id)
    
    if sender_profile["points"] < amount:
        await ctx.send(f"{ctx.author.mention}, you don't have enough points! You only have `{sender_profile['points']:,}` points.")
        return

    sender_profile["points"] -= amount
    receiver_profile["points"] += amount
    save_data(all_data)
    
    await ctx.send(f"💸 {ctx.author.mention} sent **{amount:,}** Lalamove points to {member.mention}! 📦")

@bot.command(name="lalashop")
async def lalashop(ctx):
    # Splits the 36 massive shop entries evenly across 2 distinct pages to stay safely under Discord's 25 field embed cap!
    items = list(SHOP_ITEMS.items())
    chunk_size = 18
    
    for i in range(0, len(items), chunk_size):
        chunk = items[i:i + chunk_size]
        page_num = (i // chunk_size) + 1
        
        embed = discord.Embed(
            title=f"🧡 Lalamove Vehicle Showroom (Page {page_num}/2) 🧡",
            description="Spend your points to upgrade your delivery fleet! Use `!lalabuy [vehicle name]` to purchase.",
            color=discord.Color.orange()
        )
        
        for item_id, info in chunk:
            formatted_price = f"{info['price']:,}"
            formatted_mult = f"{info['multiplier']:,}"
            embed.add_field(
                name=f"{info['emoji']} {info['display_name']}",
                value=f"Cost: `{formatted_price}` points | Bonus: `+ {formatted_mult}` per message",
                inline=False
            )
            
        embed.set_footer(text="Keep spamming 'lalamove' to earn more points!")
        await ctx.send(embed=embed)

@bot.command(name="lalabuy")
async def lalabuy(ctx, *, item_name: str = None):
    if not item_name:
        await ctx.send(f"{ctx.author.mention}, please tell me what you want to buy! Example: `!lalabuy lalamove complex building`")
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
        
    if profile["points"] < item_info["price"]:
        shortage = item_info["price"] - profile["points"]
        await ctx.send(f"{ctx.author.mention}, you need `{shortage:,}` more points to buy the {item_display}!")
        return
        
    profile["points"] -= item_info["price"]
    profile["inventory"][item_info['display_name']] = profile["inventory"].get(item_info['display_name'], 0) + 1
    save_data(all_data)
    
    await ctx.send(f"🎉 {ctx.author.mention}, you successfully bought a **{item_display}** for `{item_info['price']:,}` points! Your delivery spam multiplier has increased!")

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
        try:
            user = await bot.fetch_user(int(user_id))
            name = user.display_name
        except:
            name = f"User ID: {user_id}"
            
        leaderboard_text += f"{medals[index]} **{name}** — `{points:,}` points\n"
        
    embed.add_field(name="Leaderboard", value=leaderboard_text, inline=False)
    embed.add_field(name="\u200b", value="> **Note:** Every extra vehicle you buy stacks your multiplier higher and higher!", inline=False)
    
    embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

bot.run(os.environ.get('DISCORD_TOKEN'))
