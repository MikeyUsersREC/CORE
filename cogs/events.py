import discord
from discord.ext import commands


class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if not isinstance(error, commands.CommandNotFound):
			await ctx.send('An error has prevented the command from running. Do you (and CORE) have the correct priveliges to run this command? If you would like the full traceback of the command, please reply with the following responses.\n\n(Y, N)')
			def Check(Message):
				return Message.channel == ctx.channel and Message.author == ctx.author
			Message = await self.bot.wait_for('message', check = Check, timeout = 20)
			if "y" in Message.content.lower() or "n" in Message.content.lower():
				if "y" in Message.content.lower():
					await ctx.send(f'Error:\n```py\n{error}\n```')
				else:
					return

def setup(bot):
	bot.add_cog(Events(bot))
