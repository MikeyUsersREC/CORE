import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio

core_color = discord.Color.from_rgb(30, 144, 255)

class Config(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	@commands.command(name="config", description="A command that changes the configuration for the bot on your server.", aliases=["conf", "settings", "serversettings", "configuration"], usage="config <Config> <On/Off>")
	@has_permissions(manage_guild=True)
	async def config(self, ctx):

		embed = discord.Embed(title = "Configuration", color = core_color)
		embed.add_field(name = "View", value = "Would you like to view your configurations?", inline = False)
		embed.add_field(name = "Change", value = "Would you like to change your configurations?", inline = False)
		embed.set_thumbnail(url = self.bot.user.avatar_url)
		embed.set_footer(text = "Configurations | CORE", icon_url = self.bot.user.avatar_url)
		await ctx.send(embed = embed)
		def check(Message):
			return Message.author == ctx.author and Message.channel == ctx.channel
		OptionMessage = await self.bot.wait_for('message', check = check, timeout = 120)

		CONFIGS = ["manualverification", "link_automoderation", "announcement_channel", "verification_role", "staff_role", "duty_channel", "infraction_channel", "erlc_code", "discord_code"]
		BOOLEAN_CONFIGS = ["manualverification", "link_automoderation"]

		if OptionMessage.content == "cancel":
			await ctx.send('Successfully cancelled.')
			return

		if OptionMessage.content == "view":
			embed = discord.Embed(title = "Configurations | CORE", color = core_color)
			embed.set_thumbnail(url = self.bot.user.avatar_url)
			embed.set_footer(text = "Settings for {}".format(ctx.guild.name), icon_url = self.bot.user.avatar_url)
			dataset = await self.bot.config.find_by_id(ctx.guild.id)
			for item in CONFIGS:
				try:
					value = dataset[item]
				except:
					value = "None"
				embed.add_field(name = item, value = value, inline = False)
			await ctx.send(embed = embed)


		if OptionMessage.content == "change":
			embed = discord.Embed(title = "Configurations | CORE", color = core_color)
			embed.set_thumbnail(url = self.bot.user.avatar_url)
			embed.set_footer(text = "Settings for {}".format(ctx.guild.name), icon_url = self.bot.user.avatar_url)
			message = "What option do you want to change?\n"
			for item in CONFIGS:
				message += "\n**{}**".format(item)
			embed.description = message
			await ctx.send(embed = embed)

			ConfigurationMessage = await self.bot.wait_for('message', check = check, timeout = 120)
			if ConfigurationMessage.content == "cancel":
				return
			
			embed = discord.Embed(title = "Configurations | CORE", color = core_color)
			embed.set_thumbnail(url = self.bot.user.avatar_url)
			embed.set_footer(text = "Settings for {}".format(ctx.guild.name), icon_url = self.bot.user.avatar_url)
			if ConfigurationMessage.content.lower() in BOOLEAN_CONFIGS:
				embed.add_field(name = ConfigurationMessage.content.lower(), value = "Options: On / Off")
			if ConfigurationMessage.content.lower() not in BOOLEAN_CONFIGS:
				embed.add_field(name = ConfigurationMessage.content.lower(), value = "Options: Any")
			if ConfigurationMessage.content.lower() not in CONFIGS:
				return await ctx.send('You have not put a valid option.')
			

			await ctx.send(embed = embed)

			ChangedOption = await self.bot.wait_for('message', check = check, timeout = 120)
			if ConfigurationMessage.content.lower() in BOOLEAN_CONFIGS:
				if ChangedOption.content.lower() not in ["true", "false", "on", "off"]:
					return await ctx.send('You have not put a valid option for this configuration.')
 
			if ConfigurationMessage.content.lower() in CONFIGS:
				if "channel" in ConfigurationMessage.content.lower():
					if discord.utils.get(ctx.guild.text_channels, name = ChangedOption.content.lower()) == None:
						return await ctx.send("You have put an invalid channel name. Only put the name of the channel, not the hashtag.")

				if "role" in ConfigurationMessage.content.lower():
					if discord.utils.get(ctx.guild.roles, name = ChangedOption.content) == None:
						return await ctx.send("You have put an invalid role name.")
     
     
			dataset = await self.bot.config.find_by_id(ctx.guild.id)
			try:
				dataset[ConfigurationMessage.content.lower()] = ChangedOption.content
				await self.bot.config.update_by_id(dataset)
				await ctx.send("Successfully configured {} as {}".format(ConfigurationMessage.content.lower(), ChangedOption.content))
			except:
				if dataset != None:
					await ctx.send('Something has gone wrong when changing the configuration. Please try again.')
				if dataset == None:
					Message = await ctx.send('CORE has found an Internal Database Corruption.\nPlease wait as we fix it.')
					await asyncio.sleep(5)
					await self.bot.config.insert({"_id": ctx.guild.id, ConfigurationMessage.content.lower(): ChangedOption.content.lower()})
					await Message.edit(content = 'CORE has fixed the Internal Database Corruption and successfully configured {} as {}'.format(ConfigurationMessage.content.lower(), ChangedOption.content))
def setup(bot):
	bot.add_cog(Config(bot))
