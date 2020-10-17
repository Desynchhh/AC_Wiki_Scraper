import discord

def is_bot_owner(ctx:discord.ext.commands.Context) -> bool:
    """Check if the context is sent by the bot owner.

    :type ctx: discord.ext.commands.Context
    :rtype: bool
    """
    return ctx.author.id == 228179496807694336

def is_owner(ctx:discord.ext.commands.Context) -> bool:
    """Check if the context is sent by the server owner.

    :type ctx: discord.ext.commands.Context
    :rtype: bool
    """
    return ctx.message.author.id == ctx.message.guild.owner_id
