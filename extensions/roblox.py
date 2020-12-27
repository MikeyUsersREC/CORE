import discord
from discord.ext import commands
import requests
core_color = discord.Color.from_rgb(30, 144, 255)


@commands.command()
async def robloxsearch(ctx, arg1=None):
	if arg1 == None:
		embed = discord.Embed(title="An error has occured.", description="An error has occured that has prevented the command to run properly.", color=core_color)
	else:
		if not arg1 == None:
			payload = {"username": arg1}
			infoRequest = requests.get("https://api.roblox.com/users/get-by-username", params=payload)
			infoJSON = infoRequest.json()
			isOnline = infoJSON["IsOnline"]
			userid = infoJSON["Id"]
			username = infoJSON["Username"]


			newPayload = {"username": username}
			NewInfoRequest = requests.get(f"https://users.roblox.com/v1/users/{userid}", params=newPayload)
			NewInfoJSON = NewInfoRequest.json()

			description = NewInfoJSON["description"]
			isBanned = NewInfoJSON["isBanned"]
			createdUnSplit = NewInfoJSON["created"]

			createdSplit = createdUnSplit.split("T")
			created = createdSplit[0]

			embed = discord.Embed(title="Roblox Search")

			statusRequest = requests.get(f"https://users.roblox.com/v1/users/{userid}/status")
			statusJSON = statusRequest.json()
			status = statusJSON["status"]

			embed.add_field(name="Username", value=f"{username}", inline=False)
			embed.add_field(name="User ID", value=f"{userid}", inline=False)
			embed.add_field(name="Description", value=f"{description}", inline=False)
			embed.add_field(name="Created", value=f"{created}", inline=False)

			if isBanned == False:
				embed.add_field(name="Banned", value="Not Banned", inline=False)
			else:
				embed.add_field(name="Banned", value="Banned", inline=False)


			if isOnline == True:
				embed.add_field(name="IsOnline", value="Online", inline=False)
			else:
				embed.add_field(name="IsOnline", value="Offline", inline=False)
		
			embed.add_field(name="Status", value=f"{status}", inline=False)




			embed.color = core_color
			headshot_url = f"https://www.roblox.com/headshot-thumbnail/image?userId={userid}&width=420&height=420&format=png"
			embed.set_thumbnail(url=headshot_url)
			embed.set_footer(text="Roblox | CORE", icon_url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
			await ctx.send(embed=embed)


@commands.command()
async def assetsearch(ctx, arg1=None):
	if arg1 == None:
		return
	else:
		payload = {"assetId": int(arg1)}
		assetRequest = requests.get(f"https://api.roblox.com/marketplace/productinfo", params=payload)
		assetJSON = assetRequest.json()
		name = assetJSON["Name"]
		description = assetJSON["Description"]
		creator = assetJSON["Creator"]["Name"]
		price = assetJSON["PriceInRobux"]
		limited = assetJSON["IsLimited"]
		createdUnSplit = assetJSON["Created"]
		createdSplit = createdUnSplit.split("T")
		created = createdSplit[0]

		embed = discord.Embed(title="Asset Search", color=core_color)

		embed.add_field(name="Name", value=f"{name}", inline=False)
		embed.add_field(name="Description", value=f"{description}", inline=False)
		embed.add_field(name="Creator", value=f"{creator}", inline=False)

		if limited == True:
			embed.add_field(name="Limited", value=f"Yes", inline=False)
		else:
			embed.add_field(name="Limited", value=f"No", inline=False)

		embed.add_field(name="Created", value=f"{created}", inline=False)

		embed.color = core_color
		embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
		embed.set_footer(text="Roblox | CORE", icon_url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
		await ctx.send(embed=embed)

def setup(bot):
    bot.add_command(robloxsearch)
    bot.add_command(assetsearch)