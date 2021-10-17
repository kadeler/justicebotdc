import discord
from time import time
from asyncio import sleep, TimeoutError
from discord.ext import commands
import youtube_dl
import asyncio
import os

client = commands.Bot(command_prefix='%', help_command=None)


async def getid(userat):
    idv = userat
    idv = idv.replace("<", "")
    idv = idv.replace("@", "")
    idv = idv.replace("!", "")
    idv = idv.replace(">", "")
    return idv


#locallibs
from poll import pollcreate
import music
import other
import error_handler


@client.event
async def on_ready():
    print('Вошел как {0}#{1}!'.format(client.user.name, client.user.discriminator))
    # print('Включить чат?')
    # inp = input()
    # if inp=='y':
    #    while True:
    #        bop = input("")
    #        for guild in client.guilds:
    #            for channel in client.get_all_channels():
    #                if channel.name == "📢𝑮̲̅𝑬̲̅𝑵̲̅𝑬̲̅𝑹̲̅𝑨̲̅𝑳̲̅📢":
    #                    await channel.send(bop)
    # else:
    #    inp

# administering

@client.command(aliases=['votekick', 'k'])
@commands.cooldown(1.0, 600.0, commands.BucketType.guild)
async def kick(ctx, *, userat):
    if userat == "<@!811330525289381938>":
        await ctx.send("```Я не могу кикнуть сам себя```")
    else:
        # Проверка на указание ника
        if userat:
            # Обработка ID Обвиняемого
            idv = await getid(userat)
            try:
                # Поиск участника
                findmember = await ctx.guild.fetch_member(idv)
                # Создание обьекта обвиняемого
                nameat = await client.fetch_user(idv)
                voteyes, voteno = await pollcreate(ctx, nameat, instance='kick')
                # Голосов ЗА больше
                if voteyes > voteno:
                    embedVar = discord.Embed(title="Вы были кикнуты с сервера {0}".format(ctx.guild.name),
                                             color=0x0002a7)
                    embedVar.set_footer(text="Чтобы вернуться просто зайдите снова по приглашению")
                    embedVar.set_thumbnail(url=ctx.guild.icon_url)
                    await nameat.send(embed=embedVar)
                    await nameat.send("https://discord.gg/DUw5BFnhtV")
                    await ctx.guild.kick(nameat)
                    await ctx.send("```{0} был кикнут!```".format(nameat))
                # Голосов ПРОТИВ больше
                elif voteno > voteyes:
                    await ctx.send("```{0} не будет кикнут```".format(nameat))
            except (discord.errors.NotFound, discord.ext.commands.errors.CommandInvokeError):
                await ctx.send('```Пользователя нет на этом сервере```')
        else:
            await ctx.send('```Укажите кого кикать! → %kick @someone```')

@client.command(aliases=['voteban', 'b'])
@commands.cooldown(1.0, 600.0, commands.BucketType.guild)
async def ban(ctx, *, userat):
    if userat == "<@!811330525289381938>":
        await ctx.send("```Я не могу забанить самого себя```")
    else:
        # Проверка на указание ника
        if userat:
            # Обработка ID Обвиняемого
            idv = await getid(userat)
            try:
                # Поиск участника
                findmember = await ctx.guild.fetch_member(idv)
                # Создание обьекта обвиняемого
                nameat = await client.fetch_user(idv)
                voteyes, voteno = await pollcreate(ctx, nameat, instance='ban')
                # Голосов ЗА больше
                if voteyes > voteno:
                    embedVar = discord.Embed(title="Вы были забанены на сервере {0}".format(ctx.guild.name),
                                             color=0x0002a7)
                    embedVar.set_footer(text="Чтобы вернуться попросите вас разбанить")
                    embedVar.set_thumbnail(url=ctx.guild.icon_url)
                    await nameat.send(embed=embedVar)
                    await ctx.guild.ban(nameat, reason=None, delete_message_days=0)
                    await ctx.send("```{0} был забанен!```".format(nameat))
                # Голосов ПРОТИВ больше
                elif voteno > voteyes:
                    await ctx.send("```{0} не будет забанен```".format(nameat))
            except (discord.errors.NotFound, discord.ext.commands.errors.CommandInvokeError):
                await ctx.send('```Пользователя нет на этом сервере```')
        else:
            await ctx.send('```Укажите кого банить! → %ban @someone```')

@client.command(aliases=['voteunban', 'ub'])
@commands.cooldown(1.0, 600.0, commands.BucketType.guild)
async def unban(ctx):
    # Поиск участника
    listofbans = await ctx.guild.bans()
    strlistofbans = "";
    i = 1
    # Сбор банлиста
    for entry in listofbans:
        strlistofbans += "{0}. {1.name}#{1.discriminator}\n".format(i, entry.user)
        i += 1
    # Проверка на пустоту банлиста
    if strlistofbans == "":
        await ctx.send("```Никто не забанен```")
    else:
        await ctx.send('```Кого вы хотите разбанить?:```')
        await ctx.send("```" + strlistofbans + "```")
        try:
            # Прослушка ответа
            def check(ubanswer):
                return ubanswer.author == ctx.message.author

            ubanswer = await client.wait_for('message', timeout=15.0, check=check)
            # Проверка на нелитерный ответ
            if ubanswer.content.isdecimal():
                nameat = listofbans[int(ubanswer.content) - 1].user
                voteyes, voteno = await pollcreate(ctx, nameat, instance='unban')
                # Голосов ЗА больше
                if voteyes > voteno:
                    embedVar = discord.Embed(title="Вас разбанили на сервере {0}".format(ctx.guild.name),
                                             color=0x0002a7)
                    embedVar.set_footer(text="Вы можете вернуться по ссылке снизу")
                    embedVar.set_thumbnail(url=ctx.guild.icon_url)
                    try:
                        await nameat.send(embed=embedVar)
                        await nameat.send("https://discord.gg/DUw5BFnhtV")
                    except discord.Forbidden:
                        await ctx.send(
                            "```Не смог отправить {0} уведомление о его разбане, сообщите ему```".format(nameat))
                    await ctx.guild.unban(nameat)
                    await ctx.send("```{0} был разбанен!```".format(nameat))
                # Голосов ПРОТИВ больше
                elif voteno > voteyes:
                    await ctx.send("```{0} не будет разбанен```".format(nameat))
            else:
                await ctx.send("```Вы не указали цифру```")
        except TimeoutError:
            await ctx.send("```Вы не выбрали кого разбанить```")

@client.command(aliases=['votetwink', 't'])
@commands.cooldown(1.0, 600.0, commands.BucketType.guild)
async def twink(ctx, *, userat):
    if userat == "<@!811330525289381938>":
        await ctx.send("```Я явно не твинк```")
    else:
        # Проверка на указание ника
        if userat:
            # Обработка ID Обвиняемого
            idv = await getid(userat)
            try:
                # Поиск участника
                findmember = await ctx.guild.fetch_member(idv)
                # Создание обьекта обвиняемого
                nameat = await client.fetch_user(idv)
                voteyes, voteno = await pollcreate(ctx, nameat, instance='twink')
                # Голосов ЗА больше
                if voteyes > voteno:
                    listofroles = await ctx.guild.fetch_roles()
                    for entry in listofroles:
                        if entry.name == 'Твинк':
                            role = entry
                    await findmember.add_roles(role)
                    await ctx.send("```{0} теперь твинк!```".format(nameat))
                # Голосов ПРОТИВ больше
                elif voteno > voteyes:
                    await ctx.send("```{0} не будет твинком```".format(nameat))
            except (discord.errors.NotFound, discord.ext.commands.errors.CommandInvokeError):
                await ctx.send('```Пользователя нет на этом сервере```')
        else:
            await ctx.send('```Укажите кого нанять! → %assign @someone```')

@client.command(aliases=['voteassign', 'a'])
@commands.cooldown(1.0, 120.0, commands.BucketType.guild)
async def assign(ctx, *, userat):
    # Проверка на указание ника
    if userat:
        # Обработка ID Обвиняемого
        idv = await getid(userat)
        try:
            # Поиск участника
            findmember = await ctx.guild.fetch_member(idv)
            # Создание обьекта обвиняемого
            nameat = await client.fetch_user(idv)
            voteyes, voteno = await pollcreate(ctx, nameat, instance='assign')
            # Голосов ЗА больше
            if voteyes > voteno:
                listofroles = await ctx.guild.fetch_roles()
                for entry in listofroles:
                    if entry.name == 'Гильдиец':
                        role = entry
                await findmember.add_roles(role)
                await ctx.send("```{0} добро пожаловать в гильдию!```".format(nameat))
            # Голосов ПРОТИВ больше
            elif voteno > voteyes:
                await ctx.send("```{0} не будет назначен```".format(nameat))
        except (discord.errors.NotFound, discord.ext.commands.errors.CommandInvokeError):
            await ctx.send('```Пользователя нет на этом сервере```')
    else:
        await ctx.send('```Укажите кого нанять! → %assign @someone```')

@client.command(aliases=['votenewvoice', 'nw'])
@commands.cooldown(1.0, 600.0, commands.BucketType.guild)
async def newvoice(ctx):
    True

# voice actions
@client.command(aliases=['votemove', 'mv'])
@commands.cooldown(1.0, 120.0, commands.BucketType.guild)
async def move(ctx, *, userat):
    hornycheck = None
    idv = await getid(userat)
    checkroles = await ctx.guild.fetch_member(idv)
    listofroles = checkroles.roles
    for entry in listofroles:
        if entry.name == '🅷🅾🆁🅽🆈💩':
            hornycheck = entry
    if userat == "<@!811330525289381938>":
        await ctx.send("```Я не могу мувнуть себя```")
    else:
        # Поиск участника
        listofchannels = ctx.guild.voice_channels
        strlistofchannels = "";
        i = 1
        # Сбор листа каналов
        for entry in listofchannels:
            if entry.name != 'ПРОСНИСЬ!!!':
                strlistofchannels += "{0}. {1.name}\n".format(i, entry)
                i += 1
        # Проверка на пустоту листа
        if strlistofchannels == "":
            await ctx.send("```Каналы отсутствуют```")
        else:
            checkvoice = await ctx.guild.fetch_member(idv)
            if checkvoice.voice is None:
                await ctx.send("```Пользователя нет в войсчате```")
            elif hornycheck != None:
                await ctx.send('```Нельзя вытаскивать из хорниджейла```')
            else:
                await ctx.send('```Куда вы хотите мувнуть?:```')
                await ctx.send("```" + strlistofchannels + "```")
                try:
                    # Прослушка ответа
                    def check(ubanswer):
                        return ubanswer.author == ctx.message.author

                    ubanswer = await client.wait_for('message', timeout=15.0, check=check)
                    # Проверка на нелитерный ответ
                    if ubanswer.content.isdecimal():
                        # Поиск участника
                        findmember = await ctx.guild.fetch_member(idv)
                        channelobj = listofchannels[int(ubanswer.content) - 1]
                        nameat = findmember
                        voteyes, voteno = await pollcreate(ctx, nameat, instance='move')
                        # Голосов ЗА больше
                        if voteyes > voteno:
                            await nameat.move_to(channelobj)
                            await ctx.send("```{0} был мувнут!```".format(nameat))
                        # Голосов ПРОТИВ больше
                        elif voteno > voteyes:
                            await ctx.send("```{0} не будет мувнут```".format(nameat))
                    else:
                        await ctx.send("```Вы не указали цифру```")
                except TimeoutError:
                    await ctx.send("```Вы не выбрали куда мувнуть```")

@client.command(aliases=['votemute', 'mt'])
@commands.cooldown(1.0, 300.0, commands.BucketType.guild)
async def mute(ctx, *, userat):
    # Проверка на указание ника
    if userat:
        # Обработка ID Обвиняемого
        idv = await getid(userat)
        try:
            # Поиск участника
            findmember = await ctx.guild.fetch_member(idv)
            if findmember.voice is None:
                await ctx.send("```Пользователя нет в войсчате```")
            else:
                # Создание обьекта обвиняемого
                nameat = await client.fetch_user(idv)
                # Плашка с голосованием
                voteyes, voteno = await pollcreate(ctx, nameat, instance='mute')
                # Голосов ЗА больше
                if voteyes > voteno:
                    await findmember.edit(mute=True)
                    await ctx.send("```{0} был замучен!```".format(nameat))
                # Голосов ПРОТИВ больше
                elif voteno > voteyes:
                    await ctx.send("```{0} не будет замучен```".format(nameat))
        except (discord.errors.NotFound, discord.ext.commands.errors.CommandInvokeError):
            await ctx.send('```Пользователя нет на этом сервере```')
    else:
        await ctx.send('```Укажите кого замутить! → %mute @someone```')

@client.command(aliases=['voteunmute', 'umt'])
@commands.cooldown(1.0, 120.0, commands.BucketType.guild)
async def unmute(ctx, *, userat):
    # Проверка на указание ника
    if userat:
        # Обработка ID Обвиняемого
        idv = await getid(userat)
        try:
            # Поиск участника
            findmember = await ctx.guild.fetch_member(idv)
            if findmember.voice is None:
                await ctx.send("```Пользователя нет в войсчате```")
            else:
                # Создание обьекта обвиняемого
                nameat = await client.fetch_user(idv)
                voteyes, voteno = await pollcreate(ctx, nameat, instance='unmute')
                # Голосов ЗА больше
                if voteyes > voteno:
                    await findmember.edit(mute=False)
                    await ctx.send("```{0} был размучен!```".format(nameat))
                # Голосов ПРОТИВ больше
                elif voteno > voteyes:
                    await ctx.send("```{0} не будет размучен```".format(nameat))
        except (discord.errors.NotFound, discord.ext.commands.errors.CommandInvokeError):
            await ctx.send('```Пользователя нет на этом сервере```')
    else:
        await ctx.send('```Укажите кого размутить! → %unmute @someone```')

@client.command(aliases=['votedeafen', 'df'])
@commands.cooldown(1.0, 300.0, commands.BucketType.guild)
async def deafen(ctx, *, userat):
    # Проверка на указание ника
    if userat:
        # Обработка ID Обвиняемого
        idv = await getid(userat)
        try:
            # Поиск участника
            findmember = await ctx.guild.fetch_member(idv)
            if findmember.voice is None:
                await ctx.send("```Пользователя нет в войсчате```")
            else:
                # Создание обьекта обвиняемого
                nameat = await client.fetch_user(idv)
                voteyes, voteno = await pollcreate(ctx, nameat, instance='deafen')
                # Голосов ЗА больше
                if voteyes > voteno:
                    await findmember.edit(deafen=True)
                    await ctx.send("```{0} был заглушен!```".format(nameat))
                # Голосов ПРОТИВ больше
                elif voteno > voteyes:
                    await ctx.send("```{0} не будет заглушен```".format(nameat))
        except (discord.errors.NotFound, discord.ext.commands.errors.CommandInvokeError):
            await ctx.send('```Пользователя нет на этом сервере```')
    else:
        await ctx.send('```Укажите кого заглушить! → %deafen @someone```')

@client.command(aliases=['voteundeafen', 'udf'])
@commands.cooldown(1.0, 120.0, commands.BucketType.guild)
async def undeafen(ctx, *, userat):
    # Проверка на указание ника
    if userat:
        # Обработка ID Обвиняемого
        idv = await getid(userat)
        try:
            # Поиск участника
            findmember = await ctx.guild.fetch_member(idv)
            if findmember.voice is None:
                await ctx.send("```Пользователя нет в войсчате```")
            else:
                # Создание обьекта обвиняемого
                nameat = await client.fetch_user(idv)
                voteyes, voteno = await pollcreate(ctx, nameat, instance='undeafen')
                # Голосов ЗА больше
                if voteyes > voteno:
                    await findmember.edit(deafen=False)
                    await ctx.send("```{0} был разглушен!```".format(nameat))
                # Голосов ПРОТИВ больше
                elif voteno > voteyes:
                    await ctx.send("```{0} не будет разглушен```".format(nameat))
        except (discord.errors.NotFound, discord.ext.commands.errors.CommandInvokeError):
            await ctx.send('```Пользователя нет на этом сервере```')
    else:
        await ctx.send('```Укажите кого разглушен! → %undeafen @someone```')

@client.command(aliases=['votedisconnect', 'dc'])
@commands.cooldown(1.0, 120.0, commands.BucketType.guild)
async def disconnect(ctx, *, userat):
    # Проверка на указание ника
    if userat:
        # Обработка ID Обвиняемого
        idv = await getid(userat)
        try:
            # Поиск участника
            findmember = await ctx.guild.fetch_member(idv)
            if findmember.voice is None:
                await ctx.send("```Пользователя нет в войсчате```")
            else:
                # Создание обьекта обвиняемого
                nameat = await client.fetch_user(idv)
                voteyes, voteno = await pollcreate(ctx, nameat, instance='disconnect')
                # Голосов ЗА больше
                if voteyes > voteno:
                    await findmember.move_to(None)
                    await ctx.send("```{0} был выкинут!```".format(nameat))
                # Голосов ПРОТИВ больше
                elif voteno > voteyes:
                    await ctx.send("```{0} не будет выкинут```".format(nameat))
        except (discord.errors.NotFound, discord.ext.commands.errors.CommandInvokeError):
            await ctx.send('```Пользователя нет на этом сервере```')
    else:
        await ctx.send('```Укажите кого выкинуть из войса! → %disconnect @someone```')

@client.command(aliases=['wakeup', 'w'])
@commands.cooldown(1.0, 60.0, commands.BucketType.guild)
async def wake(ctx, *, userat):
    if userat == "<@!811330525289381938>":
        await ctx.send("```Меня не нужно будить🤔```")
    else:
        if userat:
            try:
                idv = await getid(userat)
                checkvoice = await ctx.guild.fetch_member(idv)
                if ctx.message.author.voice is None:
                    await ctx.send('```Нужно быть в войсчате чтобы использовать эту команду```')
                elif checkvoice.voice is None:
                    await ctx.send("```Пользователя нет в войсчате```")
                elif ctx.message.author.voice.channel != checkvoice.voice.channel:
                    await ctx.send("```Нужно быть в одном войсчате с пользователем которого вы хотите разбудить```")
                else:
                    findmember = await ctx.guild.fetch_member(idv)
                    nameat = findmember
                    wakechannel = ctx.guild.get_channel(813367283342508052)
                    backchannel = checkvoice.voice.channel
                    startwake = time()
                    while time() < startwake + 10:
                        await sleep(2)
                        await nameat.move_to(wakechannel)
                        await sleep(2)
                        await nameat.move_to(backchannel)
                    await ctx.send("```Разбудил {0}!```".format(nameat))
            except (discord.errors.NotFound, discord.ext.commands.errors.CommandInvokeError):
                await ctx.send('```Пользователя нет на этом сервере```')
        else:
            await ctx.send('```Укажите кого разбудить! → %wake @someone```')

@client.command(aliases=['pn'])
@commands.cooldown(1.0, 60.0, commands.BucketType.guild)
async def ping(ctx, *, userat):
    if userat == "<@!811330525289381938>":
        await ctx.send("```Меня не нужно пинговать```")
    else:
        try:
            try:
                idv = await getid(userat)
                nameat = await client.fetch_user(idv)
                pingmsglist = []
                for i in range(5):
                    for j in range(5):
                        pingmsglist.append(await ctx.send(userat))
                    for j in range(5):
                        await pingmsglist[j].delete()
                    pingmsglist.clear()
                await ctx.send('```{0} был пропингован```'.format(nameat))
            except (discord.errors.NotFound, discord.ext.commands.errors.CommandInvokeError):
                await ctx.send('```Пользователя нет на этом сервере```')
        except discord.ext.commands.errors.MissingRequiredArgument:
            await ctx.send('```Укажите кого пропинговать! → %ping @someone```')

# other
@client.command(aliases=['otsosat'])
async def suck(ctx, *, userat):
    await other.suck(ctx, userat,client)

@client.command(aliases=['votejail', 'j'])
@commands.cooldown(1.0, 600.0, commands.BucketType.guild)
async def jail(ctx, *, userat):
    await other.jail(ctx, userat,client)

@client.command(aliases=['commands', 'h'])
async def help(ctx):
    await other.help(ctx,client)

@client.command()
async def test(ctx):
	True

# music

@client.command(aliases=['p'])
async def play(ctx, link):
    await music.play(ctx, link, client)

@client.command(aliases=['l'])
async def loop(ctx):
    await music.loop(ctx, client)

@client.command(aliases=['s'])
async def skip(ctx):
    await music.skip(ctx, client)

@client.command(aliases=['q'])
async def queue(ctx):
    await music.queue(ctx, client)

@client.command(aliases=['st'])
async def stop(ctx):
    await music.stop(ctx, client)

@kick.error
async def kick_error(ctx, error): await error_handler.handle(ctx, error, 'kick')
@ban.error
async def ban_error(ctx, error): await error_handler.handle(ctx, error, 'ban')
@unban.error
async def unban_error(ctx, error): await error_handler.handle(ctx, error, 'unban')
@move.error
async def move_error(ctx, error): await error_handler.handle(ctx, error, 'move')
@mute.error
async def mute_error(ctx, error): await error_handler.handle(ctx, error, 'mute')
@unmute.error
async def unmute_error(ctx, error): await error_handler.handle(ctx, error, 'unmute')
@deafen.error
async def deafen_error(ctx, error): await error_handler.handle(ctx, error, 'deafen')
@undeafen.error
async def undeafen_error(ctx, error): await error_handler.handle(ctx, error, 'undeafen')
@disconnect.error
async def disconnect_error(ctx, error): await error_handler.handle(ctx, error, 'disconnect')
@wake.error
async def wake_error(ctx, error): await error_handler.handle(ctx, error, 'wake')
@twink.error
async def twink_error(ctx, error): await error_handler.handle(ctx, error, 'twink')
@ping.error
async def ping_error(ctx, error): await error_handler.handle(ctx, error, 'ping')
@play.error
async def play_error(ctx, error): await error_handler.handle(ctx, error, 'play')


client.run('ODExMzMwNTI1Mjg5MzgxOTM4.YCwobw.6lsoZcWY0auZkQGkt9xlXkSALRs')