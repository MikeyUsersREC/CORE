from discord.ext import commands
import discord
from discord.ext.commands import has_permissions
core_color = discord.Color.from_rgb(30, 144, 255)

@commands.command()
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(member.server.roles, name='Muted')
    await member.add_roles()
    embed=discord.Embed(title="User muted!", description="**{0}** was muted by **{1}**!".format(member, ctx.author.name), color=core_color)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=embed)

@commands.command()
@has_permissions()
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(member.server.roles, name='Muted')
    await member.remove_roles(member, role)
    embed=discord.Embed(title="User muted!", description="**{0}** was unmuted by **{1}**!".format(member, ctx.author.name), color=core_color)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=embed)

def setup(bot):
    bot.add_command(mute)