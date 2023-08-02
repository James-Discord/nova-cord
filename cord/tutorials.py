import embedder

async def send(interaction, how_can_i):
    if how_can_i == 'fix ModuleNotFoundErrors':
        text = """You can install Python packages using `pip`. Here's an example: `pip install openai`.
Don't have `pip` installed? Learn more here: https://pip.pypa.io/en/stable/installation/.
"""

    if how_can_i == 'use the Python library':
        text = """For the official `openai` Python library, you just need to set the `openai.api_base` to `https://api.nova-oss.com/v1`.
```py
import openai

openai.api_key = "PUT_YOUR_NOVA_AI_API_KEY_IN_HERE"
openai.api_base = "https://api.nova-oss.com/v1"

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
)

print(completion.choices[0].message)
```
"""

    if how_can_i == 'use curl':
        text = """For curl, just follow the official OpenAI documentation: https://platform.openai.com/docs/api-reference/chat/create?lang=curl
And replace ~~`openai.com`~~ with **`nova-oss.com`**. Here's an example:

```bash
curl https://api.nova-oss.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer PUT_YOUR_NOVA_AI_API_KEY_IN_HERE" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {
        "role": "user",
        "content": "1+1"
      }
    ]
  }'
```
"""

    if how_can_i == 'use Node.js':        
        text = """Currently, the official node.js `openai` package doesn't support custom endpoints in their stable version,
but will probably change after the release of v4.0.0: https://github.com/openai/openai-node/discussions/182#discussioncomment-6335703.
Meanwhile, you can just do "normal" requests like in curl without any package.
"""

    if how_can_i == 'program a Python Discord Bot with streaming':
        text = """I'm assuming you know how to run Discord bots in Python and have already set up a bot.
And if not - there are tons of tutorials out there on the internet on how to do that.

**Warning:** I'm using *Nextcord* as my package of choice for programming Discord bots, because it worked the best for me.
If you get an error saying that Nextcord isn't compatible with another package,
simply uninstall it using a command like `pip uninstall discord.py`. 

Anyways, make sure you have all packages you need installed:
`pip install openai python-dotenv nextcord`.

We don't want our code to contain the secret API key and Discord bot token.
So create a `.env` file with the following content (obviously replace the values with the actual ones appropriately).:

```
NOVA_KEY=PUT_YOUR_NOVA_API_KEY_HERE
DISCORD_TOKEN=PUT_YOUR_DISCORD_BOT_TOKEN_HERE
```

And you should be good to go!

```py
import os
import openai
import nextcord

from dotenv import load_dotenv

load_dotenv() # reads our secret of our .env file and makes them accessible using os.getenv()

# add a new command
@bot.slash_command(description='Chat with AI')
async def chat(interaction: nextcord.Interaction,
    # this makes it so people can enter their prompt when using the slash command
    prompt: str = SlashOption(description='Chatbot Prompt', required=True)
):
    partial_message = await interaction.send('‎') # just writes an empty message
    message = await partial_message.fetch() # prepares this message to be used 

    # set the configuration for the AI access
    openai.api_base = 'https://api.nova-oss.com/v1'
    openai.api_key = os.getenv('NOVA_KEY')

    async with interaction.channel.typing(): # so Discord displays the "[Bot name] is typing..." at the bottom 
        try:
            completion = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[{'role': 'user', 'content': prompt}],
                stream=True # this is really important to get the streaming (realtime updates) to work
            )
            # from now on, we will get new completions in the background which are saved in the completion variable	
        except Exception as exc:
            await interaction.send(':x: Error - could not generate an AI response. Look in the console.')
            raise exc # so the error shows up in the console

        # we want to save the text that was generated using the AI
        text = ''

        for event in completion: # loop through word generation in real time
            try:
                new_text = event['choices'][0]['delta']['content'] # add the newly generated word to the variable
            except KeyError: # end or an error occured
                break # stop the loop

            text += new_text # ad the new word to the complete text variable

            if text: # we get errors if the new text we're editing the message to is empty
                await message.edit(content=text) # finally edit the message to include the entire new text

    # put any code in here if you want anything to happen when the AI is done with the completion

# starts the Discord bot
bot.run(os.getenv('DISCORD_TOKEN'))
```
"""
    return await embedder.info(interaction, text)
