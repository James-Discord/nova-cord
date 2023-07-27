import os
import asyncio
import requests

import keys
import embedder

from dotenv import load_dotenv

load_dotenv()

async def get_credentials(interaction):
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

    tos_message = await embedder.warn(interaction, f"""# THIS IS JUST A DEMO/EXAMPLE!
# THE KEY WON'T WORK!
# THE SYSTEM ISN'T READY YET.
# DON'T SAVE THE KEY!!!
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
        answer = await interaction.client.wait_for('message', timeout=666, check=check)
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
