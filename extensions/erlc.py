import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, has_role

from datetime import datetime

core_color = discord.Color.from_rgb(30, 144, 255)

class ERLC(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	def is_an_enabled_guild():
		async def predicate(ctx):
			dataset = await ctx.bot.enabledPerGuildExtension.find_by_id(ctx.guild.id)
			return dataset != None and dataset["erlc"]
		return commands.check(predicate)

	def has_staff():
		async def predicate(ctx):
			dataset = await ctx.bot.config.find_by_id(ctx.guild.id)
			try:
				role = dataset["staff_role"]
				role = discord.utils.get(ctx.guild.roles, name = role)
			except:
				return False
			return role in ctx.author.roles
		return commands.check(predicate)


	@commands.command()
	@is_an_enabled_guild()
	@has_staff()
	async def duty(self, ctx, arg1="On-Duty"):
		dataset = await ctx.bot.config.find_by_id(ctx.guild.id)
		channel = discord.utils.get(ctx.message.channel.guild.text_channels , name=dataset["duty_channel"])
		embed = discord.Embed(title="Duty Changed", color=core_color)
		embed.add_field(name="Name", value=ctx.author.name, inline=False)
		if arg1.lower() == "off" or arg1 == "off-duty":
			embed.add_field(name="Status", value="Off-Duty", inline=False)
		else:
			embed.add_field(name="Status", value="On-Duty", inline=False)
		embed.add_field(name="Time", value=f"{datetime.utcnow()}")
		embed.set_thumbnail(url=str(ctx.message.author.avatar_url))
		await channel.send(embed=embed)

	@commands.command(name="code", aliases=["server_code", "getservercode"])
	@is_an_enabled_guild()
	async def code(self, ctx):
		dataset = await ctx.bot.config.find_by_id(ctx.guild.id)
		embed = discord.Embed(title="Server Code", color=core_color)
		embed.set_thumbnail(url=self.bot.user.avatar_url)
		embed.add_field(name="Server Code", value=dataset["erlc_code"], inline=False)
		embed.add_field(name="Discord Code", value=dataset["discord_code"], inline=False)
		embed.set_footer(text=f"{ctx.guild.name} | CORE", icon_url = self.bot.user.avatar_url)
		await ctx.send(embed=embed)

	@commands.command(name="logaction", aliases=["logserveraction", "logkick", "logwarning"])
	@is_an_enabled_guild()
	@has_staff()
	async def _logaction(self, ctx):
		dataset = await ctx.bot.config.find_by_id(ctx.guild.id)
		embed = discord.Embed(title="Log a Moderation Action", color=core_color)
		embed.add_field(name="Question", value="What type of a moderation action is the one you are trying to log?", inline=False)
		embed.add_field(name="Warning", value="Message 'warning' if you would like to log a warning.", inline=False)	
		embed.add_field(name="Kick", value="Message 'kick' if you would like to log a kick.", inline=False)	
		embed.set_thumbnail(url=ctx.bot.user.avatar_url)
		embed.set_footer(text=f"{ctx.guild.name} | CORE", icon_url = self.bot.user.avatar_url)

		await ctx.send(embed=embed)

		def MessageCheck(message):
			if message.author == ctx.message.author:
				return True

		def OptionCheck(message):
			if message.author == ctx.message.author and message.content.lower() == "kick" or message.content.lower() == "warning":
				return True

		ActionTypeOutput = None
		ViolatorName = None
		ReasonOfAction = None



		try:
			ActionType = await self.bot.wait_for("message", check=OptionCheck, timeout=60)
			if ActionType.content.lower() == "kick":
				ActionTypeOutput = "Kick"
			elif ActionType.content.lower() == "warning":
				ActionTypeOutput = "Warning"
		except Exception as e:
			embed = discord.Embed(title="Timeout Error", color=core_color)
			embed.add_field(name="Error", value="The maximum limit of amount given to respond has been reached or you have not chosen one of the available options.", inline=False)	
			embed.set_thumbnail(url=ctx.bot.user.avatar_url)
			embed.set_footer(text=f"{ctx.guild.name} | CORE", icon_url = self.bot.user.avatar_url)

			await ctx.send(embed=embed)
			raise e
			return

		embed = discord.Embed(title="Log a Moderation Action", color=core_color)
		embed.add_field(name="Question", value="What is the name of the violator?", inline=False)
		embed.set_thumbnail(url=ctx.bot.user.avatar_url)
		embed.set_footer(text=f"{ctx.guild.name} | CORE", icon_url = self.bot.user.avatar_url)

		await ctx.send(embed=embed)



		try:
			Violator = await self.bot.wait_for("message", check=MessageCheck, timeout=60)
			if Violator is not None and Violator.content.lower() is not "cancel":
				ViolatorName = Violator.content
			elif Violator.content.lower() is "cancel":
				return
		except Exception as e:

			embed = discord.Embed(title="Timeout Error", color=core_color)
			embed.add_field(name="Error", value="The maximum limit of amount given to respond has been reached.", inline=False)	
			embed.set_thumbnail(url=ctx.bot.user.avatar_url)
			embed.set_footer(text=f"{ctx.guild.name} | CORE", icon_url=self.bot.user.avatar_url)

			await ctx.send(embed=embed)
			raise e

			return

		embed = discord.Embed(title="Log a Moderation Action", color=core_color)
		embed.add_field(name="Question", value="What was the reason for this infraction?", inline=False)
		embed.set_thumbnail(url=ctx.bot.user.avatar_url)
		embed.set_footer(text=f"{ctx.guild.name} | CORE", icon_url=self.bot.user.avatar_url)

		await ctx.send(embed=embed)


		try:
			ReasonMessage = await self.bot.wait_for("message", check=MessageCheck, timeout=60)
			if ReasonMessage is not None:
				ReasonOfAction = ReasonMessage.content

		except Exception as e:
			embed = discord.Embed(title="Timeout Error", color=core_color)
			embed.add_field(name="Error", value="The maximum limit of amount given to respond has been reached.", inline=False)	
			embed.set_thumbnail(url=ctx.bot.user.avatar_url)
			embed.set_footer(text=f"{ctx.guild.name} | CORE", icon_url=self.bot.user.avatar_url)

			await ctx.send(embed=embed)
			raise e
			return


		embed = discord.Embed(title="Infraction Logging Systems", color=core_color)
		embed.set_footer(text=f"{ctx.guild.name} | CORE", icon_url=self.bot.user.avatar_url)
		embed.set_thumbnail(url=ctx.author.avatar_url)
		embed.add_field(name="Moderator Name", value=ctx.author.name, inline=False)	
		embed.add_field(name="Violator Name", value=ViolatorName, inline=False)
		embed.add_field(name="Reason", value=ReasonOfAction, inline=False)
		embed.add_field(name="Time", value=f"{datetime.utcnow()}", inline=False)
		embed.add_field(name="Action Type", value=ActionTypeOutput, inline=False)

		channel = discord.utils.get(ctx.guild.text_channels, name=dataset["infraction_channel"])


		await channel.send(embed=embed)

	@commands.command(name = "ssu", aliases=["serverstartup", "startssu", "hostssu"])
	@has_permissions(manage_channels = True)
	async def _ssu(self, ctx, status = "Open"):
		if status.lower() == "on" or status.lower() == "open":
			ssu_embed = discord.Embed(title = f"{ctx.guild.name} | Server Start Up", color = core_color)
			ssu_embed.set_footer(text = "Server Start Up | CORE", icon_url=self.bot.user.avatar_url)
			ssu_embed.set_thumbnail(url = ctx.guild.icon_url)
		
			embed = discord.Embed(title = "SSU Command | CORE", description = "What channel do you want this in?", color = core_color)
			await ctx.send(embed = embed)

			def Check(Message):
				return ctx.message.channel == Message.channel and ctx.author == Message.author

			Message = await self.bot.wait_for('message', check = Check, timeout = 60)

			channel = discord.utils.get(ctx.guild.text_channels, name = Message.content.lower())

			ssu_embed.add_field(name = "Hosted By", value = ctx.author.name, inline = False)
			ssu_embed.add_field(name = "Game Link", value = "https://www.roblox.com/games/2534724415/Emergency-Response-Liberty-County?refPageId=10b1bc76-bd7a-4308-a3fb-60d91dcb14ce", inline = False)
			dataset = await self.bot.config.find_by_id(ctx.guild.id)
			ssu_embed.add_field(name = "Server Code", value = dataset["erlc_code"], inline = False)

			await channel.send("@everyone" ,embed = ssu_embed)



def setup(bot):
	bot.add_cog(ERLC(bot))
