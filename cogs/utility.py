import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
import random

core_color = discord.Color.from_rgb(30, 144, 255)

class Utility(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

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


	@commands.command(name="info", description="Gets the information of the mentioned user.", aliases=["getinfo"], usage="info <User>")
	async def info(self, ctx, *, member: discord.Member):
	    description = f"Name: {member.display_name}\nNickname: {member.nick}\nID: {member.id}\nRoles: {len(member.roles)}\nJoined At: {member.joined_at}\nStatus: {member.raw_status}\nHighest Role: {member.top_role.name}"
	    infoEmbed = discord.Embed(title="information", description=description, color=core_color)
	    infoEmbed.set_thumbnail(url=member.avatar_url)
	    await ctx.send(embed=infoEmbed)

	@commands.command(name="prefix", aliases=["changeprefix", "viewprefix"], description="Changes your server prefix.", usage="prefix <Prefix>")
	@has_permissions(manage_guild=True)
	async def prefix(self, ctx, arg=None):
		if arg == None:
			dataset = await bot.prefixData.find_by_id(ctx.guild.id)
			prefix = dataset["prefix"]
			await ctx.send(f"My prefix is `{prefix}`")
		else:
			dataset = await bot.prefixData.find_by_id(ctx.guild.id)
			dataset["prefix"] = arg
			await bot.prefixData.update_by_id(dataset)
			await ctx.send(f"My prefix has been changed to `{arg}`")

	@commands.command(name="load", aliases=["loadextension", "loadext"], description="Loads the extension you provide.", usage="load <Extension>")
	async def load(self, ctx, extension):
	    extensionLowered = extension.lower()
	    try:
	    	bot.load_extension(f'extensions.{extensionLowered}')
	    	embed = discord.Embed(title="Extension loaded!", description=f"{extensionLowered}.py was loaded.", color=core_color)
	    except Exception as e:
	    	embed = discord.Embed(title="Extension could not be loaded!", description=f"{extensionLowered}.py could not be loaded as it does not exist.", color=core_color)
	    embed.set_thumbnail(url=ctx.bot.user.avatar_url)
	    await ctx.send(embed=embed)

	@commands.command(name="unload", aliases=["unloadextension", "unloadext"], description="Unloads the extension you provide.", usage="unload <Extension>")
	async def unload(self, ctx, extension):
	    bot.unload_extension(f'extensions.{extension}')

	@commands.command(name="reload", aliases=["reloadextension", "reloadext"], description="Reloads the extension you provide.", usage="reload <Extension>")
	async def reload(self, ctx, extension):
	    bot.unload_extension(f'extensions.{extension}')
	    bot.load_extension(f'extensions.{extension}')


def setup(bot):
	bot.add_cog(Utility(bot))