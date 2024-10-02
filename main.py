import os
import discord
from dotenv import load_dotenv
import asyncio
from discord import FFmpegPCMAudio
from discord.ext import commands, tasks
import speech_recognition as sr
from openai import OpenAI

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
intents.members = True
intents.voice_states = True
bot = commands.Bot(command_prefix="jarvis ", intents=intents)
CHANNEL_ID = 1290491744139350110
audio_file = "jarvis.mp3"
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
MODEL="gpt-4o"

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    channel = bot.get_channel(CHANNEL_ID)

ROSS_USER_ID = 265197452842369025

@bot.command(pass_context = True, brief='Mute Sarah Ross constantly so you cannot hear her YAP')
async def muteRoss(ctx):
    await yesSir(ctx)
    constantRossMute.start()
    
@bot.command(pass_context = True, brief='Unmute Sarah')
async def unmuteRoss(ctx):
    await yesSir(ctx)
    constantRossMute.stop()

@tasks.loop(seconds = 0.1)
async def constantRossMute():
    for guild in bot.guilds:
        member = guild.get_member(ROSS_USER_ID)
        if member and member.voice and member.voice.channel:
            if not member.voice.mute:
                try:
                    await member.edit(mute = True)
                except discord.Forbidden:
                    print("Bot cannot mute")

@bot.command(brief='Join the current VC')
async def join(ctx):
    if ctx.author.voice:

        channel = ctx.author.voice.channel
        voice = await channel.connect()
    else:
        await ctx.send("Sorry sir, you are not in a voice channel")
    await yesSir(ctx)
@bot.command(brief='Leave the current VC')
async def leave(ctx):
    await yesSir(ctx)
    await ctx.voice_client.disconnect()

@bot.event
async def on_command_error(ctx, error):
    completion = client.chat.completions.create(
  model=MODEL,
  messages=[
    {"role": "system", "content": """You are JARVIS, the AI system from Iron Man, 
     and you should respond to questions like JARVIS. Start every exchange with sir,
      and end with sir as well, along with sir in between each sentence, however, if the content says anything similar to one 
     of these strings: \"yesSir\", \"join\", \"leave\", \"muteRoss\", \"unmuteRoss\", 
     then say ERROR instead. When referring to your the person prompting you, their 
     name will always be \"Patrick\", also if some asks about a person named Sarah, 
     make sure to make fun of them"""},
    {"role": "user", "content": ctx.message.content}
  ]
)
    await ctx.send(completion.choices[0].message.content)
    


async def yesSir(ctx):
    try:
        audio_source = discord.FFmpegPCMAudio(audio_file)
        ctx.voice_client.play(audio_source)
    except Exception as e:
        await ctx.send(f"Error {e}")

bot.run(TOKEN)

