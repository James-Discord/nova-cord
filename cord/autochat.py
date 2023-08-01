import embedder
from nextcord import DMChannel

async def process(message):
    text = message.content

    # IGNORE BOTS
    if message.author.bot:
        return

    # IGNORE DM CHANNELS
    if isinstance(message.channel, DMChannel):
        return

    if 'N0V4x0SS' in text or 'T3BlbkFJ' in text:
        await embedder.warn(message, f'{message.author.mention}, I think you sent an *OpenAI* or *NovaAI* key in here, which could lead to other users accessing your API account without your knowledge. Be very careful with API credentials!', delete_after=15)
        await message.delete()

    # COMMANDS: WRONG CHANNEL
    commands_allowed = ('commands' in message.channel.name) or (message.author.guild_permissions.manage_messages)

    if text.startswith('/') and not commands_allowed:
        await embedder.error(message, f'{message.author.mention}, plesae __only__ run commands in <#1133103276871667722>.', delete_after=10)
        await message.delete()
        return

    # COMMANDS: NOT RAN CORRECTLY
    if text.startswith('/') and len(text) > 2:
        await embedder.warn(message, """Need help running commands? Check out
**https://nova-oss.com/novacord**!""", delete_after=10)
        return
