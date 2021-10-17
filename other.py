import discord
from asyncio import sleep, TimeoutError
from discord.ext import commands
import youtube_dl
import asyncio
#locallibs
from poll import pollcreate

async def getid(userat):
    idv = userat
    idv = idv.replace("<", "")
    idv = idv.replace("@", "")
    idv = idv.replace("!", "")
    idv = idv.replace(">", "")
    return idv

async def jail(ctx,userat,client):
    if userat == "<@!811330525289381938>":
        await ctx.send("```Я не хорни)```")
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
                voteyes,voteno = await pollcreate(ctx,nameat,instance='disconnect')
                # Голосов ЗА больше
                if voteyes > voteno:
                    listofroles = await ctx.guild.fetch_roles()
                    for entry in listofroles:
                        if entry.name == '🅷🅾🆁🅽🆈💩':
                            horny = entry
                    listofvc = await ctx.guild.fetch_channels()
                    for tmp in listofvc:
                        if tmp.name == '🤢𝑯̲̅𝑶̲̅𝑹̲̅𝑵̲̅𝒀̲̅ 𝑱̲̅𝑨̲̅𝑰̲̅𝑳̲̅💩':
                            vc = tmp
                    await findmember.add_roles(horny)
                    if findmember.voice is not None:
                        await findmember.move_to(vc)
                    await ctx.send("```{0} был заключен!```".format(nameat))
                    await sleep(600)
                    await findmember.remove_roles(horny)
                    await ctx.send("```{0} выпущен из под стражи!```".format(nameat))
                # Голосов ПРОТИВ больше
                elif voteno > voteyes:
                    await ctx.send("```{0} не хорни```".format(nameat))
            except (discord.errors.NotFound, discord.ext.commands.errors.CommandInvokeError):
                await ctx.send('```Пользователя нет на этом сервере```')
        else:
            await ctx.send('```Укажите кого заключить! → %jail @someone```')

async def suck(ctx,userat,client):
    if userat:
        try:
            idv = await getid(userat)
            nameat = await client.fetch_user(idv)
            if ctx.message.author==nameat:
                await ctx.send("😐 {0} отсосал самому себе 🤔".format(nameat))
            else:
                await ctx.send("🥴 {0} 🍆отсосал💦 {1} 🍑".format(ctx.message.author, nameat))
        except (discord.errors.NotFound, discord.ext.commands.errors.CommandInvokeError):
            await ctx.send('```Пользователя нет на этом сервере```')
    else:
        await ctx.send('```Укажите кому отсосать!🥴 → %suck @someone```')

async def help(ctx,client):
    await ctx.send("```ini\n"
                   "Команды бота:\n"
                   "\n"
                   "[%assign] @someone (%voteassign/%a - Нанять в гильдию\n"
                   "\n"
                   "[%kick] @someone (%votekick/%k) - Кикнуть кого-либо\n"
                   "\n"
                   "[%ban] @someone (%voteban/%b) - Забанить кого-либо\n"
                   "\n"
                   "[%unban] (%voteunban/%ub) - Разбанить кого-либо\n"
                   "\n"
                   "[%move] @someone (%votemove/%mv) - Мувнуть кого-либо\n"
                   "\n"
                   "[%mute] @someone (%votemute/%mt) - Замутить кого-либо\n"
                   "\n"
                   "[%unmute] @someone (%voteunmute/%umt) - Размутить кого-либо\n"
                   "\n"
                   "[%deafen] @someone (%votedeafen/%df) - Заглушить кого-либо\n"
                   "\n"
                   "[%undeafen] @someone (%voteundeafen/%udf) - Разглушить кого-либо\n"
                   "\n"
                   "[%disconnect] @someone (%votedisconnect/%dc) - Отключить кого-либо\n"
                   "\n"
                   "[%jail] @someone (%votejail/%j) - Отправить в хорни джейл на 10 мин\n"
                   "\n"
                   "[%wake] @someone (%wakeup/%w) - Покидать выбранного из канала в канал в течении 15 секунд\n"
                   "\n"
                   '[%twink] @someone (%votetwink/%t) - Дать выбранному роль "Твинк", не позволяющая голосовать\n'
                   "[КОМАНДА ДЛЯ УДАЛЕНИЯ РОЛИ ОТСУТСТВУЕТ, ПУТИ НАЗАД НЕТ]\n"
                   "\n"
                   "[%ping] @someone (%pn) - Упоминать пользователя в течении 15 секунд\n"
                   "\n"
                   "[%suck] @someone (%otsosat) - отсосать🍆💦```")

async def test(ctx,client):
    if ctx.message.author.id==775829071498051584 or ctx.message.author.id==220219840466518016:
        await ctx.send('Здравствуйте, создатель')