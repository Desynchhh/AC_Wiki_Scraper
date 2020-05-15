import logging, os, re
from datetime import datetime

log_dir = 'logs'

def check_log_dir_exists():
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)


async def log_command(ctx, command=str, *args):
    check_log_dir_exists()
    guild_name = re.sub(r'[\W]', '', ctx.guild.name)
    logging.basicConfig(filename=f"{log_dir}/{guild_name}{ctx.guild.id}.log", level=logging.INFO)
    logging.info(f"{ctx.author.name}#{ctx.author.id} used command '{command}' with arguments {args} ({datetime.now()})")

async def log_error(ctx, error):
    check_log_dir_exists()
    guild_name = re.sub(r'[\W]', '', ctx.guild.name)
    logging.basicConfig(filename=f"{log_dir}/{guild_name}{ctx.guild.id}.log", level=logging.DEBUG)
    logging.exception(f"{ctx.author.name}#{ctx.author.id} {error} ({datetime.now()})")