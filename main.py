import discord
from discord.ext import commands
import paramiko
import os
import json

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

with open("config.json", "r") as config_file:
    config = json.load(config_file)
    token = config["token"]
    prefix = config["prefix"]

def load_cogs():
    for folder in os.listdir('./cogs/'):
        if folder.endswith(".py"):
            cog_name = f'cogs.{folder[:-3]}'
            try:
                bot.load_extension(cog_name)
                print(f'Loaded cog: {cog_name}')
            except Exception as e:
                print(f'Failed to load cog: {cog_name}\n{e}')
        else:
            for filename in os.listdir(f"./cogs/{folder}"):
                if filename.endswith('.py'):
                    cog_name = f'cogs.{folder}.{filename[:-3]}'
                    try:
                        bot.load_extension(cog_name)
                        print(f'Loaded cog: {cog_name}')
                    except Exception as e:
                        print(f'Failed to load cog: {cog_name}\n{e}')

load_cogs()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

bot.run(token)
