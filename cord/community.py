import asyncio
import datetime

import embedder

async def process_channel(channel, scores):
    if channel.name in ['general', 'support', 'suggestions', 'showcase', 'team-discussion', 'prompts', 'research-resources']:
        after = datetime.datetime.now() - datetime.timedelta(days=7)

        async for message in channel.history(limit=1000, after=after):
            if not '```' in message.content: # no code
                if not scores.get(message.author.id):
                    scores[message.author.id] = 0

                scores[message.author.id] += message.content.strip().count(' ')

async def leaderboard(interaction):
    msg = await interaction.send('Loading the leaderboard... Go grab a mug of bleach.. ||**[for legal reasons that a joke]**|| \nhttps://media.tenor.com/M67VmLlocdMAAAAS/spinning-seal.gif')

    scores = {}

    channels = interaction.guild.text_channels
    tasks = [process_channel(channel, scores) for channel in channels] # go fast like sonik by doing splitting it into tasks
    await asyncio.gather(*tasks)

    board = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]) # sort dict by value and get only first 10

    emojis = [':first_place:', ':second_place:', ':third_place:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':keycap_ten:']

    text = 'Words (excluding code) typed in selected channels in the last 7 days with a limit of 1000 messages per channel:\n'
    place = 0

    for user in list(board.keys()):
        text += f'{emojis[place]} {interaction.guild.get_member(user).mention} **{scores[user]}**\n'
        place += 1

    await embedder.info(msg, title='Leaderboard (7 days)', text=text)
