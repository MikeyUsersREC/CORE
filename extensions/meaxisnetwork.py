import discord
from discord.ext import commands
import requests
from datetime import datetime
import json

mn_color = discord.Color.from_rgb(35, 35, 35)
meaxisnetwork_url = "https://meaxisnetwork.net/assets/images/square_logo.png"


class MeaxisNetwork(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")


	def is_an_enabled_guild():
		async def predicate(ctx):
			dataset = await ctx.bot.enabledPerGuildExtension.find_by_id(ctx.guild.id)
			try:
				return dataset != None and dataset["meaxisnetwork"]
			except:
				for key, value in dataset.items():
					if key == "meaxisnetwork" and value == True:
						return True
		return commands.check(predicate)

	@commands.command()
	@is_an_enabled_guild()
	async def profile(self, ctx):
		APIRequest = requests.get(f"https://api.meaxisnetwork.net/v3/users/search/?query={ctx.author.id}&from=discord")
		APIJSON = APIRequest.json()
		username = APIJSON["username"]
		color = mn_color
		if APIJSON["highestTitleColor"]:
			color = discord.Colour(int(APIJSON["highestTitleColor"].replace("#", "0x"), 16))
		embed = discord.Embed(title = username , color = color)
		for key, value in APIJSON.items():
			vars()[key.capitalize()] = value
			if key != "joinedOn" and value != "":
				embed.add_field(name = key.capitalize(), value = f"{value}", inline = False)
			if key == "joinedOn":
				embed.add_field(name = key.capitalize(), value = f"{datetime.fromtimestamp(value)}", inline = False)

		avatar = APIJSON["avatar"].replace("\\", "")

		embed.set_thumbnail(url=avatar)
		await ctx.send(embed=embed)

	@commands.command()
	@is_an_enabled_guild()
	async def funfact(self, ctx):
		funfactRequest = requests.get("https://api.meaxisnetwork.net/v2/funfact/")
		funfactJSON = funfactRequest.json()
		funfact = funfactJSON["text"]
		funfactID = funfactJSON["id"]
		funfactAuthor = funfactJSON["author"]
		
		embed = discord.Embed(title=f"Funfact #{funfactID}", color=mn_color)
		embed.add_field(name = "Funfact:", value = funfact, inline = False)
		embed.add_field(name = "Author", value = funfactAuthor, inline = False)
		embed.set_thumbnail(url=meaxisnetwork_url)
		await ctx.send(embed=embed)

	@commands.command()
	@is_an_enabled_guild()
	async def leafy(self, ctx):
		leafyRequest = requests.get("https://api.meaxisnetwork.net/v2/leafy/")
		embed = discord.Embed(title=f"Leafy API Status", color=mn_color)
		if leafyRequest.status_code == 200:
			embed.add_field(name = "Status:", value ="Online", inline = False)
		else:
			embed.add_field(name = "Status:", value ="Offline", inline = False)
		embed.set_thumbnail(url=meaxisnetwork_url)
		await ctx.send(embed=embed)
		return

	@commands.command()
	@is_an_enabled_guild()
	async def finduser(self, ctx, username, privateBeta = False):
		if privateBeta in ["True", "true"]:
			privateBeta = True
		elif privateBeta in ["False", "false"]:
			privateBeta = False
		try:
			dataset = await self.bot.enabledPerGuildExtension.find_by_id(ctx.guild.id)
			data = dataset["0f128am-1823301-191y9-q77r61-09a99qm-oaowiqu7-177a"]
		except:
			data = False
		if privateBeta and data:
			await ctx.send('Authorisation has been given.', delete_after = 2)
			await ctx.message.delete()
		APIRequest = requests.get(f"https://api.meaxisnetwork.net/v3/users/search/?query={username}&from=username")
		APIJSON = None
		try:
			APIJSON = APIRequest.json()
			APIJSON["username"]
		except:
			member = discord.utils.get(ctx.guild.members, name = username)
			if member == None:
				member = await ctx.guild.fetch_member(username.strip("<!@>"))
				APIJSON = requests.get(f"https://api.meaxisnetwork.net/v3/users/search?from=discord&query={member.id}").json()
			else:
				APIJSON = requests.get(f"https://api.meaxisnetwork.net/v3/users/search?from=discord&query={member.id}").json()
		username = APIJSON["username"]
		color = mn_color
		if APIJSON["highestTitleColor"]:
			color = discord.Colour(int(APIJSON["highestTitleColor"].replace("#", "0x"), 16))
		embed = discord.Embed(title = username , color = color)
		for key, value in APIJSON.items():
			vars()[key.capitalize()] = value
			if key != "joinedOn" and value != "":
				embed.add_field(name = key.capitalize(), value = f"{value}", inline = False)
			if key == "joinedOn":
				embed.add_field(name = key.capitalize(), value = f"{datetime.fromtimestamp(value)}", inline = False)

		avatar = APIJSON["avatar"].replace("\\", "")

		embed.set_thumbnail(url=avatar)
		if privateBeta and data:
			await ctx.author.send(embed = embed)
			id = APIJSON["id"]
			creations = requests.get(f"https://api.meaxisnetwork.net/v3/users/{id}/creations").json()
			applications = requests.get(f"https://api.meaxisnetwork.net/v3/users/{id}/applications").json()
			activity = requests.get(f"https://api.meaxisnetwork.net/v3/users/{id}/activity").json()
			activity = "\nActivity: \n\n" + str(activity)[:1900] + "...\n"
			applications = "\nApplications: \n\n" + str(applications)[:1900] + "...\n"
			creations = "\nCreations:\n \n" + str(creations)[:1900] + "...\n"
			await ctx.author.send(applications)
			await ctx.author.send(activity)
			await ctx.author.send(creations)
			return
		await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(MeaxisNetwork(bot))
