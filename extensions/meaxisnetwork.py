import discord
from discord.ext import commands

mn_color = discord.Color.from_rgb(35, 35, 35)
meaxisnetwork_url = "https://meaxisnetwork.net/assets/images/square_logo.png"


class MeaxisNetwork(commands.Cog):
	 def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	@commands.command()
	async def profile(ctx):
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

		embed = discord.Embed(title=username, color=mn_color)
		embed.add_field(name = "Description", value = description, inline = False)
		embed.add_field(name = "Account ID", value = AccountID, inline = False)
		embed.set_thumbnail(url=meaxisnetwork_url)
		await ctx.send(embed=embed)

	@commands.command()
	async def funfact(ctx):
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
	async def leafy(ctx):
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
	async def finduser(ctx, username):
		payload = {"username": username}
		usernameRequest = requests.get("https://api.meaxisnetwork.net/v2/accounts/exists/", params=payload)
		usernameJSON = usernameRequest.json()
		usernameResult = usernameJSON["message"]
		embed = discord.Embed(title="User Result", color=mn_color)
		embed.add_field(name = "Username Entered:", value = username, inline = False)
		embed.add_field(name = "Result:", value = usernameResult, inline = False)
		embed.set_thumbnail(url=meaxisnetwork_url)
		await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(MeaxisNetwork(bot))