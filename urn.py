from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime as DT
import os
import discord
from discord import Option
 

load_dotenv()
bot = commands.Bot(command_prefix=['<@1043241661179900074> '], intents=discord.Intents.all(), help_command=None)
bot.startTime = DT.now()
bot.currentTime = DT.now()

@bot.event
async def on_ready():
    print(f"{bot.user} ({bot.user.id}) is online\nTime at start: {bot.currentTime}\nTime to start: " + str((DT.now() - bot.startTime)))
    with open(r'dm.txt', 'r') as file:
        data1 = file.read()
        file.close()
    with open(r'reacte.txt', 'r') as file2:
        data2 = file2.read()    
        file2.close()    
    await bot.change_presence(activity=discord.Game(name=f"⚱ed {str(data1)} people | Reacted to {str(data2)} message"))

@bot.slash_command(name="urn", description="⚱")
async def urn(ctx, urn: Option(discord.Member, "pick a user to ⚱", required=True, defualt=None)):
    dm = bot.get_user(urn.id)
    try:
        await dm.send("⚱")
        await ctx.respond(f"<@{urn.id}> has been ⚱ed", ephemeral=True)
        with open(r'dm.txt', 'r') as file:
            data1 = file.read()
            data1 = data1.replace(data1, str(int(data1)+1))
        with open(r'dm.txt', 'w') as file:
            file.write(data1)
            file.close()
        with open(r'reacte.txt', 'r') as file2:
            data2 = file2.read()
            file2.close()
        await bot.change_presence(activity=discord.Game(name=f"⚱ed {str(data1)} people | Reacted to {str(data2)} messages"))
    except:
        await ctx.respond(f"an error accured 🥴", ephemeral=True)

@bot.user_command(guild_ids=[767528920437227530], name='death')
async def death(ctx, user: discord.Member):
    if ctx.author.id == 557286947106586627:
        await ctx.respond("bot killed", ephemeral=True)
        await bot.close()
    else:
        await ctx.respond("bozo you cant do this", ephemeral=True)

@bot.message_command(name='urn')
async def urn(ctx, message: discord.Message):
    dm = bot.get_user(message.author.id)
    try:
        await dm.send("⚱")
        await ctx.respond(f"<@{message.author.id}> has been ⚱ed", ephemeral=True)
        with open(r'dm.txt', 'r') as file:
            data1 = file.read()
            data1 = data1.replace(data1, str(int(data1)+1))
        with open(r'dm.txt', 'w') as file:
            file.write(data1)
            file.close()
        with open(r'reacte.txt', 'r') as file2:
            data2 = file2.read()
            file2.close()
        await bot.change_presence(activity=discord.Game(name=f"⚱ed {str(data1)} people | Reacted to {str(data2)} messages"))
    except:
        await ctx.respond(f"an error accured 🥴", ephemeral=True)

@bot.user_command(name='urn')
async def urn(ctx, user: discord.Member):
    dm = bot.get_user(user.id)
    try:
        await dm.send("⚱")
        await ctx.respond(f"<@{user.id}> has been ⚱ed", ephemeral=True)
        with open(r'dm.txt', 'r') as file:
            data1 = file.read()
            data1 = data1.replace(data1, str(int(data1)+1))
        with open(r'dm.txt', 'w') as file:
            file.write(data1)
            file.close()
        with open(r'reacte.txt', 'r') as file2:
            data2 = file2.read()
            file2.close()
        await bot.change_presence(activity=discord.Game(name=f"⚱ed {str(data1)} people | Reacted to {str(data2)} messages"))
    except:
        await ctx.respond(f"an error accured 🥴", ephemeral=True)

@bot.event
async def on_message_edit(message_before, message_after):
    message = bot.get_message(message_after.id)
    await addUrn(message)

@bot.event
async def on_message(message):
        await addUrn(message)
        await bot.process_commands(message) 


async def addUrn(message):
    if message.author.id != 1043241661179900074:
        if "⚱" in message.content:
            await message.add_reaction("⚱")
        elif "u" in message.content.lower():
            if "r" in message.content.lower():
                if "n" in message.content.lower():
                    await message.add_reaction("⚱")
                    with open(r'reacte.txt', 'r') as file:
                        data1 = file.read()
                        data1 = data1.replace(data1, str(int(data1)+1))
                    with open(r'reacte.txt', 'w') as file:
                        file.write(data1)
                        file.close()
                    with open(r'dm.txt', 'r') as file2:
                        data2 = file2.read()
                        file2.close()
                    await bot.change_presence(activity=discord.Game(name=f"⚱ed {str(data2)} people | Reacted to {str(data1)} messages"))

bot.run(os.getenv('TOKEN'))
