import discord
from discord.ext import commands

class CreatorCommands(commands.Cog, name="Creator Commands"):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")


	@commands.command(name="restart", aliases=["reloadbot"], description="Restarts the bot. (Bot Creator Command)", usage="restart")
	@commands.is_owner()
	async def restart(self, ctx):
		status_change.stop()
		await bot.logout()
		await asyncio.sleep(30)
		await bot.login(token)
		status_change.start()

	@commands.command(name="close", aliases=["closebot", "shutdown"], description="Closes the bot. (Bot Creator Command)", usage="close")
	@commands.is_owner()
	async def close(self, ctx):
	    await bot.close()
	    print("Bot Closed")




def setup(bot):
	bot.add_cog(CreatorCommands(bot))