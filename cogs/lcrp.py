import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, has_role

from datetime import datetime

core_color = discord.Color.from_rgb(30, 144, 255)

class LCRP(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	def is_in_guild(guild_id):
		async def predicate(ctx):
			return ctx.guild and ctx.guild.id == guild_id
		return commands.check(predicate)

	@commands.command()
	@is_in_guild(722195079262896239)
	@has_role("[-] 𝙎𝙩𝙖𝙛𝙛")
	async def duty(self, ctx, arg1="On-Duty"):
		channel = discord.utils.get(ctx.message.channel.guild.text_channels , name="on-duty")
		embed = discord.Embed(title="Duty Changed", color=core_color)
		embed.add_field(name="Name", value=ctx.author.name, inline=True)
		if arg1.lower() == "off" or arg1 == "off-duty":
			embed.add_field(name="Status", value="Off-Duty", inline=True)
		else:
			embed.add_field(name="Status", value="On-Duty", inline=True)
		embed.add_field(name="Time", value=f"{datetime.utcnow()}")
		embed.set_thumbnail(url=str(ctx.message.author.avatar_url))
		await channel.send(embed=embed)

	@commands.command(name="code", aliases=["server_code", "getservercode"])
	@is_in_guild(722195079262896239)
	async def code(self, ctx):
		embed = discord.Embed(title="Server Code", color=core_color)
		embed.set_thumbnail(url=self.bot.user.avatar_url)
		embed.add_field(name="Server Code", value="AvvxY", inline=False)
		embed.add_field(name="Discord Code", value="BGryYXC", inline=False)
		embed.set_footer(text="Lake County RP | CORE", icon_url=self.bot.user.avatar_url)
		await ctx.send(embed=embed)

	@commands.command(name="logaction", aliases=["logserveraction", "logkick", "logwarning"])
	@is_in_guild(722195079262896239)
	@has_role("[-] 𝙎𝙩𝙖𝙛𝙛")
	async def _logaction(self, ctx):
		embed = discord.Embed(title="Log a Moderation Action", color=core_color)
		embed.add_field(name="Question", value="What type of a moderation action is the one you are trying to log?", inline=False)
		embed.add_field(name="Warning", value="Message 'warning' if you would like to log a warning.", inline=False)	
		embed.add_field(name="Kick", value="Message 'kick' if you would like to log a kick.", inline=False)	
		embed.set_thumbnail(url=ctx.bot.user.avatar_url)
		embed.set_footer(text="Lake County RP | CORE", icon_url=self.bot.user.avatar_url)

		await ctx.send(embed=embed)

		def MessageCheck(message):
			if message.author == ctx.message.author:
				return True

		ActionTypeOutput = None
		ViolatorName = None
		ReasonOfAction = None



		try:
			ActionType = await self.bot.wait_for("message", check=MessageCheck, timeout=120)
			if ActionType.content.lower() == "kick":
				ActionTypeOutput = "Kick"
			elif ActionType.content.lower() == "warning":
				ActionTypeOutput = "Warning"
		except Exception as e:
			embed = discord.Embed(title="Timeout Error", color=core_color)
			embed.add_field(name="Error", value="The maximum limit of amount given to respond has been reached.", inline=False)	
			embed.set_thumbnail(url=ctx.bot.user.avatar_url)
			embed.set_footer(text="Lake County RP | CORE", icon_url=self.bot.user.avatar_url)

			await ctx.send(embed=embed)
			raise e
			return

		embed = discord.Embed(title="Log a Moderation Action", color=core_color)
		embed.add_field(name="Question", value="What is the name of the violator?", inline=False)
		embed.set_thumbnail(url=ctx.bot.user.avatar_url)
		embed.set_footer(text="Lake County RP | CORE", icon_url=self.bot.user.avatar_url)

		await ctx.send(embed=embed)



		try:
			Violator = await self.bot.wait_for("message", check=MessageCheck, timeout=120)
			if Violator is not None:
				ViolatorName = Violator.content
		except Exception as e:

			embed = discord.Embed(title="Timeout Error", color=core_color)
			embed.add_field(name="Error", value="The maximum limit of amount given to respond has been reached.", inline=False)	
			embed.set_thumbnail(url=ctx.bot.user.avatar_url)
			embed.set_footer(text="Lake County RP | CORE", icon_url=self.bot.user.avatar_url)

			await ctx.send(embed=embed)
			raise e

			return

		embed = discord.Embed(title="Log a Moderation Action", color=core_color)
		embed.add_field(name="Question", value="What was the reason for this infraction?", inline=False)
		embed.set_thumbnail(url=ctx.bot.user.avatar_url)
		embed.set_footer(text="Lake County RP | CORE", icon_url=self.bot.user.avatar_url)

		await ctx.send(embed=embed)


		try:
			ReasonMessage = await self.bot.wait_for("message", check=MessageCheck, timeout=120)
			if ReasonMessage is not None:
				ReasonOfAction = ReasonMessage.content

		except Exception as e:
			embed = discord.Embed(title="Timeout Error", color=core_color)
			embed.add_field(name="Error", value="The maximum limit of amount given to respond has been reached.", inline=False)	
			embed.set_thumbnail(url=ctx.bot.user.avatar_url)
			embed.set_footer(text="Lake County RP | CORE", icon_url=self.bot.user.avatar_url)

			await ctx.send(embed=embed)
			raise e
			return


		embed = discord.Embed(title="Infraction Logging Systems", color=core_color)
		embed.set_footer(text="Lake County RP | CORE", icon_url=self.bot.user.avatar_url)
		embed.set_thumbnail(url=ctx.author.avatar_url)
		embed.add_field(name="Moderator Name", value=ctx.author.name, inline=False)	
		embed.add_field(name="Violator Name", value=ViolatorName, inline=False)
		embed.add_field(name="Reason", value=ReasonOfAction, inline=False)
		embed.add_field(name="Time", value=f"{datetime.utcnow()}", inline=False)
		embed.add_field(name="Action Type", value=ActionTypeOutput, inline=False)

		channel = discord.utils.get(ctx.guild.text_channels, name="infraction-logs")


		await channel.send(embed=embed)




def setup(bot):
	bot.add_cog(LCRP(bot))