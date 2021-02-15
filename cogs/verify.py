import discord
from discord.ext import commands

class Verififcation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(name="verify", description="A command for servers to use so that they can add a verification stage to prevent alternative accounts in their server.", aliases=["verification"], usage="verify")	
	async def verify(self, ctx):
		dataset = await bot.config.find_by_id(ctx.guild.id)
		verification_role = dataset["verification_role"]

		if get(ctx.guild.roles, name=verification_role) == None:
			raise Exception("Configuration contains invalid argument.")
			return

		if dataset["manualverification"] == False:
			member = ctx.message.author
			role = get(member.guild.roles, name=verification_role)
			if role in member.roles:
				embed = discord.Embed(title="Verification", description="You are already verified. No roles have been added.", color=core_color)
				embed.set_thumbnail(url=ctx.bot.user.avatar_url)
				await ctx.send(embed=embed)
			else:
				await member.add_roles(role)
				embed = discord.Embed(title="Verification", color=core_color)
				embed.add_field(name="Added Roles", value=verification_role)
				embed.set_thumbnail(url=ctx.bot.user.avatar_url)
				await ctx.send(embed=embed)
		elif dataset["manualverification"] == True:
			member = ctx.message.author
			role = get(member.guild.roles, name=verification_role)
			letters = string.ascii_lowercase
			result_str = ''.join(choice(letters) for i in range(20))
			embed = discord.Embed(title="Manual Verification", description=f"Please type this code in chat:\n\n{result_str}", color=core_color)
			embed.set_thumbnail(url=ctx.bot.user.avatar_url)
			await ctx.send(embed=embed)
			try:
				Message = await bot.wait_for('message', timeout=300)
				if Message.content.lower() == str(result_str):
					if role in member.roles:
						embed = discord.Embed(title="Verification", description="You are already verified. No roles have been added.", color=core_color)
						embed.set_thumbnail(url=ctx.bot.user.avatar_url)
						await ctx.send(embed=embed)
					else:
						await member.add_roles(role)
						embed = discord.Embed(title="Verification", color=core_color)
						embed.add_field(name="Added Roles", value=verification_role)
						embed.set_thumbnail(url=ctx.bot.user.avatar_url)
						await ctx.send(embed=embed)
			except Exception as e:
				return

def setup(bot):
	bot.add_cog(Verififcation(bot))
