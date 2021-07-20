import discord
from discord.ext import commands

import asyncio

core_color = discord.Color.from_rgb(30, 144, 255)
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
		await self.bot.logout()
		await asyncio.sleep(30)
		await self.bot.login(token)
		status_change.start()

	@commands.command(name="close", aliases=["closebot", "shutdown"], description="Closes the bot. (Bot Creator Command)", usage="close")
	@commands.is_owner()
	async def close(self, ctx):
	    await self.bot.close()
	    print("Bot Closed")


	@commands.command(name = "embed", aliases = ["makeembed", "createembed"], description = "Creates an Embed (Bot Creator Command)")
	@commands.is_owner()
	async def embed(self, ctx):
		def check(message):
			return message.author == ctx.author and message.guild == ctx.guild

		def custom_check(message):
			return message.author == ctx.author and message.guild == ctx.guild and message.content.lower() in ["yes", "no"]

		questions = ["What do you want the embed title to be?", "What do you want the embed description to be?", "What color do you want the embed to be?"]
		responses = []
		messages = []
		variables = ["title", "description", "color"]
		for question in questions:
			message = await ctx.send(question)
			messages.append(message)
			response = await self.bot.wait_for('message', timeout = 120, check = check)
			if response.content == "cancel":
				return await ctx.send('Cancelled.')
			responses.append(response.content)
		message = "Is this your desired configuration?\n"
		if responses[2] == "default":
			responses[2] = core_color
		else:
			responses[2] = int(responses[2], 16)
		for response in responses:
			index = responses.index(response)
			question = questions[index]
			message += f"{question} {response}\n"
			if response == "None":
				response = None
		message = await ctx.send(message)
		messages.append(message)
		message = await self.bot.wait_for('message', timeout = 60, check = custom_check)
		messages.append(message)
		embed = None
		if message.content.lower() == "yes":
			embed = discord.Embed(color = core_color)
			dictionary = dict(zip(variables, responses))
			for key, value in dictionary.items():
				try:
					setattr(embed, key, value)
				except:
					message = await ctx.send(f"{key} could not be parsed.")
					messages.append(message)
		else:
			return await ctx.send("Embed has been cancelled")
		await ctx.send(embed = embed)


		send_message = await ctx.send('Do you want to send this embed to anyone?')
		message = await self.bot.wait_for('message', timeout = 120, check = custom_check)
		if message.content.lower() == "no":
			return
		await ctx.send('How many users do you want to send to?')
		amount = await self.bot.wait_for('message', timeout = 120, check = check)
		amount = int(amount.content)
		for _ in range(amount):
			num = 0
			message = await ctx.send("Please send the ID of the user")
			id_message = await self.bot.wait_for('message', timeout = 120, check = check)
			for guild in self.bot.guilds:
				for member in guild.members:
					if member.id == int(id_message.content):
						try:
							if num == 0:
								num = 1
								await member.send(embed = embed)
								return await ctx.send(f'{member.username} has been sent the embed.')
							else:
								id_message.content = "0"

						except:
							pass

def setup(bot):
	bot.add_cog(CreatorCommands(bot))
