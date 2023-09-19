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

    if ('N0V4x0SS' in text and 'nv-' in text) or ('T3BlbkFJ' in text and 'sk-' in text):
        censored_text = ''

        for word in text.split():
            if 'N0V4x0SS' in word or 'T3BlbkFJ' in word:
                censored_text += '❚' * len(word)
            else:
                censored_text += word
            censored_text += ' '

        await embedder.warn(message, f"""{message.author.mention},
I think you sent an *OpenAI* or *NovaAI* key in here.
This could lead to other users accessing and abusing your API account without your knowledge.
Be very careful with API credentials!""", content=f'||{message.author.mention} sent (censored version):\n```{censored_text}```||', delete_after=60)
        await message.delete()

    commands_allowed = 'commands' in message.channel.name or 'bot' in message.channel.name

    if text.startswith('/') and text.count(' ') <= 2:
        # COMMANDS: WRONG CHANNEL
        if not commands_allowed:
            await embedder.error(message, f'{message.author.mention}, please __only__ run commands in <#1133103276871667722>.', delete_after=10)
            await message.delete()
            return

        # COMMANDS: NOT RAN CORRECTLY
        if len(text) > 2:
            await embedder.warn(message, """Need help running commands? Check out
**https://nova-oss.com/novacord** or run `/tutorial`!""", delete_after=10)
            await message.delete()
            return

    if 'dQw4w9WgXcQ' in text:
        await embedder.warn(message, """Hide your rickrolls better next time...""", delete_after=10)
        await message.delete()
        return
