import embedder

async def send(interaction, how_can_i):
    if how_can_i == 'fix error 429 (ratelimit/not enough credits)':
        text = """This means you used the API too often. You can either wait a bit or try to get more credits.
If you try to bypass this, all your accounts and IP addresses may get banned.
"""

    if how_can_i == 'fix error 401 (invalid key)':
        text = """Make sure you entered your NovaAI API key (starting with `nv-`) correctly.
For HTTP requests, it can be specified using a header:
```
Authorization: Bearer nv-...
```
"""

    if how_can_i == 'use the API in custom front-ends':
        text = """Depending on the front end, the endpoints might differ a bit:

**ChatGPT Next Web**
(https://chat-gpt-next-web.vercel.app/):
`https://api.nova-oss.com`

Code: https://github.com/Yidadaa/ChatGPT-Next-Web

**Better ChatGPT**
(https://chat.resisto.rodeo/, https://chatgpt1.nextweb.fun/, https://freechatgpt.chat/, https://bettergpt.chat/):
`https://api.nova-oss.com/v1/chat/completions`

Code: https://github.com/ztjhz/BetterChatGPT

**ai.ls**
(https://ai.ls, https://chatsverse.xyz/):
`https://api.nova-oss.com`

*Warning - __not__ open source!*

Don't forget to also set the correct model and API key!

**Warning:** in theory, these front-ends could __steal your NovaAI key__.
Self-host them if you know how to.

**__Official front-end__**
:point_right: https://chat.nova-oss.com

"""

    if how_can_i == 'get my NovaAI API key':
        text = """Open up the **`#commands`** channel and run **`/credentials`**.
Then, follow the instructions carefully.

Fore more information: https://nova-oss.com/novacord
"""

    if how_can_i == 'see my available credits':
        text = """Open up the **`#commands`** channel and run **`/credits`**."""

    if how_can_i == 'fix ModuleNotFoundErrors':
        text = """You can install Python packages using the terminal command `pip`.
Here's an example: `pip install openai`.
Don't have `pip` installed? Learn more here: https://pip.pypa.io/en/stable/installation/.
"""

    if how_can_i == 'use the Python library':
        text = """To use the official `openai` Python library, you just need to do the following.
```py
# Import the OpenAI library (assuming it's already installed)
import openai

# Set the OpenAI API key
openai.api_key = "NOVA_AI_KEY"

# Set the OpenAI API base URL
openai.api_base = "https://api.nova-oss.com/v1/"

# Create a chat completion using the gpt-3.5-turbo model and the user and system messages
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the highest mountain?"}
    ]
)

# Extract and print the content of the model's response
response_content = completion.choices[0].message.content
print(response_content)
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
        text = """
```js
const OpenAI = require('openai');

const openai = new OpenAI({
  apiKey: 'PUT_YOUR_NOVA_API_KEY_HERE', 
  baseURL: 'https://api.nova-oss.com/v1/',
});

async function main() {
  const completion = await openai.chat.completions.create({
    messages: [
      { role: 'system', content: 'You are a helpful assistant.' },
      { role: 'user', content: 'What is the highest mountain?' }
    ],
    model: 'gpt-3.5-turbo',
  });
  
  console.log(completion.choices);
}

main();
```
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
    return await embedder.info(interaction, title=f'Tutorial: "{how_can_i}"', text=text)
