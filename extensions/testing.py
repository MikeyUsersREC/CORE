from discord.ext import commands
import discord
core_color = discord.Color.from_rgb(30, 144, 255)


@commands.command()
async def test(ctx, *, args):
  await ctx.send(args)
  return

  def setup(bot):
    bot.add_command(test)