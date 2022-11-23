from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime as DT
import os
import discord

urn = ["urn", "Urn", "URn", "URN", "urN", "uRN", "uRn", "UrN",]

load_dotenv()
bot = commands.Bot(command_prefix=['<@1043241661179900074> '], intents=discord.Intents.all(), help_command=None)
bot.startTime = DT.now()
bot.currentTime = DT.now()

@bot.event
async def on_ready():
    print(f"{bot.user} ({bot.user.id}) is online\nTime at start: {bot.currentTime}\nTime to start: " + str((DT.now() - bot.startTime)))
    await bot.change_presence(activity=discord.Game(name="urn"))

@bot.user_command(guilds_id=[767528920437227530], name='death')
async def death(ctx, user: discord.Member):
    if ctx.author.id == 557286947106586627:
        await ctx.respond("bot killed", ephemeral=True)
        await bot.close()
    else:
        await ctx.respond("bozo you cant do this", ephemeral=True)

@bot.user_command(name='urn')
async def callbackname(ctx, user: discord.Member):
    await ctx.respond(f"<@{user.id}> has been ⚱ed", ephemeral=True)
    dm = bot.get_user(user.id)
    await dm.send("⚱")

@bot.event
async def on_message(message):
    if message.author.id != 1043241661179900074:
        if "⚱" in message.content:
            await message.add_reaction("⚱")
        elif "u" in message.content or "U" in message.content:
            if "r" in message.content or "R" in message.content:
                if "n" in message.content or "N" in message.content:
                    await message.add_reaction("⚱")
        await bot.process_commands(message) 

bot.run(os.getenv('TOKEN'))
