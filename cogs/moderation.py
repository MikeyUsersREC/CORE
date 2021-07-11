import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio

core_color = discord.Color.from_rgb(30, 144, 255)

class Moderation(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")


	@commands.command(name="mute", description="Mutes the mentioned user.", aliases=["m", "silence"], usage="<User>")
	@has_permissions(manage_messages=True)
	async def mute(self, ctx, member: discord.Member, time=None, *, reason = None):
		try:
			self.bot.actionLogs[ctx.message.created_at.strftime("%m/%d/%Y, %H:%M:%S")] = {"ActionType": "Mute", "Guild": ctx.guild.name, "Author": ctx.author.name, "User": member.name}
		except:
			pass
		role = discord.utils.get(ctx.guild.roles, name="Muted")
		if role == None:
			role = await ctx.guild.create_role(name = "Muted", permissions = discord.Permissions(ctx.guild.default_role.permissions.value), color = discord.Color(0xA9A9A9))
			await role.edit(position = discord.utils.get(ctx.guild.members, name = "CORE").top_role.position - 1)
			for channel in ctx.guild.text_channels:
        			perms = channel.overwrites_for(role)
       				perms.send_messages = False
        			await channel.set_permissions(role, overwrite=perms, reason="Mute Overwrite")			
		await member.add_roles(role)
		embed=discord.Embed(title="User has been muted", color=core_color)
		embed.add_field(name = "User", value = member.name, inline = False)
		embed.add_field(name = "Author", value = ctx.author.name, inline = False)
		embed.add_field(name = "Time", value = f"{str(time).lower()}", inline = False)
		embed.add_field(name = "Reason", value = reason, inline = False)
		embed.set_thumbnail(url=ctx.bot.user.avatar_url)
		await ctx.send(embed=embed)

		if str(time).lower().endswith("s"):
			timeList = time.lower().split("s")
			timeDown = int(timeList[0])
		elif str(time).lower().endswith("m"):
			timeList = time.lower().split("m")
			timeDown = int(timeList[0]) * 60
		elif str(time).lower().endswith("h"):
			timeList = time.lower().split("h")
			timeDown = int(timeList[0]) * 60 * 60
		elif str(time).lower().endswith("d"):
			timeList = time.lower().split("d")
			timeDown = int(timeList[0]) * 60 * 60 * 24
		await asyncio.sleep(timeDown)

		await member.remove_roles(role)

	@commands.command(name="unmute", aliases=["um", "unsilence"], description="Ummutes the mentioned user if they are already muted.", usage="<User>")
	@has_permissions(manage_messages=True)
	async def unmute(self, ctx, member: discord.Member):
		try:
			self.bot.actionLogs[ctx.message.created_at.strftime("%m/%d/%Y, %H:%M:%S")] = {"ActionType": "Unmute", "Guild": ctx.guild.name, "Author": ctx.author.name, "User": member.name}
		except:
			pass
		role = discord.utils.get(ctx.guild.roles, name="Muted")
		if member.has_role(role):
			embed=discord.Embed(title="User unmuted!", description="**{0}** was muted by **{1}**!".format(member.display_name, ctx.guild.name), color=core_color)
			embed.set_thumbnail(url=ctx.bot.user.avatar_url)
			await member.remove_roles(role)
		else:
			await ctx.send("That member is not muted.")
			return

	@commands.command(name="kick", aliases=["k", "removeuser"], description="Kick the mentioned user.", usage="kick <User>")
	@has_permissions(kick_members=True) 
	async def kick(self, ctx, member : discord.Member, *, reason=None):
		try:
			self.bot.actionLogs[ctx.message.created_at.strftime("%m/%d/%Y, %H:%M:%S")] = {"ActionType": "Kick", "Guild": ctx.guild.name, "Author": ctx.author.name, "User": member.name}
		except:
			pass
		await member.kick(reason=reason)
		if reason == None:
			reason = "None"
		kickEmbed = discord.Embed(title = "Successfully Kicked", color = core_color)
		kickEmbed.add_field(name = "Moderator", value = ctx.author.name, inline = False)
		kickEmbed.add_field(name = "Member", value = member.name, inline = False)
		kickEmbed.add_field(name = "Reason", value = reason, inline = False)
		kickEmbed.set_footer(text = "Moderation | CORE", icon_url = self.bot.user.avatar_url)
		kickEmbed.set_thumbnail(url = self.bot.user.avatar_url)
		await ctx.send(embed=kickEmbed)

	@commands.command(name="ban", aliases=["b", "blacklist"], description="Ban the mentioned user.", usage="ban <User>")
	@has_permissions(ban_members=True) 
	async def ban(self, ctx, member : discord.Member, *, reason=None):
		try:
			self.bot.actionLogs[ctx.message.created_at.strftime("%m/%d/%Y, %H:%M:%S")] = {"ActionType": "Ban", "Guild": ctx.guild.name, "Author": ctx.author.name, "User": member.name}
		except:
			pass
		await member.ban(reason=reason)
		banEmbed = discord.Embed(title="Successfully Banned", color=core_color)
		banEmbed.add_field(name = "Moderator", value = ctx.author, inline = False)
		banEmbed.add_field(name = "Member", value = member.name, inline = False)
		banEmbed.add_field(name = "Reason", value = reason, inline = False)
		banEmbed.set_footer(text = "Moderation | CORE", icon_url = self.bot.user.avatar_url)
		banEmbed.set_thumbnail(url = self.bot.user.avatar_url)
		await ctx.send(embed=banEmbed)

	@commands.command(name="purge", aliases=["delete", "purgechannel", "purgemessages", "deletemessages", "pu"], description="Deletes a certain amount of messages in the current channel.", usage="purge <Amount>")
	@has_permissions(manage_channels=True)
	async def purge(self, ctx, amount=15):
		try:
			self.bot.actionLogs[ctx.message.created_at.strftime("%m/%d/%Y, %H:%M:%S")] = {"ActionType": "Purge", "Guild": ctx.guild.name, "Author": ctx.author.name, "Amount": amount}
		except:
			pass
		new_amount = amount + 1
		await ctx.channel.purge(limit=new_amount)

	@commands.command(name="warn", description="Warn the mentioned user.", aliases=["w", "infract", "warnuser", "warnmember"], usage="warn <User> [Reason]")
	@has_permissions(manage_messages=True)
	async def warn(self, ctx, member: discord.Member, *,reason=None):
		if member in [bot.user, ctx.author]:
			return await ctx.send("You can't warn yourself or the bot.")
		if reason == None:
			reason = "None"

		self.bot.actionLogs[ctx.message.created_at.stftime("%m/%d/%Y, %H:%M:%S")] = {"ActionType": "Warning", "Guild": ctx.guild.name, "Author": ctx.author, "User": member.name, "Reason": reason.name}
		embed = discord.Embed(title = "Successfully Warned", color = core_color)
		embed.add_field(name = "Moderator", value = ctx.author.name, inline = False)
		embed.add_field(name = "Member", value = member.name, inline = False)
		embed.add_field(name = "Reason", value = reason, inline = False)
		embed.set_footer(text = "Moderation | CORE", icon_url = self.bot.user.avatar_url)
		embed.set_thumbnail(url = self.bot.user.avatar_url)
		await ctx.send(embed = embed)

	@commands.command(name="modlog", aliases=["getwarnings", "warnings", "infractions", "gw"], description="Get the warnings of the mentioned user.", usage="get_log <User>")
	@has_permissions(manage_messages=True)
	async def get_log(self, ctx, member: discord.Member = None):
		if member == None:
			member = ctx.author
		embed = discord.Embed(title = "{}'s Actions".format(member.name), color = core_color)

		for key, value in self.bot.auditLogs.items():
			try:
				if value["Guild"] == ctx.guild.name and value["User"] == member.name:
					description = f"Date: {key}\n"
					for key, value in value.items():
						if key != "Guild" and key != "User":
							description += f"{key}: {value}\n"
					embed.add_field(name = value["ActionType"], value = description, inline = False)
			except:
				pass
		embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		embed.set_footer(text = "Moderation Actions | CORE", icon_url = self.bot.user.avatar_url)
		embed.set_thumbnail(url = self.bot.user.avatar_url)
		await ctx.send(embed = embed)

	@commands.command(aliases=["clear_warns", "clearwarnings", "cw"], description="Clear the mentioned user's warnings.", usage="clearwarns <User>")
	@has_permissions(manage_messages=True)
	async def clearwarns(self, ctx, member: discord.Member):
		pass

def setup(bot):
	bot.add_cog(Moderation(bot))
