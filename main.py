import os
import json
import discord
from discord.ext import commands

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
    if not os.path.exists(DATA_FILE): return {}
    with open(DATA_FILE, "r") as f:
        try: return json.load(f)
        except: return {}

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

def get_profile(guild_id, user_id, data=None):
    if data is None:
        data = load_data()
    gid, uid = str(guild_id), str(user_id)
    
    if gid not in data or not isinstance(data[gid], dict): 
        data[gid] = {}
    if uid not in data[gid] or not isinstance(data[gid][uid], dict): 
        data[gid][uid] = {"points": 0, "inventory": {}}
        
    if "points" not in data[gid][uid]: 
        data[gid][uid]["points"] = 0
    if "inventory" not in data[gid][uid] or not isinstance(data[gid][uid]["inventory"], dict): 
        data[gid][uid]["inventory"] = {}
        
    return data, data[gid][uid]

@bot.event
async def on_ready():
    print(f'Lalamove Spam Bot is online and tracking servers safely!')

@bot.event
async def on_message(message):
    if message.author.bot: return
    if not message.guild: return  # Guard against DM interaction crashes

    if message.content.strip().lower() == "lalamove":
        data, profile = get_profile(message.guild.id, message.author.id)
        bonus = sum(qty * SHOP_ITEMS[item_id]["multiplier"] 
                    for item_id, qty in profile["inventory"].items() if item_id in SHOP_ITEMS)
        profile["points"] += (1 + bonus)
        save_data(data)
        try: await message.add_reaction("📦")
        except: pass

    await bot.process_commands(message)

@bot.command(name="lalapoints")
async def lalapoints(ctx, member: discord.Member = None):
    target = member or ctx.author
    _, profile = get_profile(ctx.guild.id, target.id)
    await ctx.send(f"📦 **{target.display_name}** has **{profile['points']:,}** points!")

@bot.command(name="lalaowned")
async def lalaowned(ctx, member: discord.Member = None):
    target = member or ctx.author
    _, profile = get_profile(ctx.guild.id, target.id)
    
    embed = discord.Embed(title=f"🚘 {target.display_name}'s Garage", color=discord.Color.orange())
    
    inv_lines = []
    for item_id, qty in profile["inventory"].items():
        if qty > 0 and item_id in SHOP_ITEMS:
            item = SHOP_ITEMS[item_id]
            inv_lines.append(f"✅ {item['emoji']} **{item['display_name']}** — *Count: {qty}* (+{(qty * item['multiplier']):,} mult)")
            
    inv_text = "\n".join(inv_lines)
    embed.add_field(name="Active Fleet Infrastructure", value=inv_text or "*This garage is empty!*", inline=False)
    embed.add_field(name="Total Points", value=f"`{profile['points']:,}` points")
    
    if target.display_avatar:
        embed.set_thumbnail(url=str(target.display_avatar.url))
    await ctx.send(embed=embed)

@bot.command(name="lalashop")
async def lalashop(ctx):
    items = list(SHOP_ITEMS.items())
    for i in range(0, len(items), 18):
        page_num = (i // 18) + 1
        embed = discord.Embed(
            title=f"🧡 Lalamove Showroom (Page {page_num}/2)", 
            description="Type `!lalabuy [item name]` to purchase an upgrade!",
            color=discord.Color.orange()
        )
        for k, v in items[i:i+18]:
            embed.add_field(name=f"{v['emoji']} {v['display_name']}", value=f"Cost: `{v['price']:,}` | Multi: `+{v['multiplier']:,}`", inline=False)
        await ctx.send(embed=embed)

@bot.command(name="lalabuy")
async def lalabuy(ctx, *, item_name: str):
    name_clean = item_name.strip().lower()
    if name_clean not in SHOP_ITEMS: 
        return await ctx.send("❌ Item not found! Verify spelling via `!lalashop`.")
        
    data, profile = get_profile(ctx.guild.id, ctx.author.id)
    item = SHOP_ITEMS[name_clean]
    
    if profile["points"] < item["price"]: 
        shortage = item["price"] - profile["points"]
        return await ctx.send(f"❌ You need `{shortage:,}` more points to purchase **{item['display_name']}**!")
        
    profile["points"] -= item["price"]
    profile["inventory"][name_clean] = profile["inventory"].get(name_clean, 0) + 1
    save_data(data)
    await ctx.send(f"🎉 {ctx.author.mention}, successfully purchased **{item['emoji']} {item['display_name']}**!")

@bot.command(name="lalasendpoints")
async def lalasendpoints(ctx, member: discord.Member, amount: int):
    if amount <= 0: 
        return await ctx.send("❌ Amount must be greater than 0!")
    if member.id == ctx.author.id:
        return await ctx.send("❌ You cannot send points to yourself!")
        
    data, sender = get_profile(ctx.guild.id, ctx.author.id)
    data, receiver = get_profile(ctx.guild.id, member.id, data=data)
    
    if sender["points"] < amount: 
        return await ctx.send("❌ Insufficient points!")
        
    sender["points"] -= amount
    receiver["points"] += amount
    save_data(data)
    await ctx.send(f"💸 Sent `{amount:,}` points to {member.mention}!")

@bot.command(name="lalatop")
async def lalatop(ctx):
    data = load_data()
    server_data = data.get(str(ctx.guild.id), {})
    
    valid_users = []
    for uid, udata in server_data.items():
        if isinstance(udata, dict) and "points" in udata:
            valid_users.append((uid, udata["points"]))
            
    top = sorted(valid_users, key=lambda x: x[1], reverse=True)[:5]
    if not top:
        return await ctx.send("📦 No one has earned any Lalamove points in this server yet!")
        
    desc = ""
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
    for i, (uid, points) in enumerate(top):
        desc += f"{medals[i]} <@{uid}> — `{points:,}` points\n"
        
    embed = discord.Embed(title="🏆 Top Drivers", description=desc, color=discord.Color.orange())
    await ctx.send(embed=embed)

bot.run(os.environ.get('DISCORD_TOKEN'))
