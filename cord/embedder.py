import nextcord
import datetime

from typing import Union

async def send(
    ctx,
    title: str,
    text: str,
    content: str = '',
    ephemeral: bool = False,
    color: nextcord.Color = nextcord.Color.blue()
):
    edit = False    

    if isinstance(ctx, nextcord.PartialInteractionMessage):
        ctx = await ctx.fetch()
        edit = True

    embed = nextcord.Embed(
        title=title,
        description=text,
        color=color
    )

    time_difference = datetime.datetime.now(datetime.timezone.utc) - ctx.created_at
    milliseconds = int(time_difference.total_seconds() * 1000)

    end = ''

    if milliseconds > 10000: # https://youtu.be/-5wpm-gesOY
        end = f' in {milliseconds}ms'

    embed.set_footer(text=f'Powered by NovaAI{end}', icon_url='https://i.ibb.co/LDyFcSh/fav-blurple.png')
    embed.set_author(name='NovaCord', url='https://nova-oss.com/novacord')

    interaction_type = Union[nextcord.Interaction, nextcord.InteractionResponse]

    # these checks are done so this function is easy as fuck to use

    if edit:
        return await ctx.edit(embed=embed, content=content)

    if isinstance(ctx, nextcord.Message):
        response = await ctx.reply(embed=embed, content=content)

    elif isinstance(ctx, interaction_type):
        response = await ctx.send(embed=embed, ephemeral=ephemeral, content=content)

    else:
        response = await ctx.send(embed=embed, content=content)

    return response

async def ok(ctx, text: str, title: str=':white_check_mark: Success', *args, **kwargs):
    return await send(ctx, title, text, color=nextcord.Color.green(), *args, **kwargs)

async def info(ctx, text: str, title: str=':information_source: Information', *args, **kwargs):
    return await send(ctx, title, text, color=nextcord.Color.blue(), *args, **kwargs)

async def warn(ctx, text: str, title: str=':warning: Warning', *args, **kwargs):
    return await send(ctx, title, text, color=nextcord.Color.orange(), *args, **kwargs)

async def error(ctx, text: str, title: str=':x: Error - Command Failed', *args, **kwargs):
    return await send(ctx, title, text, color=nextcord.Color.red(), *args, **kwargs)
