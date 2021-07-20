import discord
from discord.ext import commands
from PIL import Image
from io import BytesIO

core_color = discord.Color.from_rgb(30, 144, 255)


class ImageManipulation(commands.Cog, name="Image Manipulation"):
	def __init__(self, bot):
		self.bot = bot
	@staticmethod
	def pixelate(image: Image) -> Image:
		return image.resize((32, 32), resample=Image.NEAREST).resize((1024, 1024), resample=Image.NEAREST)

	@staticmethod
	def quantize(image: Image) -> Image:
		return image.quantize()

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
	@commands.command(name="8bit", description = "Makes your profile picture 8 bit, retro style.", aliases = ["8bitify", "make8bit"])
	async def eightbit_command(self, ctx):
			async with ctx.typing():
				image_bytes = await ctx.author.avatar_url.read()
				avatar = Image.open(BytesIO(image_bytes))
				avatar = avatar.convert("RGBA").resize((1024, 1024))

				eightbit = self.pixelate(avatar)
				eightbit = self.quantize(eightbit)

				bufferedio = BytesIO()
				eightbit.save(bufferedio, format="PNG")
				bufferedio.seek(0)

				file = discord.File(bufferedio, filename="8bitavatar.png")

				embed = discord.Embed(
					title=f"{user.name}'s 8-bit avatar",
					description='I think it looks pretty cool!',
					color = core_color
			)

				embed.set_image(url="attachment://8bitavatar.png")
				embed.set_footer(text=f"Made by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

			await ctx.send(file=file, embed=embed)

def setup(bot):
	bot.add_cog(ImageManipulation(bot))
