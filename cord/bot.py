# This example requires the 'members' and 'message_content' privileged intents to function.

import os
import nextcord

import system
import chatbot
import embedder
import autochat
import community

from dotenv import load_dotenv
from nextcord.ext import commands
from nextcord import SlashOption

load_dotenv()

bot = commands.Bot(
    intents=nextcord.Intents.all(),
    default_guild_ids=[int(guild_id) for guild_id in os.getenv('DISCORD_GUILD_IDS').split()] # so slash commands work
)

@bot.event
async def on_ready():
    print(f'Online as {bot.user} (ID: {bot.user.id})')
    await bot.change_presence(activity=nextcord.Game(name='with fire'))

@bot.event
async def on_message(message):
    if message.author.bot: # block bots
        return

    await autochat.process(message)
    await bot.process_commands(message)

@bot.slash_command(description='Chat with AI')
async def chat(interaction: nextcord.Interaction,
    prompt: str = SlashOption(description='AI Prompt', required=True)
):
    await chatbot.respond(interaction, prompt)

@bot.slash_command(description='Sets your DMs up, so you can write the bot.')
async def dm(interaction: nextcord.Interaction):
    try:
        await interaction.user.create_dm()
        await embedder.info(interaction.user.dm_channel, 'Hello!')
    except nextcord.Forbidden:
        await embedder.error(interaction, text="""Please open this server\'s options,
go to `Privacy Settings` and enable `Direct Messages` as well as `Message Requests`.""")
    else:     
        await embedder.ok(interaction, 'Great, DMs are set up successfully!')

@bot.slash_command(description='Get your secret NovaAI API credentials.')
async def credentials(interaction: nextcord.Interaction):
    return await system.get_credentials(interaction)

@bot.slash_command(description='Leaderboard.')
async def leaderboard(interaction: nextcord.Interaction):
    await community.leaderboard(interaction)

bot.run(os.getenv('DISCORD_TOKEN'))
