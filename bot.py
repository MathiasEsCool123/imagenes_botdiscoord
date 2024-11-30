import discord
from discord.ext import commands
from PIL import Image, ImageFilter
import requests
from io import BytesIO
import yt_dlp  

intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} está conectado y listo!")


@bot.command()
async def filtro(ctx, miembro: discord.Member = None):
    """Aplica un filtro al avatar de un usuario."""
    if not miembro:
        miembro = ctx.author

  
    avatar_url = miembro.avatar.url
    response = requests.get(avatar_url)
    avatar = Image.open(BytesIO(response.content))


    filtro_aplicado = avatar.filter(ImageFilter.BLUR)

    
    buffer = BytesIO()
    filtro_aplicado.save(buffer, format="PNG")
    buffer.seek(0)

 
    await ctx.send(file=discord.File(fp=buffer, filename="avatar_editado.png"))


@bot.command()
async def join(ctx):
    """Unirse al canal de voz del usuario."""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Conectado al canal: {channel}")
    else:
        await ctx.send("¡Debes estar en un canal de voz para usar este comando!")


@bot.command()
async def play(ctx, url: str):
    """Reproducir audio desde un video de YouTube."""
    if not ctx.voice_client:
        await ctx.send("¡Primero usa el comando `!join` para conectar al bot!")
        return


    ydl_opts = {'format': 'bestaudio', 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']

    
    ctx.voice_client.stop()
    ctx.voice_client.play(discord.FFmpegPCMAudio(audio_url), after=lambda e: print("Reproducción finalizada."))
    await ctx.send(f"Reproduciendo: **{info['title']}**")


@bot.command()
async def leave(ctx):
    """Desconectar del canal de voz."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Desconectado del canal de voz.")
    else:
        await ctx.send("El bot no está conectado a un canal de voz.")


bot.run("token") 
