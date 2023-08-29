"""Account system functionality."""

import os
import requests

import embedder
import accounts
import tos_verification

from dotenv import load_dotenv

load_dotenv()

async def get_credentials(interaction):
    for _ in range(2):
        try:
            get_response = await accounts.request_user_by_discord_id(interaction.user.id)
        except Exception as exc:
            await embedder.error(interaction, """Sorry,\n" \
there was an issue while checking if you already have an account.
Please report this issue to the staff!""", ephemeral=True)
            raise exc

        if get_response.status_code == 200: # user exists
            break

        # NEW USER
        read_tos = await tos_verification.verify(interaction)

        if not read_tos:
            await interaction.delete_original_message()
            return

        # CREATE USER
        get_response = requests.post(
            url='http://localhost:2333/users',
            timeout=3,
            headers={
                'Content-Type': 'application/json',
                'Authorization': os.getenv('CORE_API_KEY')
            },
            json={
                'discord_id': str(interaction.user.id)
            }
        )

        try:
            get_response.raise_for_status()

        except Exception as exc:
            await embedder.error(interaction, """Sorry,
your account could not be created. Please report this issue to the staff!""", ephemeral=True)

            raise exc

        else:
            await embedder.ok(interaction, f"""Welcome to NovaAI, {interaction.user.mention}!
Your account was created successfully.""", ephemeral=True)

    api_key = get_response.json()['api_key']

    await embedder.info(interaction, f"""This is your **secret** API key.
Don't paste it on untrusted websites, apps or programs.
Store it securely using a `.env` file in the environment variables
or use a secure password manager like *KeePass*, *ProtonPass* or *Bitwarden*.
We reserve the right to __disable your API key at any time__ if you violate our terms of service.
If you accept the terms of service and privacy policy, feel free to use the following API key:

## ||`{api_key}`||
(Don't see anything? Click the empty space above to reveal it.)

Learn more about how to use our API at **https://nova-oss.com**.
""", ephemeral=True)
