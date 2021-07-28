import requests
import discord
from discord.ext import commands


headers = {
    "Accept": "application/json",
    "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjkxZTkwZjk0LTYwMTYtNGJhZC04YjcwLTM0OTlkNjc3NzI3NiIsImlhdCI6MTYyNzQ1MDgyNiwic3ViIjoiZGV2ZWxvcGVyLzU2NGIwYzI4LTk3ODQtMTRkZC1iNWRjLTk2NGRhOWZhMzY4MSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjE3My4xOC41OC4xMjYiXSwidHlwZSI6ImNsaWVudCJ9XX0.-rsPkHoWxrFaMCD1NDBDABLWz8ftmIW-QwJz71xwNwtcRSRhFaBSvBuJL6NBTURmnNypxk0hwq7Y-B0w_4648w"
    }




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




client.run("ODY5ODI4OTQ0OTYxMTA1OTkx.YQD5VQ.UEbB6hSFoaTkkVxCkmZO6WENByY")