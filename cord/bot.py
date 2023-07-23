# This example requires the 'members' and 'message_content' privileged intents to function.

import os
import openai
import nextcord

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
    partial_message = await interaction.send('‎') # empty message
    message = await partial_message.fetch()

    openai.api_base = os.getenv('OPENAI_BASE', 'https://api.openai.com/v1')
    openai.api_key = os.getenv('OPENAI_KEY')

    model = os.getenv('OPENAI_MODEL')

    async with interaction.channel.typing(): # show the "Typing..."
        completion = openai.ChatCompletion.create(
            model=model,
            messages=[
                {'role': 'system', 'content': f"""You are a helpful Discord AI bot based on OpenAI\'s {model} model called "Nova".
You were developed by NovaAI (website: nova-oss.com) in July of 2023, but your knowledge is limited to mid-2021.
Respond using Markdown. Keep things simple and short and directly do what the user says without any fluff.
For programming code, always make use formatted code blocks like this:
```py
print("Hello")
```
"""},
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.6,
            stream=True
        )

        text = ''

        for event in completion: # loop through word generation in real time
            try:
                new_text = event['choices'][0]['delta']['content'] # newly generated word
            except KeyError: # end
                break

            text += new_text

            if text:
                await message.edit(content=text)

    await message.add_reaction('✅')

bot.run(os.getenv('DISCORD_TOKEN'))
