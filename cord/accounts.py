"""Account system functionality."""

import os
import json
import requests

import embedder

from dotenv import load_dotenv

load_dotenv()

async def request_user_by_discord_id(discord_id):
    return requests.get(
        url=f'https://api.nova-oss.com/users?discord_id={discord_id}',
        timeout=3,
        headers={
            'Content-Type': 'application/json',
            'Authorization': os.getenv('CORE_API_KEY')
        }
    )

async def get_account(interaction):
    try:
        user_response = await request_user_by_discord_id(interaction.user.id)

    except Exception as exc:
        await embedder.error(interaction, """Sorry, there was an error while checking if you have an account.
Please report this issue to the staff!""", ephemeral=True)
        raise exc

    if user_response.status_code == 404:
        await embedder.error(interaction, """You don't have an account yet!""", ephemeral=True)
        return

    return user_response.json()

async def get_info(interaction):
    account = await get_account(interaction)

    await embedder.info(interaction, f"""### Your account
This is all we have stored about your API account in our database.
Feel free to request a removal of your account by contacting the staff.

||```json
{json.dumps(account, indent=4)}
```||
(Click to reveal)

Learn more about how to use our API at **https://nova-oss.com**.
""", ephemeral=True)

async def get_credits(interaction):
    account = await get_account(interaction)
    amount_credits = account["credits"]

    await embedder.info(interaction, f"""### Your credits
Amount: **{amount_credits if amount_credits < 1000000 else '∞'}**
""", ephemeral=True)

async def get_credits_of(interaction, user):
    if not interaction.user.guild_permissions.administrator:
        await embedder.error(interaction, """Sorry, you don't have the permission to do that.""", ephemeral=True)
        return

    try:
        userinfo = await request_user_by_discord_id(user.id)

    except Exception as exc:
        await embedder.error(interaction, """Sorry, there was an error while checking if you have an account.
Please report this issue to the staff!""", ephemeral=True)
        raise exc

    if userinfo.status_code == 404:
        await embedder.error(interaction, """You don't have an account yet!""", ephemeral=True)
        return

    account = userinfo.json()
    amount_credits = account["credits"]

    await embedder.info(interaction, f"""### Credits of {user.name}
Amount: **{amount_credits if amount_credits < 1000000 else '∞'}**
""", ephemeral=True)
