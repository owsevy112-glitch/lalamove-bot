import os
import json
import discord
from discord.ext import commands

# --- CONFIGURATION ---
SPAM_CHANNEL_ID = 1507731908480729259  # Updated with your Channel ID
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
    # Ensure inventory is a dict (fixes legacy list issue)
    if not isinstance(data[user_id].get("inventory"), dict):
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
    
    # Check against the specific channel ID
    if message.channel.id == SPAM_CHANNEL_ID and content_clean == "lalamove":
        all_data = load_data()
        user_id = str(message.author.id)
        profile = get_user_profile(all_data, user_id)
        
        # Calculate bonus: 1 base point + all multipliers
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
    target = member or ctx.author
    profile = get_user_profile(load_data(), str(target.id))
    await ctx.send(f"📦 **{target.display_name}** has **{profile['points']}** points!")

@bot.command(name="lalashop")
async def lalashop(ctx):
    embed = discord.Embed(title="🧡 Lalamove Vehicle Showroom 🧡", color=discord.Color.orange())
    for item_id, info in SHOP_ITEMS.items():
        embed.add_field(name=f"{info['emoji']} {info['display_name']}", value=f"Price: `{info['price']}` | Bonus: `x{info['multiplier']}`", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="lalabuy")
async def lalabuy(ctx, *, item_name: str = None):
    if not item_name: return await ctx.send("Usage: `!lalabuy [vehicle name]`")
    item_clean = item_name.strip().lower()
    if item_clean not in SHOP_ITEMS: return await ctx.send("Vehicle not found! Check `!lalashop`.")
    
    all_data = load_data()
    profile = get_user_profile(all_data, str(ctx.author.id))
    item = SHOP_ITEMS[item_clean]
    
    if profile["points"] < item["price"]: return await ctx.send(f"Not enough points! You need `{item['price'] - profile['points']}` more.")
    
    profile["points"] -= item["price"]
    profile["inventory"][item["display_name"]] = profile["inventory"].get(item["display_name"], 0) + 1
    save_data(all_data)
    await ctx.send(f"🎉 You bought **{item['display_name']}**! Your point bonus has increased.")

@bot.command(name="lalaowned")
async def lalaowned(ctx, member: discord.Member = None):
    target = member or ctx.author
    profile = get_user_profile(load_data(), str(target.id))
    inv = profile["inventory"]
    fleet = ""
    for item_id, info in SHOP_ITEMS.items():
        name = info['display_name']
        qty = inv.get(name, 0)
        if qty > 0: fleet += f"✅ {info['emoji']} {name}: x{qty} (Bonus: +{qty * info['multiplier']})\n"
        else: fleet += f"❌ {info['emoji']} {name}\n"
    await ctx.send(f"🚘 **{target.display_name}'s Garage**:\n{fleet or 'Empty!'}")

@bot.command(name="lalatop")
async def lalatop(ctx):
    all_data = load_data()
    leaderboard = sorted(all_data.items(), key=lambda x: x[1]["points"], reverse=True)[:5]
    text = "\n".join([f"**{ctx.guild.get_member(int(uid)).display_name if ctx.guild.get_member(int(uid)) else uid}**: {data['points']} pts" for uid, data in leaderboard])
    await ctx.send(f"🏆 **Top Drivers**:\n{text}")

bot.run(os.environ.get('DISCORD_TOKEN'))
