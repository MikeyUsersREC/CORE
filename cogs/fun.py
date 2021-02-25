import discord
from discord.ext import commands
import asyncio
import random
from random import randint


core_color = discord.Color.from_rgb(30, 144, 255)

class Fun(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")


	@commands.command(name="8ball", aliases=["eightball", "responsegenerator"], description="The 8ball will generate a response to a question that you give it.", usage="8ball <Question>")
	async def eightball(self, ctx, *, question):
		import requests
		request = requests.get(f"https://8ball.delegator.com/magic/JSON/{question}")
		requestJSON = request.json()
		magic = requestJSON["magic"]
		answer = magic["answer"]
		questionOutput = magic["question"]
		embed = discord.Embed(title="The 8ball has responded.", color=core_color)
		embed.add_field(name="Question", value=questionOutput, inline=False)
		embed.add_field(name="Answer", value=answer, inline=False)
		embed.set_thumbnail(url=self.bot.user.avatar_url)
		await ctx.send(embed=embed)


	@commands.command(name="rng", aliases=["randomnumber", "randomnumbergenerator"], description="Generates a random number from the numbers you provide.")
	async def randomnumber(self, ctx, num1: int, num2: int):
		randomNumber = randint(num1, num2)
		message = await ctx.send("Calculating...")
		await asyncio.sleep(2)
		await message.edit(content=f"The number is: {randomNumber}")

	@commands.command(name="maths", description="Calculates from the numbers that you provide.", aliases=["calculate", "calculator", "calc"], usage="maths <Operation> <Interger> <Interger>")
	async def maths(self, ctx, arg="practise", arg2="add", arg3=5, arg4=91):
		if arg == "practise":
			num1 = randint(100, 1000)
			num2 = randint(1000, 5000)
			result = num1 + num2
			mathsEmbed = discord.Embed(title="Maths with CORE", description=f"Work out this calculation and say it in chat.\n\n{num1} + {num2}", color=core_color)
			mathsEmbed.set_thumbnail(url=ctx.bot.user.avatar_url)
			await ctx.send(embed=mathsEmbed)
			try:
				msg = await bot.wait_for("message")
				if msg.content == str(result):
					succesfulEmbed = discord.Embed(title="Maths with CORE", description="You successfully guessed the answer.", color=core_color)
					succesfulEmbed.set_thumbnail(url=ctx.bot.user.avatar_url)
					await ctx.send(embed=succesfulEmbed)
				else:
					failureEmbed = discord.Embed(title="Maths with CORE", description="Answer was incorrect.", color=core_color)
					failureEmbed.set_thumbnail(url=ctx.bot.user.avatar_url)
					await ctx.send(embed=failureEmbed)
			except:
				return
		elif arg == "operation":
			if arg2 == "add":
				number = arg3 + arg4
				addEmbed = discord.Embed(title="Maths with CORE", description=f"Answer is: {number}", color=core_color)
				addEmbed.set_thumbnail(url=ctx.bot.user.avatar_url)
				await ctx.send(embed=addEmbed)
			if arg2 == "minus" or arg2 == "subtract":
				number = arg3 - arg4
				subtractEmbed = discord.Embed(title="Maths with CORE", description=f"Answer is: {number}", color=core_color)
				subtractEmbed.set_thumbnail(url=ctx.bot.user.avatar_url)
				await ctx.send(embed=subtractEmbed)
			if arg2 == "multiply" or arg2 == "times":
				number = arg3 * arg4
				multiplyEmbed = discord.Embed(title="Maths with CORE", description=f"Answer is: {number}", color=core_color)
				multiplyEmbed.set_thumbnail(url=ctx.bot.user.avatar_url)
				await ctx.send(embed=multiplyEmbed)
			if arg2 == "divide" or arg2 == "share":
				number = arg3 / arg4
				divideEmbed = discord.Embed(title="Maths with CORE", description=f"Answer is: {number}", color=core_color)
				divideEmbed.set_thumbnail(url=ctx.bot.user.avatar_url)
				await ctx.send(embed=divideEmbed)

	@commands.command(name="rps", aliases=["rockpaperscissors"], description="Start a rock paper scissors game with the bot.", usage="rps <Rock/Paper/Scissors>")
	async def rps(self, ctx, arg):
		randomNumber = randint(1, 3)
		embed = discord.Embed(title="Rock Paper Scissors!", color=core_color)
		if arg.lower() == "rock" or arg.lower() == "paper" or arg.lower() == "scissors":
			if randomNumber == 1:
				embed.description = "Rock!"
			elif randomNumber == 2:
				embed.description = "Paper!"
			elif randomNumber == 3:
				embed.description = "Scissors!"
			await ctx.send(embed=embed)
		else:
			await ctx.send("Please put one of the required arguments. Arguments: 'rock', 'paper' or 'scissors'")
			raise Exception("No keyword argument specified for the command to run properly. Please put the required arguments and try again.")

def setup(bot):
	bot.add_cog(Fun(bot))