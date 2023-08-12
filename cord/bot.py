"""Bot base."""

import os
import nextcord
import datetime

import api
import chatbot
import embedder
import autochat
import accounts
import community
import tutorials
import credential_manager

from dotenv import load_dotenv
from nextcord.ext import commands
from nextcord import SlashOption

load_dotenv()

guild_ids = [int(guild_id) for guild_id in os.getenv('DISCORD_GUILD_IDS').split()]

bot = commands.Bot(
    intents=nextcord.Intents.all(),
    default_guild_ids=guild_ids  # so slash commands work
)

@bot.event
async def on_message(message):
    if message.author.bot: # block bots
        return

    await autochat.process(message)
    await bot.process_commands(message)

# @bot.slash_command(description='Chat with AI')
# async def chat(interaction: nextcord.Interaction,
#     prompt: str = SlashOption(description='AI Prompt', required=True)
# ):
#     await chatbot.respond(interaction, prompt)

@bot.slash_command(description='Sets your DMs up, so you can write the bot.')
async def dm_setup(interaction: nextcord.Interaction):
    try:
        await interaction.user.create_dm()
        await embedder.info(interaction.user.dm_channel, 'Hello!')
    except nextcord.Forbidden:
        await embedder.error(interaction, text="""Please open this server\'s options,
go to `Privacy Settings` and enable `Direct Messages` as well as `Message Requests`.""")

    else:
        await embedder.ok(interaction, 'Great, DMs are set up successfully!')

@bot.slash_command(description='Create your account and get your API key.')
async def credentials(interaction: nextcord.Interaction):
    return await credential_manager.get_credentials(interaction)

@bot.slash_command(description='Leaderboard.')
async def leaderboard(interaction: nextcord.Interaction):
    return await community.leaderboard(interaction)

@bot.slash_command(description='Get info and stats about your NovaAI API account.')
async def account(interaction: nextcord.Interaction):
    return await accounts.get_info(interaction)

@bot.slash_command(name='credits', description='Get information about the amount of credits you have on your NovaAI API account.')
async def credits_(interaction: nextcord.Interaction):
    return await accounts.get_credits(interaction)

@bot.slash_command(description='Get credits of a certain user. Admin only.')
async def credits_of(interaction: nextcord.Interaction, user: nextcord.User):
    return await accounts.get_credits_of(interaction, user)

@bot.slash_command(description='Manually set the credits of a certain user. Admin only.')
async def set_credits(interaction: nextcord.Interaction, user: nextcord.User, amount: int):
    return await accounts.set_credits(interaction, user, amount)

@bot.slash_command(description='View examples and tips for implementing NovaAI\'s API.')
async def tutorial(interaction: nextcord.Interaction,
    how_can_i: str = SlashOption(#
        description='Read a tutorial on how to...',
        required=True,
        choices=[
            'fix error 401 (invalid key)',
            'fix error 429 (ratelimit/not enough credits)',
            'use GPT-4',
            'use curl',
            'use Node.js',
            'get my NovaAI API key',
            'use the Python library',
            'fix ModuleNotFoundErrors',
            'use the API in custom front-ends',
            'program a Python Discord Bot with streaming',
        ]
    )
):
    return await tutorials.send(interaction, how_can_i)

@bot.slash_command(description='Lookup members by their Discord ID.')
async def lookup(interaction: nextcord.Interaction,
    discord_id: int = SlashOption(description='Discord ID', required=True)
):
    for member in interaction.guild.members:
        if str(member.id).startswith(str(discord_id)):
            return await embedder.ok(interaction, f'Result: {member.mention} (`{member.id}`)')

async def get_member_song_line(member):
    if member.activity and member.activity.type == nextcord.ActivityType.listening:
        album = ''
        if member.activity.title != member.activity.album:
            album = f'({member.activity.album})'

        return f'{member.mention}: [{member.activity.artist.replace(";", ",")} - **{member.activity.title}** {album}]({member.activity.track_url})\n'
    return ''

@bot.slash_command(description='See what others in this Discord are listening right now.')
async def music(interaction: nextcord.Interaction):
    text = ''

    for member in interaction.guild.members:
        text += await get_member_song_line(member)

    if text:
        return await embedder.ok(interaction, text)
    return await embedder.error(interaction, 'No one is listening to anything right now.')

# update the message in #music every 10 seconds to show what people are listening to
@bot.event
async def on_ready():
    print(f'Online as {bot.user} (ID: {bot.user.id})')

    await api.start(bot)
    await bot.change_presence(activity=nextcord.Game(name='with fire'))

    while True:
        text = ''
        channel = bot.get_channel(int(os.getenv('DISCORD_MUSIC_CHANNEL_ID')))

        if channel:
            async for message in channel.history(limit=1):
                if message.author == bot.user:
                    for member in channel.guild.members:
                        text += await get_member_song_line(member)

                    if text:
                        await message.edit(embed=nextcord.Embed(
                            title='What are people listening to right now?',
                            description=text,
                            color=nextcord.Color.green()
                        ))
                    else:
                        await message.edit(embed=nextcord.Embed(
                            title='What are people listening to right now?',
                            description='No one is listening to anything right now :(',
                            color=nextcord.Color.red()
                        ))

        await nextcord.utils.sleep_until(nextcord.utils.utcnow().replace(second=0, microsecond=0) + datetime.timedelta(seconds=10))

bot.run(os.getenv('DISCORD_TOKEN'))
