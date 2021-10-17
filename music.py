import discord
from asyncio import sleep, TimeoutError
from discord.ext import commands
import youtube_dl
import asyncio



youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': False,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

queuelist = []
linklist = []

async def nextsong():
    pass

async def play(ctx,link,client):
    if ctx.message.author.voice == None:
        await ctx.send('```Нужно быть в войсчате чтобы использовать эту команду```')
    else:
        channel = ctx.message.author.voice.channel
        try:
            await channel.connect()
            server = ctx.message.guild
            voicechannel = server.voice_client
            async with ctx.typing():
                player = await YTDLSource.from_url(link, loop=client.loop)
                voicechannel.play(player, after=nextsong)
                await ctx.send('```Сейчас играет: {0}```'.format(player.title))
                queuelist.append(player.title)
                linklist.append(link)
        except discord.ext.commands.errors.ClientException:
            tmpplay = await YTDLSource.from_url(link, loop=client.loop)
            queuelist.append(tmpplay.title)
            linklist.append(link)
            await ctx.send('```{0} добавлена в очередь```'.format(tmpplay.title))

async def skip(ctx,client):
    server = ctx.message.guild
    voicechannel = server.voice_client
    player = await YTDLSource.from_url(queuelist[1], loop=client.loop)
    voicechannel.play(player)

async def loop(ctx,client):
    ctx

async def queue(ctx, client):
    print(queuelist)
    if not queuelist:
        await ctx.send('```Cписок пуст```')
    else:
        strlistofqueue = ''
        j = 1
        for i in queuelist:
            strlistofqueue += '{0}. {1}\n'.format(j, i)
            j += 1
        await ctx.send('```{0}```'.format(strlistofqueue))

async def stop(ctx, client):
    print(queuelist)
    voiceclient = ctx.message.guild.voice_client
    if ctx.message.author.voice == None:
        await ctx.send('```Нужно быть в войсчате чтобы использовать эту команду```')
    else:
        try:
            await voiceclient.disconnect()
            queuelist.clear()
        except AttributeError:
            await ctx.send('```Бот сейчас ничего не играет```')