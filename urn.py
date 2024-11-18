from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime as DT
import os
import discord
import random

#Buttons
class urnbuttonsA(discord.ui.View):        
    @discord.ui.button(label="◀", disabled=True)
    async def left_button_callback(self, button, interation):
        embe = interation.message.embeds[0]
        emb = str(embe.title).split('Top ')[1].replace('*', '')
        page = str(embe.footer).split("'")[1].split(" ")
        leader = await leaderboardMaker(interation.message.guild.id, emb, int(page[1])-1)
        await interation.edit(content=leader[0],embed=leader[1], view=leader[2])

    @discord.ui.button(label="▶", disabled=True)
    async def right_button_callback(self, button, interation):
        embe = interation.message.embeds[0]
        emb = str(embe.title).split('Top ')[1].replace('*', '')
        page = str(embe.footer).split("'")[1].split(" ")
        leader = await leaderboardMaker(interation.message.guild.id, emb, int(page[1])+1)
        await interation.edit(content=leader[0],embed=leader[1], view=leader[2])

class urnbuttonsB(discord.ui.View):
    @discord.ui.button(label="◀", disabled=True)
    async def left_button_callback(self, button, interation):
        nothing = 0

    @discord.ui.button(label="▶", disabled=False)
    async def right_button_callback(self, button, interation):
        embe = interation.message.embeds[0]
        emb = str(embe.title).split('Top ')[1].replace('*', '')
        page = str(embe.footer).split("'")[1].split(" ")
        leader = await leaderboardMaker(interation.message.guild.id, emb, int(page[1])+1)
        await interation.edit(content=leader[0],embed=leader[1], view=leader[2])
class urnbuttonsC(discord.ui.View):       
    @discord.ui.button(label="◀", disabled=False)
    async def left_button_callback(self, button, interation):
        embe = interation.message.embeds[0]
        emb = str(embe.title).split('Top ')[1].replace('*', '')
        page = str(embe.footer).split("'")[1].split(" ")
        leader = await leaderboardMaker(interation.message.guild.id, emb, int(page[1])-1)
        await interation.edit(content=leader[0],embed=leader[1], view=leader[2])

    @discord.ui.button(label="▶", disabled=True)
    async def right_button_callback(self, button, interation):
        nothing = 0

def buttonPick(footer):
    text = (str(footer).split("'"))[1]
    pages = text.split(" ")
    if pages[1] == '1':
        return urnbuttonsB()
    elif pages[1] == pages[3]:
        return urnbuttonsC()
    else:
        return urnbuttonsA()


load_dotenv()
bot = commands.Bot(command_prefix=['<@1043241661179900074> '], intents=discord.Intents.all(), help_command=None)
bot.startTime = DT.now()
bot.currentTime = DT.now()
currentactivity = 2
leaderboard = discord.SlashCommandGroup("leaderboard")

@bot.event
async def on_ready():
    print(f"{bot.user} ({bot.user.id}) is online\nTime at start: {bot.currentTime}\nTime to start: " + str((DT.now() - bot.startTime)))
    await bot.change_presence(activity=discord.Game(name=f"starting..."))
    tylist = ['dm', 'golden', 'reacte']
    guilds = bot.guilds
    dirlist = os.listdir('guilds')
    for guild in guilds:
        if str(guild.id) not in dirlist:
            os.makedirs(f'guilds/{guild.id}')
            for item in tylist:
                with open(f'guilds/{guild.id}/{item}.txt', 'w') as file:
                    file.write('0')
                    file.close()
    activityrotater.start()

@bot.event
async def on_guild_join(guild):
    tylist = ['dm', 'golden', 'reacte']
    dirlist = os.listdir('guilds')
    if str(guild.id) not in dirlist:
        os.makedirs(f'guilds/{guild.id}')
        for item in tylist:
            with open(f'guilds/{guild.id}/{item}.txt', 'w') as file:
                file.write('0')
                file.close()

@tasks.loop(minutes=15)
async def activityrotater():
    global currentactivity
    currentactivity = currentactivity + 1
    if currentactivity > 2:
        currentactivity = 0
    await activityupdater(currentactivity)


async def activityupdater(type):
    global currentactivity
    if type == currentactivity:
            type = (['reacte', 'dm', 'golden'])[type]
            sta = 0
            dirlist = os.listdir('guilds')    
            for item in dirlist:
                if item != 'opt':
                    dicts = await statCounter(item)
                    sta = dicts[type] + sta
            if type == 'reacte':
                content = f'Reacted to {sta} messages'
            elif type == 'dm':
                content = f"⚱'d {sta} people in dms"
            if type == 'golden':
                content = f"{sta} Golden ⚱'s have been spotted"
            await bot.change_presence(activity=discord.Game(name=content))

@bot.slash_command(name='rotateactivity', guild_ids=[int(os.getenv('GUILD'))])
@discord.default_permissions(administrator=True)
async def rotateactivity(ctx):
    global currentactivity
    currentactivity = currentactivity + 1
    if currentactivity > 2:
        currentactivity = 0
    await activityupdater(currentactivity)
    await ctx.respond(content='Activity Rotated', ephemeral=True)


@bot.event
async def on_application_command_error(ctx, error):
    try:
        await ctx.respond('an error accured 🥴', ephemeral=True)
    except:
        channel = bot.get_channel(int(os.getenv('CHANNEL')))
        await channel.send(content=f'an error accured 🥴\n{error}')

@leaderboard.command(name="visibility", description='Opt this server out from sharing its name in public leaderboards')
@discord.default_permissions(administrator=True)
@discord.option('value', choices=['True', 'False'], required=True)
async def visleaderboard(ctx, value):
    with open('guilds/opt/out.txt', 'r') as file:
        list = file.readlines()
        file.close()
    if value == 'True':
        if str(ctx.guild.id) in list:
            list.remove(str(ctx.guild.id))
            response = ('This server is now visible on public leaderboards')
        else:
            return await ctx.respond('This server is already visible', ephemeral=True)
    if value == 'False':
        if str(ctx.guild.id) not in list:
            list.append(str(ctx.guild.id))
            response = ('This server has been opt out on public leaderboards')
        else:
            return await ctx.respond('This server has already been opt out', ephemeral=True)
    with open('guilds/opt/out.txt', 'w') as file:
        file.write("\n".join([f"{t}"for t in list]))
        file.close()
    await ctx.respond(response, ephemeral=True)

@leaderboard.command(name='guild', description='See your servers stats')
async def guildleaderboard(ctx):
    item = await statCounter(ctx.guild.id)
    embed = discord.Embed(title=f'Guild Stats', color=0xc1694f)
    embed = await statPage({f"{ctx.guild.id}": item}, embed, 1, [])
    await ctx.respond(embed=embed)

@leaderboard.command(name='public', description='See the public leaderboard')
@discord.option('sort', choices=['Score', 'Reacte', 'DM', 'Golden'], required=True, defualt='score')
async def publicleaderboard(ctx, sort):
    await ctx.respond('One Moment')
    leader = await leaderboardMaker(ctx.guild.id, sort, 1)
    await ctx.edit(content=leader[0],embed=leader[1], view=leader[2])

async def leaderboardMaker(guildid, sort, page):
    optoutlist = ['opt']
    with open('guilds/opt/out.txt', 'r') as file:
        for line in file.readlines():
            optoutlist.append(line.replace('\n', ''))
        file.close()
    if str(guildid) in optoutlist:
        optoutlist.remove(str(guildid))
    stuff = {}
    for item in os.listdir('guilds'):
        if item != 'opt':
            items = await statCounter(item)
            stuff[F'{item}'] = items
    stuff = dict(sorted(stuff.items(), key=lambda bleh: bleh[1][f'{sort.lower()}'], reverse=True))
    for item in stuff:
        stuff[f'{item}']['pos'] = list(stuff).index(item)
    embed = discord.Embed(title=f"Public Leaderboard: Top **{sort}**", color=0xc1694f)
    embed = await statPage(stuff, embed, page, optoutlist)
    view = buttonPick(embed.footer)
    return '',embed, view
    
async def statCounter(guildid):
    tylist = ['dm', 'golden', 'reacte']
    countlist = {"dm": 0, "golden": 0, "reacte": 0, "score": 0}
    for item in tylist:
        with open(f'guilds/{guildid}/{item}.txt') as file:
            data = file.read()
            file.close()
        countlist[item] = int(data)
    countlist['score'] = countlist['reacte'] + (countlist['golden']*100) + (countlist['dm']*5)
    return countlist

async def statPage(stuff, embed: discord.Embed, page, oulist):
    skip = 0
    for item in stuff:
        if ((page-1)*10) <= list(stuff).index(item) < ((page*10)+skip):
            itemdic = stuff[f'{item}']
            if item == '-1':
                name = "DM'S"
            elif item == '1043241661179900074':
                name = "Urn 2 Version 1"
            else:
                try:
                    name = (await bot.fetch_guild(int(item))).name
                except:
                    name = f'Unknown Server [{item}]'
            if item not in oulist:
                embed.add_field(name=f"**{(list(stuff).index(item))+1}.** **{name}**", value=f'> **Score:** {itemdic["score"]} | {itemdic["reacte"]}:urn: | {itemdic["dm"]}<:urndm:1299043301873291335> | {itemdic["golden"]}<:golden_urn:1298534134565568512>', inline=False)
            else:
                skip = skip+1
    embed.add_field(name='** **',value="-# :urn:**=**reactions|<:urndm:1299043301873291335>**=**:urn:'s dm'd|<:golden_urn:1298534134565568512>**=**golden :urn:'s", inline=False)
    embed.set_footer(text=f'Page {page} of {await tpage(len(stuff)-skip)}')
    return embed

async def tpage(page):
    if len(str(page)) == 1:
        total = '1'
    else:
        total = (str(page))[:-1]
    return total

#urn

@bot.message_command(name='urn')
async def messageUrn(ctx, message: discord.Message):
    dm = bot.get_user(message.author.id)
    response = await dmUrn(dm, ctx.guild.id)
    await ctx.respond(response, ephemeral=True)

@bot.slash_command(name='urn', description="⚱")
@discord.option('urn', discord.Member, description="Choose Someone to ⚱", required=True)
async def slashUrn(ctx, urn):
    dm = bot.get_user(urn.id)
    response = await dmUrn(dm, ctx.guild.id)
    await ctx.respond(response, ephemeral=True)

@bot.user_command(name='urn')
async def userUrn(ctx, user: discord.User):
    dm = bot.get_user(user.id)
    response = await dmUrn(dm, ctx.guild.id)
    await ctx.respond(response, ephemeral=True)

@bot.event
async def on_message_edit(message_before, message_after):
    message = bot.get_message(message_after.id)
    await reacteUrn(message)

@bot.event
async def on_message(message):
    await reacteUrn(message)
    await bot.process_commands(message) 

async def reacteUrn(message):
    if message.author.id != bot.user.id:
        if "⚱" in message.content:
            await message.add_reaction("⚱")
        elif "u" in message.content.lower():
            if "r" in message.content.lower():
                if "n" in message.content.lower():
                    if isinstance(message.channel, discord.channel.DMChannel):
                        guildid = -1
                    else:
                        guildid = message.guild.id
                    if await goldenUrn(message, guildid, 'reacte') == False:
                        await message.add_reaction("⚱")
                    await writeStats(guildid, 'reacte')
                    await activityupdater(0)

async def dmUrn(dm, guildid):
    try:
        if await goldenUrn(dm, guildid,'dm') == False:
            await dm.send("⚱")
        await writeStats(guildid, 'dm')
        await activityupdater(1)
        return f"<@{dm.id}> has been ⚱ed"
    except:
        return f"an error accured 🥴"
    
async def goldenUrn(item, guildid, type):
    if random.randint(1,10000) <= 3:
        if type == 'reacte':
            await item.add_reaction('<:golden_urn:1298534134565568512>')
        if type == 'dm':
            await item.send('<:golden_urn:1298534134565568512>')
        await writeStats(guildid, 'golden')
        await activityupdater(2)
    else:
        return False

async def writeStats(guildid, type):
    try:
        with open(f'guilds/{guildid}/{type}.txt', 'r') as file:
            data = file.read()
            file.close()
    except:
        data = 0
    try:
        number = int(data)
    except:
        return 'error'
    with open(f'guilds/{guildid}/{type}.txt', 'w') as file:
        file.write(str(number+1))
        file.close()

async def readStats(type, exclusion):
    number = 0
    if exclusion == True:
        with open('/guilds/opt/out.txt') as file:
            exlist = file.readlines()
    if exclusion == False:
        exlist = ['0']
    alllist = os.listdir('guilds')
    for i in alllist:
        if str(i) not in exlist:
            if str(i) != 'opt':
                with open(f'guilds/{str(i)}/{type}.txt', 'r') as file:
                    number = number + int(file.read())
                    file.close()
    return number

bot.add_application_command(leaderboard)
bot.run(os.getenv('TOKEN'))
