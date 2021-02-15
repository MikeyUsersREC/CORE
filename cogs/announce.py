import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio

class Announcements(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	@commands.command(name="announce", aliases=["announcement", "sendannouncement"], description="Sends an embed with the parameters you send to the designated announcement channel.", usage="announce")
	@has_permissions(manage_channels=True) 
	async def announce(self, ctx):
		dataset = await bot.config.find_by_id(ctx.guild.id)

		announcement_channel = dataset["announcement_channel"]
		channel = ctx.message.channel
		announcements = discord.utils.get(ctx.message.channel.guild.text_channels , name=announcement_channel)
		areSureEmbed = discord.Embed(title="Announcement" , description="What is the body of the announcement?", color=core_color)
		await ctx.send("" , embed=areSureEmbed)

		def check(m):
			return m.channel == channel and m.author == ctx.message.author
		try:
			msg = await bot.wait_for('message' , check=check , timeout=120)
			if msg.content == "cancel":
				cancelEmbed = discord.Embed(title="Announcement" , description="Successfully cancelled!" ,
	                                            color=core_color)
				await channel.send("" , embed=cancelEmbed)
				return
			CategoryEmbed = discord.Embed(title="Announcement" ,
	                                                 	description="What catgegory is your announcement? Categories: information, warning, important",
	                                                     color=core_color)

			await channel.send(''.format(msg) , embed=CategoryEmbed)
		except asyncio.TimeoutError:
			TimeoutEmbed = discord.Embed(title="Timeout!", description="You have reached the 120 second timeout! Please send another command if you want to continue!" , color=core_color)
			await ctx.send(embed=TimeoutEmbed)
			return
		def yesCheck(m):
			return m.channel == channel and m.author == ctx.message.author
		try:
			categoryMsg = await bot.wait_for('message' , check=check , timeout=120)
			if msg.content == "cancel":
				cancelEmbed = discord.Embed(title="Announcement" , description="Successfully cancelled!", color=core_color)
				await channel.send("" , embed=cancelEmbed)
				return
			SendingAnnouncementEmbed = discord.Embed(title="Announcement" ,
	                                                     description="Are you sure you want to send this announcement?\n\n" + msg.content ,
	                                                     color=core_color)
			await channel.send(''.format(msg) , embed=SendingAnnouncementEmbed)
		except asyncio.TimeoutError:
			TimeoutEmbed = discord.Embed(title="Timeout!" ,
	                                         description="You have reached the 120 second timeout! Please send another command if you want to continue!" ,
	                                         color=core_color)
			await channel.send("" , embed=TimeoutEmbed)
		try:
			Message = await bot.wait_for('message' , check=yesCheck , timeout=120)
			if Message.content == "cancel" or Message.content == "no":
				cancelEmbed = discord.Embed(title="Announcement" , description="Successfully cancelled!" ,
	                                            color=core_color)
				await channel.send("" , embed=cancelEmbed)
				return
			if categoryMsg.content == "placeholder":
				AnnouncementEmbed = discord.Embed(title="CORE | information" , description=msg.content ,

	                                              color=core_color)
				AnnouncementEmbed.set_thumbnail(
	                url="https://media.discordapp.net/attachments/733628287548653669/754109649074257960/768px-Logo_informations.png?width=468&height=468")

			elif categoryMsg.content == "information":
				AnnouncementEmbed = discord.Embed(title="CORE | information" , description=msg.content ,

	                                              color=discord.Color.from_rgb(0 , 0 , 255))
				AnnouncementEmbed.set_thumbnail(
	                url="https://media.discordapp.net/attachments/733628287548653669/754109649074257960/768px-Logo_informations.png?width=468&height=468")
			if categoryMsg.content == "important":
				AnnouncementEmbed = discord.Embed(title=":loudspeaker: Important Announcement" , description=msg.content ,

	                                              color=discord.Color.from_rgb(255 , 0 , 0))
				AnnouncementEmbed.set_thumbnail(
	                url="https://cdn.discordapp.com/emojis/746034342303891585.png?v=1")
			elif categoryMsg.content == "warning":
				AnnouncementEmbed = discord.Embed(title=":warning: Warning Announcement" , description=msg.content ,

	                                              color=discord.Color.from_rgb(252, 206, 0))
				await announcements.send("", embed=AnnouncementEmbed)
				return
			elif categoryMsg.content == "critical":
				if ctx.message.author.id == 635119023918415874:
					AnnouncementEmbed = discord.Embed(title=":no_entry_sign: | Critical Announcement" ,
	                                                  description=msg.content ,

	                                                  color=discord.Color.from_rgb(255 , 0 , 0))
				else:
					UnauthorisedUseOfCritical = discord.Embed(title=":no_entry_sign: You are unauthorised to use this category.", description="You are not authorised to use this category, please use another category, this category can only be used by the Bot Developer.", color= discord.Color.from_rgb(255, 0, 0))
					await ctx.send("", embed=UnauthorisedUseOfCritical)
					return
			elif categoryMsg.content == "developmentWithPing":
				if ctx.message.author.id == 635119023918415874:
					TestingEmbed = discord.Embed(title=":construction:  Development Announcement" ,
	                                                  description=msg.content ,

	                                                  color=discord.Color.from_rgb(255, 145, 0))
					await announcements.send("@everyone", embed=TestingEmbed)
					return
				else:
					PleaseTryAgain = discord.Embed(title="Error:" ,
	                                               description="You did not put the one of the valid categories available for this announcement, please try again." ,
	                                               color=discord.Color.from_rgb(255 , 0 , 0))
					await ctx.send("" , embed=PleaseTryAgain)
					return
			elif categoryMsg.content == "development":
				if ctx.message.author.id == 635119023918415874:
					TestingEmbed = discord.Embed(title=":construction:  Development Announcement" ,
	                                             description=msg.content ,

	                                             color=discord.Color.from_rgb(255 , 145 , 0))
					await announcements.send("" , embed=TestingEmbed)
					return
				else:
					PleaseTryAgain = discord.Embed(title="Error:" ,
												description="You did not put the one of the valid categories available for this announcement, please try again." ,
	                                            color=discord.Color.from_rgb(255 , 0 , 0))
					await ctx.send("" , embed=PleaseTryAgain)
					return
			else:
				PleaseTryAgain = discord.Embed(title="Error:", description="You did not put the one of the valid categories available for this announcement, please try again.", color= discord.Color.from_rgb(255, 0, 0))
				await ctx.send("", embed=PleaseTryAgain)
				return
				SendingAnnouncementEmbed = discord.Embed(title="Announcement" ,
	                                                     description="Sending announcement...\n\n" + msg.content ,
	                                                     color=core_color)
				await channel.send(''.format(msg) , embed=SendingAnnouncementEmbed)
			await announcements.send("@everyone" , embed=AnnouncementEmbed)
		except asyncio.TimeoutError:
			TimeoutEmbed = discord.Embed(title="Timeout!" ,
	                                         description="You have reached the 120 second timeout! Please send another command if you want to continue!" ,
	                                         color=core_color)
			await channel.send("" , embed=TimeoutEmbed)


	@commands.command(name="categories", aliases=["announcementcategories", "ac"], description="Specifies the announcement categories you can use in the announce command.", usage="categories")
	async def categories(self, ctx):
	    f = discord.Embed(title="Categories", description="These are the categories for the CORE Announce command:\n\ninformation,\nimportant,\nwarning", color=core_color)
	    f.set_thumbnail(url=ctx.bot.user.avatar_url)
	    await ctx.send(embed=f)

def setup(bot):
	bot.add_cog(Announcements(bot))