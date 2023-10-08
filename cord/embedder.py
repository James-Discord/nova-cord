import nextcord

from typing import Union

async def send(
    ctx,
    title: str,
    text: str,
    content: str = '',
    ephemeral: bool = False,
    color: nextcord.Color = nextcord.Color.blue(),
    **kwargs
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

    embed.set_footer(text='Powered by Nova with ❤️', icon_url='https://i.ibb.co/LDyFcSh/fav-blurple.png')
    embed.set_author(name='NovaCord', url='https://nova-oss.com/novacord')

    interaction_type = Union[nextcord.Interaction, nextcord.InteractionResponse]

    # these checks are done so this function is easy to use
    if edit:
        return await ctx.edit(embed=embed, content=content, **kwargs)

    if isinstance(ctx, nextcord.Message):
        response = await ctx.reply(embed=embed, content=content, **kwargs)

    elif isinstance(ctx, interaction_type):
        response = await ctx.send(embed=embed, ephemeral=ephemeral, content=content, **kwargs)

    else:
        response = await ctx.send(embed=embed, content=content, **kwargs)

    return response

async def ok(ctx, text: str, title: str=':white_check_mark: Success', *args, **kwargs):
    return await send(ctx, title, text, color=nextcord.Color.green(), *args, **kwargs)

async def info(ctx, text: str, title: str=':information_source: Information', *args, **kwargs):
    return await send(ctx, title, text, color=nextcord.Color.blue(), *args, **kwargs)

async def warn(ctx, text: str, title: str=':warning: Warning', *args, **kwargs):
    return await send(ctx, title, text, color=nextcord.Color.orange(), *args, **kwargs)

async def error(ctx, text: str, title: str=':x: Error - Command Failed', *args, **kwargs):
    return await send(ctx, title, text, color=nextcord.Color.red(), *args, **kwargs)
