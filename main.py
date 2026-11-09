import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} - Mochi Ready!")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
        await ctx.send("Mochi ရောက်ပြီ! 🎵")
    else:
        await ctx.send("အရင် Voice Channel ထဲ ဝင်ဦးနော်!")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Mochi ပြန်ပြီနော်! 👋")
    else:
        await ctx.send("Mochi က Voice ထဲမှာ မရှိဘူးလေ!")

@bot.command()
async def play(ctx, *, search: str):
    if not ctx.voice_client:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("အရင် Voice Channel ထဲ ဝင်ဦး!")
            return

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search, download=False)
        if 'entries' in info:
            info = info['entries'][0]
        url = info['url']
        title = info.get('title', 'Unknown')

    vc = ctx.voice_client
    if vc.is_playing():
        vc.stop()

    ffmpeg_opts = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    vc.play(discord.FFmpegPCMAudio(url, **ffmpeg_opts))
    await ctx.send(f"🎶 ဖွင့်နေပြီ: **{title}**")

@bot.command()
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("ရပ်လိုက်ပြီ ⏹️")

bot.run(os.getenv("DISCORD_TOKEN"))