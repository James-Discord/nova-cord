import random
import embedder

async def process(message):
    if message.content == '/key':
        responses = [
            'https://media.tenor.com/t9f91LQWsM4AAAAS/breaking-bad-funny.gif',
            'NPC detected, command rejected.',
            'https://images-ext-1.discordapp.net/external/DXc3r4PyRR3m_4AzevpxWhfFtavdcMeDpZqFj3Ig4hc/https/media.tenor.com/b7swbvaVKhUAAAPo/seriously-laugh.mp4',
            'there👏is👏no👏/key👏command👏',
            'https://i.imgflip.com/7tuhc6.jpg'
        ]

        await message.reply(random.choice(responses))
        await message.channel.send('Jokes aside - the project is still under development. There\'s no **`/key`** command.')

    if message.content.startswith('/') and ('commands' not in message.channel.name) and (not message.author.guild_permissions.manage_messages):
        await embedder.warn(message, 'Please only run commands in `/commands`.')
