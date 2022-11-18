from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime as DT
import os
import discord

urn = ["urn", "Urn", "URn", "URN", "urN", "uRN", "uRn", "UrN",]

load_dotenv()
bot = commands.Bot(command_prefix=['1043241661179900074 '], intents=discord.Intents.all(), help_command=None)
bot.startTime = DT.now()
bot.currentTime = DT.now()

@bot.event
async def on_ready():
    print(f"{bot.user} ({bot.user.id}) is online\nTime at start: {bot.currentTime}\nTime to start: " + str((DT.now() - bot.startTime)))
    await bot.change_presence(activity=discord.Game(name="urn"))

@bot.command()
async def kys():
    await bot.close()

@bot.event
async def on_message(message):
    if message.content == "urn" or message.content == "Urn" or message.content == "URn" or message.content == "URn" or message.content == "URN" or message.content == "urN" or message.content == "uRN" or message.content == "uRn" or message.content ==  "UrN":
        await message.reply("⚱")
    elif "u" in message.content or "U" in message.content:
        if "r" in message.content or "R" in message.content:
            if "n" in message.content or "N" in message.content:
                await message.add_reaction("⚱")


                  

bot.run(os.getenv('TOKEN'))
