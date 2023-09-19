import os
import aiohttp.web

from dotenv import load_dotenv

load_dotenv()

app = aiohttp.web.Application()

async def start(client):
    async def get_userinfo():
        guild = client.get_guild(int(os.getenv('DISCORD_GUILD')))
        members = guild.members

        user_roles = {member.id: [role.name for role in member.roles] for member in members}
        return user_roles

    app.router.add_get('/get_roles', lambda request: aiohttp.web.json_response(get_userinfo()))
    app.router.add_get('/user_ids', lambda request: aiohttp.web.json_response([member.id for member in client.get_guild(int(os.getenv('DISCORD_GUILD'))).members]))
    app.router.add_get('/ping', lambda request: aiohttp.web.Response(text='pong'))

    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner, '0.0.0.0', 3224)
    await site.start()
