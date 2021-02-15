import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, has_role

core_color = discord.Color.from_rgb(30, 144, 255)

class LCRP(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	def is_in_guild(guild_id):
		async def predicate(ctx):
			return ctx.guild and ctx.guild.id == guild_id
		return commands.check(predicate)

	@commands.command()
	@is_in_guild(722195079262896239)
	@has_role("[-] 𝙎𝙩𝙖𝙛𝙛")
	async def duty(self, ctx, arg1="On-Duty"):
		channel = discord.utils.get(ctx.message.channel.guild.text_channels , name="on-duty")
		embed = discord.Embed(title="Duty Changed", color=core_color)
		embed.add_field(name="Name", value=ctx.author.name, inline=True)
		if arg1.lower() == "off" or arg1 == "off-duty":
			embed.add_field(name="Status", value="Off-Duty", inline=True)
		else:
			embed.add_field(name="Status", value="On-Duty", inline=True)
		embed.add_field(name="Time", value=f"{datetime.utcnow()}")
		embed.set_thumbnail(url=str(ctx.message.author.avatar_url))
		await channel.send(embed=embed)

	@commands.command(name="code", aliases=["server_code", "getservercode"])
	@is_in_guild(722195079262896239)
	async def code(self, ctx):
		embed = discord.Embed(title="Server Code", color=core_color)
		embed.set_thumbnail(core_image)
		embed.add_field(name="Server Code", value="AvvxY", inline=False)
		embed.add_field(name="Discord Code", value="BGryYXC", inline=False)
		await ctx.send(embed=embed)






def setup(bot):
	bot.add_cog(LCRP(bot))