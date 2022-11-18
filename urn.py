from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime as DT
import os
import discord


load_dotenv()
bot = commands.Bot(command_prefix=['<@1043241661179900074>'], intents=discord.Intents.all(), help_command=None)
bot.startTime = DT.now()
bot.currentTime = DT.now()

@bot.event
async def on_ready():
    print(f"{bot.user} ({bot.user.id}) is online\nTime at start: {bot.currentTime}\nTime to start: " + str((DT.now() - bot.startTime)))
    await bot.change_presence(activity=discord.Game(name="urn"))

@bot.event
async def on_message(message):
    if "u" in message.content:
        if "r" in message.content:
            if "n" in message.content:
                await message.add_reaction("⚱")
                  

bot.run(os.getenv('TOKEN'))
