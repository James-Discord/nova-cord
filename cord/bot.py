# This example requires the 'members' and 'message_content' privileged intents to function.

import os
import asyncio
import nextcord
import requests

import keys
import chatbot
import embedder

from dotenv import load_dotenv
from nextcord.ext import commands
from nextcord import SlashOption

load_dotenv()

bot = commands.Bot(
    intents=nextcord.Intents.all(),
    default_guild_ids=[int(guild_id) for guild_id in os.getenv('DISCORD_GUILD_IDS').split()]
)

@bot.event
async def on_ready():
    print(f'Online as {bot.user} (ID: {bot.user.id})')
    await bot.change_presence(activity=nextcord.Game(name='with fire'))

@bot.event
async def on_message(message):
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
        await embedder.error(interaction, text='Please open this server\'s options, go to `Privacy Settings` and enable `Direct Messages` and `Message Requests`.')
    else:     
        await embedder.ok(interaction, 'Great, DMs are set up successfully!')

@bot.slash_command(description='Get your secret NovaAI API key.')
async def key(interaction: nextcord.Interaction):
    try:
        resp = requests.post(
            url='https://nova-oss.com/api/tos-verification',
            timeout=5,
            headers={'Content-Type': 'application/json', 'Authorization': os.getenv('TOS_VERIFICATION_KEY')}
        ).json()
    except Exception as exc:
        await embedder.error(interaction, """Sorry, the API server for the verification system is not functioning,
which means you can\'t create a new key right now. Please report this issue to the staff!""")
        raise exc

    tos_code = resp['code']
    tos_emoji = resp['emoji']

    tos_message = await embedder.warn(interaction, f"""# THIS IS JUST A DEMO!
# THE KEY DOESN'T WORK!
You have to read the privacy policy and terms of service first.
In the latter, there is a hidden emoji which you'll have to send (NOT react!) in here.

https://nova-oss.com/legal/privacy
https://nova-oss.com/legal/terms?verify={tos_code}

I know it's annoying, but it really helps combat spam bots and abuse.

This message will be deleted and your code will run out **after about 10 minutes**
if you don't pass the verification, but **feel free to run this command again** at any time.
""", ephemeral=True)

    def check(message): return interaction.user.id == message.author.id and message.content == tos_emoji

    try:
        answer = await bot.wait_for('message', timeout=666, check=check)
    except asyncio.TimeoutError:
        await tos_message.delete()
        requests.delete(
            url=f'https://nova-oss.com/api/tos-verification/{tos_code}',
            timeout=5,
            headers={'Content-Type': 'application/json', 'Authorization': os.getenv('TOS_VERIFICATION_KEY')}
        )

    else:
        await answer.delete()
        api_key = await keys.create(interaction.user)
        await embedder.ok(interaction, f"""This is your **secret** API key. Don't paste it on untrusted websites, apps or programs.
Store it securely using a `.env` file in the environment variables or use a secure password manager like *KeePass*, *ProtonPass* or *Bitwarden*.
We reserve the right to __disable your API key at any time__ if you violate our terms of service.
If you accept the terms of service and privacy policy, feel free to use the following API key:

## ||`{api_key}`||

""", ephemeral=True)

bot.run(os.getenv('DISCORD_TOKEN'))
