import requests
import discord
from discord.ext import commands


headers = {
    "Accept": "application/json",
    "authorization": "Bearer key"




client = commands.Bot(command_prefix = ".")



@client.event
async def on_ready():
    print("Bot is ready.")

@client.command()
async def htroops(ctx, tag):

    data = await sendRequest(tag)

    em = discord.Embed(title=f"{data['name']}'s Home Troops", color = discord.Color.purple())
    for troop in data["troops"]:
        if troop['village'] == 'home':
            em.add_field(name=troop['name'], value=f"Level {troop['level']}")

    await ctx.send(embed=em)

@client.command()
async def btroops(ctx, tag):

    data = await sendRequest(tag)

    em = discord.Embed(title=f"{data['name']}'s Builder Troops", color = discord.Color.blue())
    for troop in data["troops"]:
        if troop["village"] == "builderBase":
            em.add_field(name=troop['name'], value=f"Level {troop['level']}")

    await ctx.send(embed=em)


@client.command()
async def hgen(ctx, tag):

    data = await sendRequest(tag)


    em = discord.Embed(title=f"{data['name']}'s General Home Stats", color= discord.Color.purple())
    em.add_field(name="ExpLevel", value=data['expLevel'])
    em.add_field(name="TownHallLevel", value=data["townHallLevel"])
    em.add_field(name="Trophies", value=data["trophies"])
    em.add_field(name="BestTrophies", value=data["bestTrophies"])

    await ctx.send(embed=em)

@client.command()
async def bgen(ctx, tag):
    data = await sendRequest(tag)

    em = discord.Embed(title=f"{data['name']}'s General Builder Stats", color= discord.Color.blue())
    em.add_field(name="ExpLevel", value=data['expLevel'])
    em.add_field(name="BuilderHallLevel", value=data["builderHallLevel"])
    em.add_field(name="VersusTrophies", value=data["versusTrophies"])
    em.add_field(name="BestVersusTrophies", value=data["bestVersusTrophies"])

    await ctx.send(embed=em)




async def sendRequest(tag):
    response = requests.get(f"https://api.clashofclans.com/v1/players/%23{tag}", headers=headers)
    return response.json()




client.run("token")
