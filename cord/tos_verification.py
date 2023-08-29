"""The module for the Terms of Service verification system."""

import os
import asyncio
import requests

import embedder

from dotenv import load_dotenv

load_dotenv()

async def verify(interaction) -> bool:
    try:
        resp = requests.post(
            url='http://localhost:2323/api/tos-verification',
            timeout=5,
            headers={
                'Content-Type': 'application/json',
                'Authorization': os.getenv('TOS_VERIFICATION_KEY')
            }
        ).json()
    except Exception as exc:
        await embedder.error(interaction, f"""Sorry,
the API server for the verification system is not functioning,
which means you can\'t create a new key right now. Please report this issue to the staff:

```{type(exc)} - {exc}```
""")
        raise exc

    success = False
    tos_code = resp['code']
    tos_emoji = resp['emoji']

    tos_message = await embedder.warn(interaction, f"""
You have to read the privacy policy and terms of service first.
In the latter, there is a hidden emoji which you'll have to __send__ (NOT react!) in here.

https://nova-oss.com/legal/privacy?verify={tos_code}
https://nova-oss.com/legal/terms?verify={tos_code}

I know it's annoying, but it really helps combat spam bots and abuse.

This message will be deleted and your code will run out **after 10 minutes**
if you don't pass the verification, but **feel free to run this command again** at any time.
""", ephemeral=True)

    def check(message):
        correct_user = interaction.user.id == message.author.id
        return correct_user and message.content == tos_emoji

    try:
        while True:
            received_answer = await interaction.client.wait_for('message', timeout=600, check=check)
            await received_answer.delete()

            if received_answer.content == tos_emoji:
                break

    except asyncio.TimeoutError:
        await tos_message.delete()

    else:
        success = True

    finally:
        await tos_message.delete()
        requests.delete(
            url=f'https://nova-oss.com/api/tos-verification/{tos_code}',
            timeout=5,
            headers={
                'Content-Type': 'application/json',
                'Authorization': os.getenv('TOS_VERIFICATION_KEY')
            }
        )

    return success
