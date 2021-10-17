import discord
from discord.ext import commands
from asyncio import sleep, TimeoutError
import asyncio

class errpack:
    def __init__(self, command, answer):
        self.command = command
        self.answer = answer

def getanswer(inputcommand):
    for obj in answlist:
        if inputcommand == obj.command:
            return obj.answer

answlist = [errpack('kick', '```Укажите кого кикнуть! → %kick @someone```'),
            errpack('ban', '```Укажите кого забанить! → %ban @someone```'),
            errpack('unban', ''),
            errpack('twink', '```Укажите кто твинк! → %twink @someone```'),
            errpack('assign', '```Укажите кого нанять! → %assign @someone```'),
            errpack('move', '```Укажите кого мувнуть! → %move @someone```'),
            errpack('mute', '```Укажите кого замутить! → %mute @someone```'),
            errpack('unmute', '```Укажите кого размутить! → %unmute @someone```'),
            errpack('deafen', '```Укажите кого заглушить! → %deafen @someone```'),
            errpack('undeafen', '```Укажите кого разглушить! → %undeafen @someone```'),
            errpack('disconnect', '```Укажите кого выкинуть из войса! → %disconnect @someone```'),
            errpack('wake', '```Пользователь вышел из войсчата```'),
            errpack('ping', '```Укажите кого пингануть! → %ping @someone```'),
            errpack('suck', '```Укажите кому отсосать!🥴 → %suck @someone```'),
            errpack('jail', '```Укажите кого заключить! → %jail @someone```'),
            errpack('test', '```Укажите над кем протестировать! → %test @someone```'),
            errpack('play', '```Укажите что сыграть! → %play [ ссылка или поисковой запрос ]```'),
            errpack('loop', ''),
            errpack('skip', ''),
            errpack('queue', ''),
            errpack('stop', '')]

async def handle(ctx, error, reason):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send('```Команда на кулдауне, будет доступна через {:.0f} секунд```'.format(error.retry_after))
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send(getanswer(reason))
        print("{0}: {1}".format(reason,error))
    elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        if getanswer(reason)=='':
            pass
        else:
            await ctx.send(getanswer(reason))
            print("{0}: {1}".format(reason, error))
    elif isinstance(error, discord.ext.commands.errors.ClientException):
        if getanswer(reason)=='':
            pass
        else:
            await ctx.send(getanswer(reason))
            print("{0}: {1}".format(reason, error))
    else:
        raise error
