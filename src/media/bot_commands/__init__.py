from inspect import *
from src.media.bot_commands import bot_commands

commands_list = []

for i in getmembers(bot_commands):
    if all([not i[0].startswith('__'), not i[0].startswith('command'), i[0].islower()]):
        commands_list.append(i[1])
