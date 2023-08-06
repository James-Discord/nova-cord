import os
import openai

import embedder

from dotenv import load_dotenv

load_dotenv()

async def respond(interaction, prompt):
    partial_message = await interaction.send('‎') # send an empty message
    message = await partial_message.fetch() # gets the message that was send

    openai.api_base = os.getenv('OPENAI_BASE')
    openai.api_key = os.getenv('OPENAI_KEY')

    model = os.getenv('OPENAI_MODEL')

    async with interaction.channel.typing(): # show the "Typing..."
        try:
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
        except Exception as exc:
            await embedder.error(interaction, 'Could not generate an AI response.', ephemeral=True)
            raise exc

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


