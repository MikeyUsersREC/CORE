import discord
from discord.ext import commands 
from discord.ext.commands import has_permissions

core_color = discord.Color.from_rgb(30, 144, 255)

class AuditLogCommands(commands.Cog, name = "Audit Log Commands"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name = "auditlogs", description = "Gets the audit logs of a user or server.", aliases = ["al", "logs"], usage = "auditlog [User]")
	@has_permissions(manage_guild = True)
	async def _auditlogs(self, ctx, limit = 15, user: discord.User = None):
		GetAuditLogs = ctx.guild.audit_logs(limit = limit)
		if user == None:
			AuditLogs = [item async for item in GetAuditLogs]
		else:
			AuditLogs = [item async for item in GetAuditLogs if item.user == user]
		embed = discord.Embed(title = f"{ctx.guild.name}'s Audit Logs", color = core_color)
		embed.set_thumbnail(url = self.bot.user.avatar_url)
		embed.set_footer(text = "Audit Logs | CORE", icon_url = self.bot.user.avatar_url)
		for entry in AuditLogs:
			ENTRY_VARS = [vars(entry).items()]
			message = f"{str(entry.action.category).replace('_', ' ').replace('AuditLogActionCategory.', '').capitalize()}\nUser: {entry.user.name}\n"
			for item in ENTRY_VARS:
				for key, value in item:
					if len(message) <= 200 and not key.startswith('_'):
						message += f"{key.capitalize()}: {value}\n"
					elif len(message) >= 200:
						message += "..."
						continue
			embed.add_field(name = str(entry.action).replace('_', ' ').replace('AuditLogAction.', '').capitalize(), value = f"Action Type: {message}", inline = False)
		await ctx.send(embed = embed)

def setup(bot):
	bot.add_cog(AuditLogCommands(bot))

