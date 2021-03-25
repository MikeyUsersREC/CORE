import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio

core_color = discord.Color.from_rgb(30, 144, 255)

class Announcements(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	@commands.command(name="announce", aliases=["announcement", "sendannouncement"], description="Sends an embed with the parameters you send to the designated announcement channel.", usage="announce")
	@has_permissions(manage_channels=True) 
	async def announce(self, ctx):
		dataset = await self.bot.config.find_by_id(ctx.guild.id)

		announcement_channel = dataset["announcement_channel"]
		channel = ctx.message.channel
		announcements = discord.utils.get(ctx.message.channel.guild.text_channels , name=announcement_channel)
		areSureEmbed = discord.Embed(title="Announcement" , description="What is the body of the announcement?", color=core_color)
		await ctx.send(embed=areSureEmbed)

		def check(m):
			return m.channel == channel and m.author == ctx.message.author
		try:
			msg = await self.bot.wait_for('message' , check=check , timeout=120)
			if msg.content == "cancel":
				cancelEmbed = discord.Embed(title="Announcement", description="Successfully cancelled!", color=core_color)
				await channel.send(embed=cancelEmbed)
				return
			CategoryEmbed = discord.Embed(title="Announcement", description="What catgegory is your announcement? Categories: information, warning, 			important", color=core_color)
			await channel.send(embed=CategoryEmbed)
		except asyncio.TimeoutError:
			TimeoutEmbed = discord.Embed(title="Timeout!", description="You have reached the 120 second timeout! Please send another command if you 			want to continue!", color=core_color)
			await ctx.send(embed=TimeoutEmbed)
			return
		try:
			categoryMsg = await self.bot.wait_for('message' , check=check , timeout=120)
			if msg.content == "cancel":
				cancelEmbed = discord.Embed(title="Announcement" , description="Successfully cancelled!", color=core_color)
				await channel.send("" , embed=cancelEmbed)
				return
			SendingAnnouncementEmbed = discord.Embed(title="Announcement", description=f"Are you sure you want to send this announcement?\n\n 					{msg.content}", color=core_color)
			await channel.send(embed=SendingAnnouncementEmbed)
		except asyncio.TimeoutError:
			TimeoutEmbed = discord.Embed(title="Timeout!", description="You have reached the 120 second timeout! Please send another command if you 			want to continue!", color=core_color)
			await channel.send(embed=TimeoutEmbed)
		try:
			Message = await self.bot.wait_for('message' , check=check , timeout=120)
			if Message.content == "cancel" or Message.content == "no":
				cancelEmbed = discord.Embed(title="Announcement" , description="Successfully cancelled!", color=core_color)
				await channel.send("" , embed=cancelEmbed)
				return
			if categoryMsg.content.lower() == "information":
				AnnouncementEmbed = discord.Embed(title="core | information" , description=msg.content, color=discord.Color.from_rgb(0 , 0 , 255))
				AnnouncementEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/733628287548653669/754109649074257960/768px-							Logo_informations.png?width=468&height=468")
			if categoryMsg.content.lower() == "important":
				AnnouncementEmbed = discord.Embed(title=":loudspeaker: Important Announcement" , description=msg.content, 											color=discord.Color.from_rgb(255 , 0 , 0))
				AnnouncementEmbed.set_thumbnail(
	                url="https://cdn.discordapp.com/emojis/746034342303891585.png?v=1")
			elif categoryMsg.content.lower() == "warning":
				AnnouncementEmbed = discord.Embed(title=":warning: Warning Announcement", description=msg.content, 													color=discord.Color.from_rgb(252, 206, 0))
			else:
				PleaseTryAgain = discord.Embed(title="Error:", description="You did not put the one of the valid categories available for this 						announcement, please try again.", color= discord.Color.from_rgb(255, 0, 0))
				await ctx.send(embed=PleaseTryAgain)
				return
			SendingAnnouncementEmbed = discord.Embed(title="Announcement" ,
	        description="Sending announcement...\n\n" + msg.content ,
	        color=core_color)
			await channel.send(embed=SendingAnnouncementEmbed)
			await announcements.send("@everyone" , embed=AnnouncementEmbed)
		except asyncio.TimeoutError:
			TimeoutEmbed = discord.Embed(title="Timeout!", description="You have reached the 120 second timeout! Please send another command if you 			want to continue!", color=core_color)
			await channel.send(embed=TimeoutEmbed)


	@commands.command(name="categories", aliases=["announcementcategories", "ac"], description="Specifies the announcement categories you can use in the announce command.", usage="categories")
	async def categories(self, ctx):
	    f = discord.Embed(title="Categories", description="These are the categories for the CORE Announce command:\n\ninformation,\nimportant,\nwarning", color=core_color)
	    f.set_thumbnail(url=ctx.bot.user.avatar_url)
	    await ctx.send(embed=f)


	@commands.command(name = "poll", aliases = ["po", "servervote"], description = "A command to send a poll to a designated channel for an opinion of a change.", usage = "poll")
	@has_permissions(manage_channels = True)
	async def poll(self, ctx):
		embed = discord.Embed(title = "Poll Command", description = "What question are you trying to ask?", color = core_color)
		embed.set_thumbnail(url = "https://images-ext-2.discordapp.net/external/S3MLOZh_lwAfQSI9OUGntKj0AUY3Hsfx3d_1NpG8g0k/https/cdn1.vectorstock.com/i/thumbs/40/40/document-form-blank-icon-sign-icon-document-form-vector-33744040.jpg?width=90&height=94")
		await ctx.send(embed = embed)

		def Check(m):
			return ctx.message.author == m.author and m.channel == ctx.message.channel


		Content = await self.bot.wait_for('message', check = Check, timeout = 120)

		embed = discord.Embed(title = "Poll Command", description = "What channel do you want to send to?", color = core_color)
		embed.set_thumbnail(url = "https://images-ext-2.discordapp.net/external/S3MLOZh_lwAfQSI9OUGntKj0AUY3Hsfx3d_1NpG8g0k/https/cdn1.vectorstock.com/i/thumbs/40/40/document-form-blank-icon-sign-icon-document-form-vector-33744040.jpg?width=90&height=94")
		await ctx.send(embed = embed)

		Channel = await self.bot.wait_for('message', check = Check, timeout = 120)

		embed = discord.Embed(title = "Poll Command", color = core_color)
		embed.add_field(name = "Question", value = "What type of question are you trying to ask?", inline = False)
		embed.add_field(name = "1) Multiple Choice", value = "A multiple choice question (1, 2 or 3)", inline = False)
		embed.add_field(name = "2) Yes / No Question", value = "A question that people reply Yes or No to.", inline = False)
		embed.set_thumbnail(url = "https://images-ext-2.discordapp.net/external/S3MLOZh_lwAfQSI9OUGntKj0AUY3Hsfx3d_1NpG8g0k/https/cdn1.vectorstock.com/i/thumbs/40/40/document-form-blank-icon-sign-icon-document-form-vector-33744040.jpg?width=90&height=94")
		await ctx.send(embed = embed)

		MultipleChoice = await self.bot.wait_for('message', check = Check, timeout = 120)
		MultipleChoice = MultipleChoice.content

		embed = discord.Embed(title = "Poll Command", description = "Do you want to ping everyone?\n\nAnswers: No, here, everyone", color = core_color)
		embed.set_thumbnail(url = "https://images-ext-2.discordapp.net/external/S3MLOZh_lwAfQSI9OUGntKj0AUY3Hsfx3d_1NpG8g0k/https/cdn1.vectorstock.com/i/thumbs/40/40/document-form-blank-icon-sign-icon-document-form-vector-33744040.jpg?width=90&height=94")
		await ctx.send(embed = embed)

		PingConfirmation = await self.bot.wait_for('message', check = Check, timeout = 120)
		PingOption = ""

		if PingConfirmation.content.lower() in ["no", "here", "everyone"]:
			if PingConfirmation.content.lower() == "no":
				PingOption = ""
			else:
				PingOption = f"@{PingConfirmation.content.lower()}"

		try:
			int(MultipleChoice)
		except:
			await ctx.send("An option was not chosen correctly. Please try again.")

		embed = discord.Embed(title = "Poll Command", description = "What color do you want the embed to be? Blue, red, green or default.", color = core_color)
		embed.set_thumbnail(url = "https://images-ext-2.discordapp.net/external/S3MLOZh_lwAfQSI9OUGntKj0AUY3Hsfx3d_1NpG8g0k/https/cdn1.vectorstock.com/i/thumbs/40/40/document-form-blank-icon-sign-icon-document-form-vector-33744040.jpg?width=90&height=94")
		await ctx.send(embed = embed)

		ColorOfEmbed = await self.bot.wait_for('message', check = Check, timeout = 120)
		EmbedColor = None

		if ColorOfEmbed.content.lower() in ["red", "green", "blue", "default"]:
			if ColorOfEmbed.content.lower() == "default":
				pass
			elif ColorOfEmbed.content.lower() == "red":
				EmbedColor = discord.Color.red()
			elif ColorOfEmbed.content.lower() == "green":
				EmbedColor = discord.Color.green()
			elif ColorOfEmbed.content.lower() == "blue":
				EmbedColor = discord.Color.blue()

		OptionChosen = None

		if MultipleChoice in ["1", "2"]:
			OptionChosen = int(MultipleChoice)
		
		
		embed = discord.Embed(title = f"{ctx.guild.name} | Poll")
		if EmbedColor == None:
			embed.color = core_color
		else:
			embed.color = EmbedColor
		embed.set_thumbnail(url = "https://images-ext-2.discordapp.net/external/S3MLOZh_lwAfQSI9OUGntKj0AUY3Hsfx3d_1NpG8g0k/https/cdn1.vectorstock.com/i/thumbs/40/40/document-form-blank-icon-sign-icon-document-form-vector-33744040.jpg?width=90&height=94")
		embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)

		if OptionChosen == 1:
			NumberOfOptionEmbed = discord.Embed(title = "Poll Command", color = core_color)
			NumberOfOptionEmbed.add_field(name = "Question", value = "How many options do you want to have?", inline = False)
			NumberOfOptionEmbed.set_thumbnail(url = "https://images-ext-2.discordapp.net/external/S3MLOZh_lwAfQSI9OUGntKj0AUY3Hsfx3d_1NpG8g0k/https/cdn1.vectorstock.com/i/thumbs/40/40/document-form-blank-icon-sign-icon-document-form-vector-33744040.jpg?width=90&height=94")
			await ctx.send(embed = NumberOfOptionEmbed)

			NumOfOptions = await self.bot.wait_for('message', check = Check, timeout = 120)
			OptionAmount = int(NumOfOptions.content)

			embed.add_field(name = "Question", value = Content.content)

			for i in range(1, OptionAmount + 1):
				embed.add_field(name = f"Option {i}", value = f"React {i} to put your opinion of the question above.", inline = False)

			channel = discord.utils.get(ctx.guild.channels, name = Channel.content)
			message = await channel.send(f"{PingOption}", embed = embed)

			for i in range(1, OptionAmount + 1):
				await message.add_reaction(u"{}\u20E3".format(i))

		if OptionChosen == 2:

			embed.add_field(name = "Question", value = Content.content, inline = False)
			channel = discord.utils.get(ctx.guild.channels, name = Channel.content)

			message = await channel.send(PingOption, embed = embed)

			for item in [u"\U0001F44D", u"\U0001F44E"]:
				await message.add_reaction(item)

def setup(bot):
	bot.add_cog(Announcements(bot))
