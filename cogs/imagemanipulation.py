import discord
from discord.ext import commands
from PIL import Image
from io import BytesIO

core_color = discord.Color.from_rgb(30, 144, 255)


class ImageManipulation(commands.Cog, name="Image Manipulation"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="wanted", aliases=["makewanted", "deadoralive"], description="Makes the person you mention have a wanted poster after them.", usage="wanted <User>")
	async def wanted(self, ctx, user: discord.Member = None):
		if user == None:
			user = ctx.author

		wanted = Image.open(r'images\wanted.jpg')
		asset = user.avatar_url_as(size=128)
		data = BytesIO(await asset.read())
		pfp = Image.open(data)

		pfp = pfp.resize((177, 177))
		wanted.paste(pfp, (120, 212))
		wanted.save(r'images\wanted.jpg')

		await ctx.send(file = discord.File(r"images\wanted.jpg"))

def setup(bot):
	bot.add_cog(ImageManipulation(bot))