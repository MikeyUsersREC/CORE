import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio

core_color = discord.Color.from_rgb(30, 144, 255)

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")


    @commands.command(name="mute", description="Mutes the mentioned user.", aliases=["m", "silence"], usage="mute <User>")
    @has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, time):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(role)
        embed=discord.Embed(title="User muted!", description="**{0}** was muted by **{1}**!".format(member.display_name, ctx.author.name), color=core_color)
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        await ctx.send(embed=embed)

        if str(time).endswith("s"):
            timeList = time.split("s")
            timeDown = int(timeList[0])
        elif str(time).endswith("m"):
            timeList = time.split("m")
            timeDown = int(timeList[0]) * 60
        elif str(time).endswith("h"):
            timeList = time.split("h")
            timeDown = int(timeList[0]) * 60 * 60
        elif str(time).endswith("d"):
            timeList = time.split("h")
            timeDown = int(timeList[0]) * 60 * 60 * 24
        await asyncio.sleep(timeDown)

        await member.remove_roles(role)

    @commands.command(name="unmute", aliases=["um", "unsilence"], description="Ummutes the mentioned user if they are already muted.", usage="unmute <User>")
    @has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if member.has_role(role):
            embed=discord.Embed(title="User unmuted!", description="**{0}** was muted by **{1}**!".format(member.display_name, ctx.author.name), color=core_color)
            embed.set_thumbnail(url=ctx.bot.user.avatar_url)
            await member.remove_roles(role)
        else:
            await ctx.send("That member is not muted.")
            return

    @commands.command(name="kick", aliases=["k", "removeuser"], description="Kick the mentioned user.", usage="kick <User>")
    @has_permissions(kick_members=True) 
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        kickEmbed = discord.Embed(title="Successfully Kicked.", description=member.display_name + " was kicked for: " + reason, color=core_color)
        kickEmbed.set_thumbnail(url=ctx.bot.user.avatar_url)
        if reason == None:
            kickEmbed.description = member.display_name + "was kicked successfully."
        await ctx.send(embed=kickEmbed)

    @commands.command(name="ban", aliases=["b", "blacklist"], description="Ban the mentioned user.", usage="ban <User>")
    @has_permissions(ban_members=True) 
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        banEmbed = discord.Embed(title="Successfully Banned", description=member.display_name + " was banned for: " + reason, color=core_color)
        banEmbed.set_thumbnail(url=ctx.bot.user.avatar_url)
        if reason == None:
            banEmbed.description = member.display_name + "was banned successfully."
        await ctx.send(embed=banEmbed)

    @commands.command(name="purge", aliases=["delete", "purgechannel", "purgemessages", "deletemessages", "p"], description="Deletes a certain amount of messages in the current channel.", usage="purge <Amount>")
    @has_permissions(manage_channels=True)
    async def purge(self, ctx, amount=15):
        new_amount = amount + 1
        await ctx.channel.purge(limit=new_amount)

    @commands.command(name="warn", description="Warn the mentioned user.", aliases=["w", "infract", "warnuser", "warnmember"], usage="warn <User> [Reason]")
    @has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *,reason=None):
        if not member.guild_permissions.manage_messages:
            topDataSet = await bot.warningData.find_by_id(ctx.guild.id)
            bottomDataSet = topDataSet[str(member.id)]
            if bottomDataSet["warnings"] == 0:
                bottomDataSet["warnings"] = 1
                warnings = bottomDataSet["warnings"]
                bottomDataSet["warningReasons"] = {"Warning 1": reason}
                await bot.warningData.update_by_id(topDataSet)
                embed = discord.Embed(title=f"Warned Successfully", color=core_color)       
                embed.add_field(name="User", value=f"{member.name}#{member.discriminator}", inline=False)
                embed.add_field(name="Warning Number", value=f"Warning {warnings}", inline=False)
                embed.add_field(name="Warned by:", value=f"{ctx.author.name}#{ctx.author.discriminator}", inline=False)
                embed.set_thumbnail(url=member.avatar_url)
                await ctx.send(embed=embed)
            elif bottomDataSet["warnings"] >= 1 or bottomDataSet["warnings"] == 1:
                bottomDataSet["warnings"] += 1
                warnings = bottomDataSet["warnings"]
                bottomDataSet["warningReasons"][f"Warning {warnings}"] = reason
                await bot.warningData.update_by_id(topDataSet)
                embed = discord.Embed(title=f"Warned Successfully", color=core_color)       
                embed.add_field(name="User", value=f"{member.name}#{member.discriminator}", inline=False)
                embed.add_field(name="Warning Number", value=f"Warning {warnings}", inline=False)
                embed.add_field(name="Warned by:", value=f"{ctx.author.name}#{ctx.author.discriminator}", inline=False)
                embed.set_thumbnail(url=member.avatar_url)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Command Failed", description="You are not allowed to warn this user.", color=core_color)
            embed.set_thumbnail(url=ctx.bot.user.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(name="get_log", aliases=["get_warnings", "warnings", "infractions", "gw"], description="Get the warnings of the mentioned user.", usage="get_log <User>")
    @has_permissions(manage_messages=True)
    async def get_log(self, ctx, member: discord.Member):
        topDataSet = await bot.warningData.find_by_id(ctx.guild.id)
        bottomDataSet = topDataSet[str(member.id)]
        warnings = bottomDataSet["warnings"]
        embed = discord.Embed(title=f"Warnings for {member.name}", color=core_color)
        embed.add_field(name="User", value=f"{member.name}#{member.discriminator}", inline=False)
        embed.add_field(name="Warning Amount", value=f"{warnings}")

        for warning in range(0, warnings):
            value = bottomDataSet["warningReasons"][f"Warning {warning}"]
            if f"Warning {warning}" in bottomDataSet["warningReasons"]:
                embed.add_field(name=f"Warning {warning}", value=f"{value}", inline=False)

        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=["clear_warns", "clearwarnings", "cw"], description="Clear the mentioned user's warnings.", usage="clearwarns <User>")
    @has_permissions(manage_messages=True)
    async def clearwarns(self, ctx, member: discord.Member):
        dataset = await bot.warningData.find_by_id(ctx.guild.id)
        dataset[str(member.id)] = {"_id": member.id, "warnings": 0, "kicks": 0, "guild_id": ctx.guild.id, "warningReasons": None}
        await bot.warningData.update_by_id(dataset)
        print(f"{member.name} in {ctx.guild.name} has been updated to warning database.")


def setup(bot):
    bot.add_cog(Moderation(bot))