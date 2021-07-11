import discord
from discord.ext import commands
import requests
core_color = discord.Color.from_rgb(30, 144, 255)




class Roblox(commands.Cog, name = "Roblox Commands"):
	def __init__(self, bot):
		self.bot = bot

	def is_an_enabled_guild():
		async def predicate(ctx):
			dataset = await ctx.bot.enabledPerGuildExtension.find_by_id(ctx.guild.id)
			return dataset != None and dataset["roblox"]
		return commands.check(predicate)

	@commands.command()
	async def robloxsearch(self, ctx, arg1=None):
		if arg1 == None:
			embed = discord.Embed(title="An error has occured.", description="An error has occured that has prevented the command to run properly.", color=core_color)
		else:
			if not arg1 == None:
				payload = {"username": arg1}
				infoRequest = requests.get(f"https://api.roblox.com/users/get-by-username?username={arg1}")
				infoJSON = infoRequest.json()
				userid = infoJSON["Id"]
				NewInfoRequest = requests.get(f"https://users.roblox.com/v1/users/{userid}")
				NewInfoJSON = NewInfoRequest.json()

				embed = discord.Embed(title="Roblox Search")

				for key, value in NewInfoJSON.items():
					if value != "" and key != "created":
						embed.add_field(name = key.capitalize(), value = f"{value}", inline = False)
					elif key == "created":
						createdSplit = value.split("T")
						created = createdSplit[0]

						embed.add_field(name = "Created At", value = f"{created}", inline = False)

				statusRequest = requests.get(f"https://users.roblox.com/v1/users/{userid}/status")
				statusJSON = statusRequest.json()
				status = statusJSON["status"]
	

				if status != "":
					embed.add_field(name = "Status", value = f"{status}", inline = False)



				embed.color =  core_color
				headshot_url = f"https://www.roblox.com/headshot-thumbnail/image?userId={userid}&width=420&height=420&format=png"
				embed.set_thumbnail(url=headshot_url)
				embed.set_footer(text="Roblox |  CORE", icon_url=self.bot.user.avatar_url)
				await ctx.send(embed=embed)


	@commands.command()
	async def assetsearch(self, ctx, arg1=None):
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

			embed.color =  core_color
			embed.set_thumbnail(url=self.bot.user.avatar_url)
			embed.set_footer(text="Roblox |  CORE", icon_url=self.bot.user.avatar_url)
			await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Roblox(bot))

