import nextcord
import traceback

from typing import Union

async def send(
    ctx,
    title: str,
    text: str,
    ephemeral: bool = False,
    color: nextcord.Color = nextcord.Color.blue()
):
    embed = nextcord.Embed(
        title=title,
        description=text,
        color=color
    )
    embed.set_footer(text='Powered by NovaAI', icon_url='https://i.ibb.co/LDyFcSh/fav-blurple.png')
    embed.set_author(name='NovaCord', url='https://nova-oss.com/novacord')

    if isinstance(ctx, nextcord.Message):
        response = await ctx.reply(embed=embed)
    elif isinstance(ctx, Union[nextcord.Interaction, nextcord.InteractionResponse]):
        response = await ctx.send(embed=embed, ephemeral=ephemeral)
    else:
        response = await ctx.send(embed=embed)

    return response

async def ok(ctx, text: str, title: str='Success', *args, **kwargs):
    return await send(ctx, title, text, color=nextcord.Color.green(), *args, **kwargs)

async def info(ctx, text: str, title: str='Information', *args, **kwargs):
    return await send(ctx, title, text, color=nextcord.Color.blue(), *args, **kwargs)

async def warn(ctx, text: str, title: str='Warning', *args, **kwargs):
    return await send(ctx, title, text, color=nextcord.Color.orange(), *args, **kwargs)

async def error(ctx, text: str, title: str='Error - Command Failed', *args, **kwargs):
    return await send(ctx, title, text, color=nextcord.Color.red(), *args, **kwargs)
