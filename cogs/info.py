
import discord
from discord.ext import commands
from datetime import datetime
import time
import gpiozero
import psutil

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
		updateEmbed = discord.Embed(title="Version History", color=core_color)
		updateEmbed.add_field(name = "Version 1.20", value = "Patches:\n\n- Moved from Cloud Hosting to MikeyCorporation CSA\n- Extended Image Manipulation\n- Added the audit log command\n- Added the Python Programming commands to CORE allowing cheatsheet APIs to be used to gain information about python\n- Added a new 'Enable / Disable' Database to allow Extensions to be used server wide instead of previously global extensions.\n- Added more support for extensions ranging from configuration changes to entire command groups being added.", inline = False)
		updateEmbed.add_field(name = "Version 1.19", value = "Minor Changes:\n\n- Added the Image Manipulation Cog\n- Fixing bugs with announce command among others in that group", inline = False)
		updateEmbed.add_field(name = "Version 1.18", value = "New commands: \n\n- Added an 8ball command.\n- Added a better help command.\n- Added a better way of updating CORE without having to restart it.", inline = False)
		updateEmbed.add_field(name = "Version 1.17", value = "Not Available due to Github Corruption.", inline = False)
		updateEmbed.add_field(name = "Version 1.16", value = "Patches: \n\n- Information command now offers more information regarding their member such as their highest role, when they joined the server, their ID and their nickname on the server alongside other things.", inline = False)
		updateEmbed.add_field(name = "Version 1.15", value = "New commands: \n\n- New prefix command which you can change the prefix and view the current prefix for your server. This will also modify the help command to also include the server prefix in the command name rather than the default '!'.\n\n- Verify command fixed and can now function properly.", inline = False)
		updateEmbed.set_thumbnail(url=ctx.bot.user.avatar_url)
		updateEmbed.set_footer(text = "Version History | CORE", icon_url = self.bot.user.avatar_url)
		await ctx.send(embed=updateEmbed)

	@commands.command(name="ping", description="Gives you the current ping of the bot.", usage="ping")
	async def ping(self, ctx):
		before = time.monotonic()
		message = await ctx.send("Pong!")
		ping = (time.monotonic() - before) * 1000
		await message.edit(content=f"Pong!  `{int(ping)}ms`")

	@commands.command(name = "stats", description = "Gives you the stats of the bot.", aliases = ["botstats"], usage = "stats")
	async def _stats(self, ctx):
		embed = discord.Embed(title = "CORE Server Alpha", color = core_color)
		disk_usage = f"{round(gpiozero.DiskUsage().usage, 1)}%"
		cpu_temp = f"{gpiozero.CPUTemperature().temperature} Degrees (Celcius)"
		memory = psutil.virtual_memory()
		memory_usage = f"{round(memory.available/1024.0/1024.0, 1)} / {round(memory.total/1024.0/1024.0, 1)} MB"
		embed.add_field(name = "CPU Temperature", value = cpu_temp, inline = False)
		embed.add_field(name = "Disk Usage", value = disk_usage, inline = False)
		embed.add_field(name = "Memory Usage", value = memory_usage, inline = False)
		ChannelData = []
		MemberData = []
		for guild in self.bot.guilds:
			for channel in guild.channels:
				ChannelData.append(channel)
			for member in guild.members:
				MemberData.append(member)
		Channels = len(ChannelData)
		Members = len(MemberData)
		embed.add_field(name = "Servers", value = f"{len(self.bot.guilds)} Servers")
		embed.add_field(name = "Channels", value = f"{Channels} Channels", inline = False)
		embed.add_field(name = "Members", value = f"{Members} Members", inline = False)
		embed.set_thumbnail(url=self.bot.user.avatar_url)
		await ctx.send(embed = embed)


def setup(bot):
	bot.add_cog(Information(bot))
