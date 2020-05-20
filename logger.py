import os, re
from datetime import datetime

log_dir = 'logs'

def make_log_dir(guild_log_dir:str):
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    if not os.path.exists(guild_log_dir):
        os.mkdir(guild_log_dir)


async def log_command(ctx, command=str, *args):
    guild_name = re.sub(r'[\W]', '', ctx.guild.name)
    guild_id = str(ctx.guild.id)
    guild_log_dir = os.path.join(log_dir, guild_id)
    
    make_log_dir(guild_log_dir)

    log_file = os.path.join(guild_log_dir, f'COMMANDS_{guild_name}.txt')
    mode = 'a' if os.path.exists(log_file) else 'w'
    with open(log_file, mode) as f:
        f.writelines(f'COMMAND:{ctx.author.name}#{ctx.author.id}, "{command}", {args} - ({datetime.now()})\n')


async def log_error(ctx, error):
    guild_name = re.sub(r'[\W]', '', ctx.guild.name)
    guild_id = str(ctx.guild.id)
    guild_log_dir = os.path.join(log_dir, guild_id)
    
    make_log_dir(guild_log_dir)

    log_file = os.path.join(guild_log_dir, f'ERRORS_{guild_name}.txt')
    mode = 'a' if os.path.exists(log_file) else 'w'
    with open(log_file, mode) as f:
        f.writelines(f'ERROR:{ctx.author.name}#{ctx.author.id}, {error} - ({datetime.now()})\n')