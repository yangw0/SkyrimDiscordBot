import discord
import requests
import os
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
SEARCH_URL = "http://127.0.0.1:5000/weapons/search"
ALL_URL = "http://127.0.0.1:5000/weapons"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Bot connected as {client.user}")

def parse_search_query(query: str):
    filters = {}
    parts = query.strip().split()
    for part in parts:
        if '=' in part:
            key, value = part.split('=', 1)
            filters[key.strip()] = value.strip()
        else:
            filters["name"] = part
    return filters

def build_embed(weapon):
    embed = discord.Embed(title=weapon["name"], color=0x00ff00)
    embed.add_field(name="Damage", value=str(weapon["damage"]), inline=True)
    embed.add_field(name="Weight", value=str(weapon["weight"]), inline=True)
    embed.add_field(name="Value", value=str(weapon["value"]), inline=True)
    embed.add_field(name="Type", value=weapon["type"] or "N/A", inline=True)
    if weapon["perk"]:
        embed.add_field(name="Perk", value=weapon["perk"], inline=True)
    if weapon["upgrade"]:
        embed.add_field(name="Upgrade", value=weapon["upgrade"], inline=True)
    if weapon["category"]:
        embed.add_field(name="Category", value=weapon["category"], inline=True)
    if weapon["speed"]:
        embed.add_field(name="Speed", value=str(weapon["speed"]), inline=True)
    return embed

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.strip()

    if content.startswith("!search"):
        query = content[len("!search"):].strip()
        filters = parse_search_query(query)
        if not filters:
            await message.channel.send("Please provide filters like `name=elven` or `type=bow`.")
            return
        response = requests.get(SEARCH_URL, params=filters)
        if response.status_code != 200:
            await message.channel.send("⚠️ Error contacting the API.")
            return
        weapons = response.json()
        if not weapons:
            await message.channel.send("No matching weapons found.")
            return
        for weapon in weapons[:5]:
            await message.channel.send(embed=build_embed(weapon))

    elif content.startswith("!random"):
        response = requests.get(ALL_URL)
        if response.status_code != 200:
            await message.channel.send("⚠️ Could not retrieve weapons.")
            return
        weapons = response.json()
        if not weapons:
            await message.channel.send("⚠️ No weapons available.")
            return
        weapon = random.choice(weapons)
        await message.channel.send(embed=build_embed(weapon))

    elif content.startswith("!help"):
     help_text= (
        "**🗡️ SkyrimBot Help Menu**\n\n"
        "**Commands:**\n"
        "`!search [filters]` - Search for weapons using filters like:\n"
        " • `name=daedric`\n"
        " • `type=sword`\n"
        " • `perk=Smithing`\n"
        " • `category=War Axe`\n"
        " • `min_damage=15 max_value=2000`\n\n"
        "`!random` - Get a random weapon from the database\n"
        "`!help` - Show this command list\n\n"
        "**Examples:**\n"
        "`!search name=elven`\n"
        "`!search type=bow min_damage=10 max_value=1000`\n"
        "`!search perk=smithing category=Dagger`\n"
        "`!random`\n\n"
        "You can combine multiple filters for more precise results."
    )
    await message.channel.send(help_text)


client.run(TOKEN)
