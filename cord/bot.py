# This example requires the 'members' and 'message_content' privileged intents to function.

import os
import discord

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_ready():
    print(f'Online as {bot.user} (ID: {bot.user.id})')
    await bot.change_presence(activity=discord.Game(name='with fire'))

@bot.event
async def on_message(message):
    await bot.process_commands(message)

bot.run(os.getenv('DISCORD_TOKEN'))
