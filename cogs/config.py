import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

core_color = discord.Color.from_rgb(30, 144, 255)

class Config(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	@commands.command(name="config", description="A command that changes the configuration for the bot on your server.", aliases=["conf", "settings", "serversettings", "configuration"], usage="config <Config> <On/Off>")
	@has_permissions(manage_guild=True)
	async def config(self, ctx, arg1=None, *, arg2=None):
		if arg1 == "debug":
			if arg2 == "on":

				dataset = await self.bot.config.find_by_id(ctx.guild.id)

				dataset["debug_mode"] = True

				await self.bot.config.update_by_id(dataset)

				embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
				embed.set_thumbnail(url=ctx.bot.user.avatar_url)
				await ctx.send(embed=embed)

			elif arg2 == "off":
				dataset = await self.bot.config.find_by_id(ctx.guild.id)

				dataset["debug_mode"] = False

				await self.bot.config.update_by_id(dataset)

				embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
				embed.set_thumbnail(url=ctx.bot.user.avatar_url)
				await ctx.send(embed=embed)

		if arg1 == "manualverification":
			if arg2 == "on" or arg2 == "true":
				dataset = await self.bot.config.find_by_id(ctx.guild.id)

				dataset["manualverification"] = True

				await self.bot.config.update_by_id(dataset)

				embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
				embed.set_thumbnail(url=ctx.bot.user.avatar_url)
				await ctx.send(embed=embed)
			else:
				dataset = await self.bot.config.find_by_id(ctx.guild.id)

				dataset["manualverification"] = False

				await self.bot.config.update_by_id(dataset)
				embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
				embed.set_thumbnail(url=ctx.bot.user.avatar_url)
				await ctx.send(embed=embed)

		if arg1 == "announcement_channel":
			dataset = await self.bot.config.find_by_id(ctx.guild.id)

			dataset["announcement_channel"] = arg2

			await self.bot.config.update_by_id(dataset)
			embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
			embed.set_thumbnail(url=ctx.bot.user.avatar_url)
			await ctx.send(embed=embed)

		if arg1 == "verification_role":
			dataset = await self.bot.config.find_by_id(ctx.guild.id)

			dataset["verification_role"] = arg2

			await self.bot.config.update_by_id(dataset)

			embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
			embed.set_thumbnail(url=ctx.bot.user.avatar_url)
			await ctx.send(embed=embed)

		if arg1 == "link_automoderation":
			if arg2 == "on":
				dataset = await self.bot.config.find_by_id(ctx.guild.id)

				dataset["link_automoderation"] = True

				await self.bot.config.update_by_id(dataset)
				embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
				embed.set_thumbnail(url=ctx.bot.user.avatar_url)
				await ctx.send(embed=embed)

			elif arg2 == "off":
				dataset = await self.bot.config.find_by_id(ctx.guild.id)

				dataset["link_automoderation"] = False

				await self.bot.config.update_by_id(dataset)

				embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
				embed.set_thumbnail(url=ctx.bot.user.avatar_url)
				await ctx.send(embed=embed)

		if arg1 is None and arg2 is None:
			embed = discord.Embed(title="Settings and Configurations", description="__**Configurations**__\n\n**debug** | Debug Mode sends errors in the chat rather than the console.\n\n**manualverification** | Manual Verifications enables code-based chat authenticated verification for servers.\n\n**announcement_channel** | Sets the announcement channel.\n\n**verification_role** | Sets the verification role for servers.\n\n**link_automoderation** | The bot can check for links.", color=core_color)
			embed.set_thumbnail(url=ctx.bot.user.avatar_url)
			await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Config(bot))