import requests
import discord
from discord.ext import commands
import pymongo
import urllib.parse


password = urllib.parse.quote_plus("mypassword")
cluster = pymongo.MongoClient(f"mongodb+srv://Onion8:{password}@cluster0.tbrc1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["Clash"]
collection = db["mongoData"]


client = commands.Bot(command_prefix = ".")

headers = {
    "Accept": "application/json",
    "authorization": "Bearer key"
    }


@client.event
async def on_ready():
    print("Bot is ready.")


@client.command()
async def clashBotHelp(ctx):

    await ctx.send("https://github.com/Onion38/Clash-of-Clans-Discord-Bot")


@client.command()
async def setplayertag(ctx, tag):


    if collection.find_one({"_id": ctx.author.id}) == None:
        collection.insert_one({"_id": ctx.author.id})
    collection.update_one({"_id": ctx.author.id}, {"$set": {"ptag": tag}})


    await ctx.send(f"Updated your tag to {tag}")


@client.command()
async def setclantag(ctx, tag):

    if collection.find_one({"_id": ctx.author.id}) == None:
        collection.insert_one({"_id": ctx.author.id})

    collection.update_one({"_id": ctx.author.id}, {"$set": {"ctag": tag}})


    await ctx.send(f"Updated your tag to {tag}")    


@client.command()
async def mytags(ctx):
    userTag = collection.find_one({"_id": ctx.author.id})
    
    try:
        ptag = userTag["ptag"]
    except:
        ptag = "NA"
    try:
        ctag = userTag["ctag"]
    except:
        ctag = "NA"
    await ctx.send(f"Player Tag: {ptag}\nClan Tag: {ctag}")


@client.command()
async def clanwar(ctx, tag=None):
    data = await sendClanWarRequest(tag, ctx.author.id)

    if data == {"reason": "accessDenied"}:
        await ctx.send("Clan does not make War Log Public")
        return


    if data["state"] == "preparation" or None:
        em = discord.Embed(title=f"{data['clan']['name']} vs {data['opponent']['name']}")
        em.add_field(name="State", value="PREPARATION")
        
    elif data["state"] == "notInWar" or data["state"] == "warEnded":
        em = discord.Embed(title="Clan Not in War.")

    else:
        em = discord.Embed(title=f"{data['clan']['name']} vs {data['opponent']['name']}")
        em.add_field(name="State", value="IN WAR")
        em.add_field(name="score", value=f"{data['clan']['stars']} - {data['opponent']['stars']}")
        for member in data["clan"]["members"]:
            try:
                attacksLeft = 2 - len(member["attacks"])
            except:
                attacksLeft = 2
            em.add_field(name=member["name"], value=attacksLeft)


    em.set_thumbnail(url=data["clan"]["badgeUrls"]["small"])


    await ctx.send(embed=em)



@client.command()
async def clanprofile(ctx, tag=None):
    data = await sendClanRequest(tag, ctx.author.id)


    em = discord.Embed(title=f"{data['name']} Clan Stats")
    em.set_thumbnail(url=data["badgeUrls"]["small"])
    em.add_field(name="Clan Level", value=data["clanLevel"])
    em.add_field(name="Clan Points", value=data["clanPoints"])
    em.add_field(name="Clan Versus Points", value=data["clanVersusPoints"])
    em.add_field(name="War Wins", value=data["warWins"])
    em.add_field(name="War League", value=data["warLeague"]["name"])

    await ctx.send(embed=em)


@client.command()
async def hometroops(ctx, tag=None):

    data = await sendPlayerRequest(tag, ctx.author.id)

    em = discord.Embed(title=f"{data['name']}'s Home Troops", color = discord.Color.purple())
    em.set_thumbnail(url=data["clan"]["badgeUrls"]["small"])
    for troop in data["troops"]:
        if troop['village'] == 'home':
            em.add_field(name=troop['name'], value=f"Level {troop['level']}/{troop['maxLevel']}")

    await ctx.send(embed=em)


@client.command()
async def buildertroops(ctx, tag=None):

    data = await sendPlayerRequest(tag, ctx.author.id)

    em = discord.Embed(title=f"{data['name']}'s Builder Troops", color = discord.Color.blue())
    em.set_thumbnail(url=data["clan"]["badgeUrls"]["small"])
    for troop in data["troops"]:
        if troop["village"] == "builderBase":
            em.add_field(name=troop['name'], value=f"Level {troop['level']}/{troop['maxLevel']}")

    await ctx.send(embed=em)


@client.command()
async def homeprofile(ctx, tag=None):

    data = await sendPlayerRequest(tag, ctx.author.id)


    em = discord.Embed(title=f"{data['name']}'s General Home Stats", color= discord.Color.purple())
    em.set_thumbnail(url=data["clan"]["badgeUrls"]["small"])
    em.add_field(name="ExpLevel", value=data['expLevel'])
    em.add_field(name="TownHallLevel", value=data["townHallLevel"])
    em.add_field(name="Clan", value=data["clan"]["name"])
    em.add_field(name="Trophies", value=data["trophies"])
    em.add_field(name="BestTrophies", value=data["bestTrophies"])

    await ctx.send(embed=em)


@client.command()
async def builderprofile(ctx, tag=None):
    data = await sendPlayerRequest(tag, ctx.author.id)

    em = discord.Embed(title=f"{data['name']}'s General Builder Stats", color= discord.Color.blue())
    em.set_thumbnail(url=data["clan"]["badgeUrls"]["small"])
    em.add_field(name="ExpLevel", value=data['expLevel'])
    em.add_field(name="BuilderHallLevel", value=data["builderHallLevel"])
    em.add_field(name="Clan", value=data["clan"]["name"])
    em.add_field(name="VersusTrophies", value=data["versusTrophies"])
    em.add_field(name="BestVersusTrophies", value=data["bestVersusTrophies"])

    await ctx.send(embed=em)

@client.command()
async def heroes(ctx, tag=None):
    data = await sendPlayerRequest(tag, ctx.author.id)

    em = discord.Embed(title=f"{data['name']}'s Heroes", color=discord.Color.green())
    em.set_thumbnail(url=data["clan"]["badgeUrls"]["small"])
    for hero in data["heroes"]:
        em.add_field(name=hero["name"], value=f"{hero['level']}/{hero['maxLevel']}")
    await ctx.send(embed=em)

@client.command()
async def spells(ctx, tag=None):
    data = await sendPlayerRequest(tag, ctx.author.id)

    em = discord.Embed(title=f"{data['name']}'s Spells", color=discord.Color.red())
    em.set_thumbnail(url=data["clan"]["badgeUrls"]["small"])
    for spell in data["spells"]:
        em.add_field(name=spell["name"], value=f"{spell['level']}/{spell['maxLevel']}")
    await ctx.send(embed=em)



async def sendClanWarRequest(tag, id):
    if tag == None:
        userData = collection.find_one({"_id": id})
        tag = userData['ctag']
    response = requests.get(f"https://api.clashofclans.com/v1/clans/%23{tag}/currentwar", headers=headers)
    return response.json()



async def sendClanRequest(tag, id):
    if tag == None:
        userData = collection.find_one({"_id": id})
        tag = userData['ctag']
    response = requests.get(f"https://api.clashofclans.com/v1/clans/%23{tag}", headers=headers)
    return response.json()



async def sendPlayerRequest(tag, id):
    if tag == None:
        userData = collection.find_one({"_id": id})
        tag = userData['ptag']
    response = requests.get(f"https://api.clashofclans.com/v1/players/%23{tag}", headers=headers)
    return response.json()




client.run("token")