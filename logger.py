import os, re
from datetime import datetime

log_dir = 'logs'

async def make_log_dir(guild_log_dir:str):
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    if not os.path.exists(guild_log_dir):
        os.mkdir(guild_log_dir)


async def log_command(ctx, command=str, *args):
    return
    dir_path = os.path.join(log_dir, str(ctx.guild.id))
    guild_name = re.sub(r'[\W]', '', ctx.guild.name)
    file_path = os.path.join(dir_path, f'COMMANDS_{guild_name}.txt')
    msg = f'COMMAND:{ctx.author.name}#{ctx.author.id}, "{command}", {args} - ({datetime.now()})\n'
    await log(dir_path, file_path, msg)


async def log_error(ctx, error):
    return
    dir_path = os.path.join(log_dir, str(ctx.guild.id))
    guild_name = re.sub(r'[\W]', '', ctx.guild.name)
    file_path = os.path.join(dir_path, f'ERRORS_{guild_name}.txt')
    msg = f'ERROR:{ctx.author.name}#{ctx.author.id}, {error} - ({datetime.now()})\n'
    await log(dir_path, file_path, msg)


async def log(dir_path, file_path, msg):
    return
    make_log_dir(dir_path)
    mode = 'a' if os.path.exists(file_path) else 'w'
    with open(file_path, mode) as f:
        f.writelines(msg)