import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
import random
from inspect import getmembers, ismethod

core_color = discord.Color.from_rgb(30, 144, 255)

class Utility(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="roll", aliases=["choose", "randommember"], description="Picks a random member from the server.", usage="roll")
	async def roll(self, ctx):
		randomMember = choice(ctx.author.guild.members)
		if randomMember != bot.user:
			await ctx.send(f'{randomMember.mention} has been chosen.')
		else:
			randomMember = choice(ctx.author.guild.members)

	@commands.command(name="countdown", aliases=["cd", "timer"], description="Initiates a timer and mentions you when it is finished.", usage="countdown <Time | s/m/h/d>")
	async def countdown(self, ctx, time):
		if str(time).endswith("s"):
			timeList = time.split("s")
			timeDown = int(timeList[0])
		elif str(time).endswith("m"):
			timeList = time.split("m")
			timeDown = int(timeList[0]) * 60
		elif str(time).endswith("h"):
			timeList = time.split("h")
			timeDown = int(timeList[0]) * 60 * 60
		elif str(time).endswith("d"):
			timeList = time.split("d")
			timeDown = int(timeList[0]) * 60 * 60 * 24
		else:
			return
		await asyncio.sleep(timeDown)
		embed = discord.Embed(title="Timer is up", description=f"The timer you set for {time} has ended.", color=core_color)
		embed.set_thumbnail(url=ctx.bot.user.avatar_url)
		await ctx.send(f"{ctx.author.mention}", embed=embed)
		return


	@commands.command(name="userinfo", description="Gets the information of the mentioned user.", aliases=["getuser", "get_user", "getinfo"], usage="userinfo <User>")
	async def userinfo(self, ctx, *, member: discord.Member):
		infoEmbed = discord.Embed(title=f"{member.name} | User Information", color=core_color)
		for key, value in vars(member.__class__).items():
				if hasattr(member, key) and not getmembers(member, lambda x: not ismethod(x)):
						attr = getattr(member, key, "DNE")
						await ctx.send(f"{key}: {attr}")
						await asyncio.sleep(1)
		infoEmbed.set_thumbnail(url=member.avatar_url)
		await ctx.send(embed=infoEmbed)


	@commands.command(name="serverinfo", description="Gets the information of the mentioned user.", aliases=["guildinfo", "getguild", "getguildinfo"], usage="serverinfo")
	async def serverinfo(self, ctx):
		infoEmbed = discord.Embed(title=f"{ctx.guild.name} | Server Information", color=core_color)
		for key, value in vars(ctx.guild).items():
			try:
				infoEmbed.add_field(name = key.capitalize().replace("_", " "), value = f"{value.replace()}", inline = False)
			except:
				pass

		infoEmbed.set_thumbnail(url=ctx.guild.icon_url)
		await ctx.send(embed=infoEmbed)


	@commands.command(name="prefix", aliases=["changeprefix", "viewprefix"], description="Changes your server prefix.", usage="prefix <Prefix>")
	@has_permissions(manage_guild=True)
	async def prefix(self, ctx, arg=None):
		if arg == None:
			dataset = await self.bot.prefixData.find_by_id(ctx.guild.id)
			prefix = dataset["prefix"]
			await ctx.send(f"My prefix is `{prefix}`")
		else:
			dataset = await self.bot.prefixData.find_by_id(ctx.guild.id)
			dataset["prefix"] = arg
			await self.bot.prefixData.update_by_id(dataset)
			await ctx.send(f"My prefix has been changed to `{arg}`")




def setup(bot):
	bot.add_cog(Utility(bot))