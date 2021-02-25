import discord
from discord.ext import commands
from datetime import datetime

core_color = discord.Color.from_rgb(30, 144, 255)


class Information(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	@commands.command(name="support", description="Invites you to the CORE Support Server.", usage="support")
	async def support(self, ctx):
		embed = discord.Embed(title="Support", description="Support Server: https://discord.gg/YH8WQCT", color=core_color)
		embed.set_thumbnail(url=ctx.bot.user.avatar_url)
		await ctx.author.send(embed=embed)

	@commands.command(name="invite", description="Sends you the invite link for the CORE Bot.", usage="invite")
	async def invite(self, ctx):
	    embed = discord.Embed(title="Bot Invite", description="https://discord.com/api/oauth2/authorize?client_id=734495486723227760&permissions=8&scope=bot", color=core_color)
	    embed.set_thumbnail(url=ctx.bot.user.avatar_url)
	    await ctx.author.send(embed=embed)

	@commands.command(name="uptime", description="Tells you how long CORE has been online.", usage="invite")
	async def uptime(self, ctx):
	    delta_uptime = datetime.utcnow() - self.bot.launch_time
	    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
	    minutes, seconds = divmod(remainder, 60)
	    days, hours = divmod(hours, 24)
	    await ctx.send(f"{days}d, {hours}h, {minutes}m, {seconds}s")

	@commands.command(name="version", description="Gives you information about the most recent update", usage="version")
	async def version(self, ctx):
	    updateEmbed = discord.Embed(title="Most recent version:", description="Version 1.1.9\n\n- Fixed some bugs.\n- Added image manipulation.", color=core_color)
	    updateEmbed.set_thumbnail(url=ctx.bot.user.avatar_url)
	    await ctx.send(embed=updateEmbed)

def setup(bot):
	bot.add_cog(Information(bot))