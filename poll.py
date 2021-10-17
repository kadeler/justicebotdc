import discord
from asyncio import sleep

async def pollcreate(ctx,nameat,instance):
    botmember = await ctx.guild.fetch_member(811330525289381938)
    # Плашка с голосованием
    if instance=='kick':
        embedVar = discord.Embed(title="Голосуем за кик {0}".format(nameat), color=0x0002a7)
    elif instance=='assign':
        embedVar = discord.Embed(title="Голосуем за найм в гильдию {0}".format(nameat), color=0x0002a7)
    elif instance=='ban':
        embedVar = discord.Embed(title="Голосуем за бан {0}".format(nameat), color=0x0002a7)
    elif instance=='unban':
        embedVar = discord.Embed(title="Голосуем за разбан {0}".format(nameat), color=0x0002a7)
    elif instance=='move':
        embedVar = discord.Embed(title="Голосуем за мув {0}".format(nameat), color=0x0002a7)
    elif instance=='mute':
        embedVar = discord.Embed(title="Голосуем за мут {0}".format(nameat), color=0x0002a7)
    elif instance=='unmute':
        embedVar = discord.Embed(title="Голосуем за размут {0}".format(nameat), color=0x0002a7)
    elif instance=='deafen':
        embedVar = discord.Embed(title="Голосуем за заглушение {0}".format(nameat), color=0x0002a7)
    elif instance=='undeafen':
        embedVar = discord.Embed(title="Голосуем за разглушение {0}".format(nameat), color=0x0002a7)
    elif instance=='disconnect':
        embedVar = discord.Embed(title="Голосуем за кик из войса {0}".format(nameat), color=0x0002a7)
    elif instance=='jail':
        embedVar = discord.Embed(title="Голосуем за заключение {0}".format(nameat), color=0x0002a7)
    elif instance=='twink':
        embedVar = discord.Embed(title="Голосуем чтобы {0} был твинком".format(nameat), color=0x0002a7)
    embedVar.set_author(name="{0} начал голосование!".format(ctx.message.author))
    embedVar.set_footer(text="Голосование окончится через 30 секунд")
    embedVar.set_thumbnail(url=nameat.avatar_url)
    votemsg = await ctx.send(embed=embedVar)
    await votemsg.add_reaction('✅')
    await votemsg.add_reaction('❎')
    await sleep(30)
    # Подсчет голосов
    voteyes = 0
    voteno = 0
    refetched = await ctx.fetch_message(votemsg.id)
    votemsg = refetched
    for reaction in votemsg.reactions:
        for user in await reaction.users().flatten():
            reactmember = await ctx.guild.fetch_member(user.id)
            twink = False
            for role in reactmember.roles:
                if role.name == 'Твинк':
                    twink = True
            if twink == False:
                if reaction.emoji == '✅':
                    voteyes += 1
                elif reaction.emoji == '❎':
                    voteno += 1
            elif twink == True:
                await votemsg.remove_reaction('✅', reactmember)
                await votemsg.remove_reaction('❎', reactmember)
    voteyes -= 1; voteno -= 1
    await ctx.send("```Проголосовавших за: {0}\nПроголосовавших против: {1}```".format(voteyes, voteno))
    # Голосов нет
    if voteyes + voteno == 0:
        await ctx.send("```Никто не проголосовал```")
        return 0,0
    # Голосует не больше двух человек
    elif voteyes + voteno < 2:
        await ctx.send("```Проголосовавших мало, голосование отменяется```")
        return 0,0
    # Голосов поровну
    elif voteyes == voteno:
        await ctx.send("```Произошла ничья```")
        return 0,0
    else:
        return voteyes,voteno