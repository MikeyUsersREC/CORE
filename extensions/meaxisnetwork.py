from discord.ext import commands
import discord
import requests
core_color = discord.Color.from_rgb(30, 144, 255)

@commands.command()
async def myaccount(ctx):
	payload = {"discordid": ctx.author.id, "secret": "t6ovhm._7-ng9iry-1602428551-gy1pn37w.u06x8_q", "scope": "username"}
	usernameRequest = requests.get("https://api.meaxisnetwork.net/v2/accounts/fromdiscord/", params=payload)
	usernameJSON = usernameRequest.json()
	username = usernameJSON["message"]

	payload = {"discordid": ctx.author.id, "secret": "t6ovhm._7-ng9iry-1602428551-gy1pn37w.u06x8_q", "scope": "description"}
	descriptionRequest = requests.get("https://api.meaxisnetwork.net/v2/accounts/fromdiscord/", params=payload)
	descriptionJSON = descriptionRequest.json()
	description = descriptionJSON["message"]
	descriptionFixed = description.replace("\r", "")

	payload = {"discordid": ctx.author.id, "secret": "t6ovhm._7-ng9iry-1602428551-gy1pn37w.u06x8_q", "scope": "profilepicture"}
	avatarRequest = requests.get("https://api.meaxisnetwork.net/v2/accounts/fromdiscord/", params=payload)
	avatarJSON = avatarRequest.json()
	avatarURLSource = descriptionJSON["message"]
	avatarURLString = str(avatarURLSource)
	avatarURLFixed = avatarURLString.replace(r'\/','/')

	payload = {"discordid": ctx.author.id, "secret": "t6ovhm._7-ng9iry-1602428551-gy1pn37w.u06x8_q", "scope": "id"}
	accountIDRequest = requests.get("https://api.meaxisnetwork.net/v2/accounts/fromdiscord/", params=payload)
	accountIDJSON = accountIDRequest.json()
	AccountID = accountIDJSON["message"]

	embed = discord.Embed(title=username, color=core_color)
	embed.add_field(name = "Description", value = description)
	embed.add_field(name = "Account ID", value = AccountID)
	embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
	await ctx.send(embed=embed)

@commands.command()
async def funfact(ctx):
	funfactRequest = requests.get("https://api.meaxisnetwork.net/v2/funfact/")
	funfactJSON = funfactRequest.json()
	funfact = funfactJSON["text"]
	funfactID = funfactJSON["id"]
	funfactAuthor = funfactJSON["author"]
	
	embed = discord.Embed(title=f"Funfact #{funfactID}", color=core_color)
	embed.add_field(name = "Funfact:", value = funfact)
	embed.add_field(name = "Author", value = funfactAuthor)
	embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
	await ctx.send(embed=embed)

@command.command()
async def leafy(ctx):
	leafyRequest = requests.get("https://api.meaxisnetwork.net/v2/leafy/")
	embed = discord.Embed(title=f"Leafy API Status", color=core_color)
	embed.add_field(name = "Status:", value = status_code)
	embed.add_field(name = "Note:", value = "If the status is 200, then the leafy API is online.")
	embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
	await ctx.send(embed=embed)
	return

@commands.command()
async def funfact(ctx):
	funfactRequest = requests.get("https://api.meaxisnetwork.net/v2/funfact/")
	funfactJSON = funfactRequest.json()
	funfact = funfactJSON["text"]
	funfactID = funfactJSON["id"]
	funfactAuthor = funfactJSON["author"]
	
	embed = discord.Embed(title=f"Funfact #{funfactID}", color=core_color)
	embed.add_field(name = "Funfact:", value = funfact)
	embed.add_field(name = "Author", value = funfactAuthor)
	embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
	await ctx.send(embed=embed)



def setup(bot):
    bot.add_command(myaccount)
    bot.add_command(funfact)
    bot.add_command(leafy)