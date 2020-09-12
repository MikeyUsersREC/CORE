from discord.ext import commands
import discord
bot = commands.Bot(command_prefix='!' , description=None)
import asyncio
from random import randint
from discord.ext.commands import CheckFailure
from discord.ext.commands import has_role

@bot.event
async def on_ready():
    print("Bot online!")
    print("Logged into " + bot.user.name + "#" + bot.user.discriminator + "!")
    await bot.change_presence(activity=discord.Game(name="with Kevinator"))

@bot.command()
async def rps(ctx):
    num = randint(1, 3)
    embed = discord.Embed(title="Rock Paper Scissors!", color=discord.Color.from_rgb(0, 255, 0))
    if num == 1:
        embed.description = "Rock!"
    elif num == 2:
        embed.description = "Paper!"
    elif num == 3:
        embed.description = "Scissors!"
    await ctx.send("", embed=embed)
@bot.command()
@has_role("Bot Access")
async def announce(ctx):
    channel = ctx.message.channel
    announcements = discord.utils.get(ctx.message.channel.guild.text_channels , name="📢announcements")
    areSureEmbed = discord.Embed(title="Announcement" , description="What is the body of the announcement?" ,
                                 color=discord.Color.from_rgb(0, 255, 0))
    await ctx.send("" , embed=areSureEmbed)

    def check(m):
        return m.channel == channel and m.author == ctx.message.author

    try:
        msg = await bot.wait_for('message' , check=check , timeout=120)
        if msg.content == "cancel":
            cancelEmbed = discord.Embed(title="Announcement" , description="Successfully cancelled!" ,
                                            color=discord.Color.from_rgb(0, 255, 0))
            await channel.send("" , embed=cancelEmbed)
            return
        CategoryEmbed = discord.Embed(title="Announcement" ,
                                                     description="What catgegory is your announcement? Categories: information, warning, important",
                                                     color=discord.Color.from_rgb(0, 255, 0))

        await channel.send(''.format(msg) , embed=CategoryEmbed)
    except asyncio.TimeoutError:
        TimeoutEmbed = discord.Embed(title="Timeout!" ,
                                         description="You have reached the 120 second timeout! Please send another command if you want to continue!" ,
                                         color=discord.Color.from_rgb(0, 0, 255))
        await channel.send("" , embed=TimeoutEmbed)

    def yesCheck(m):
        return m.channel == channel and m.author == ctx.message.author
    try:
        categoryMsg = await bot.wait_for('message' , check=check , timeout=120)
        if msg.content == "cancel":
            cancelEmbed = discord.Embed(title="Announcement" , description="Successfully cancelled!" ,
                                            color=discord.Color.from_rgb(0, 0, 255))
            await channel.send("" , embed=cancelEmbed)
            return
        SendingAnnouncementEmbed = discord.Embed(title="Announcement" ,
                                                     description="Are you sure you want to send this announcement?\n\n" + msg.content ,
                                                     color=discord.Color.from_rgb(0, 0, 255))

        await channel.send(''.format(msg) , embed=SendingAnnouncementEmbed)
    except asyncio.TimeoutError:
        TimeoutEmbed = discord.Embed(title="Timeout!" ,
                                         description="You have reached the 120 second timeout! Please send another command if you want to continue!" ,
                                         color=discord.Color.from_rgb(0, 0, 255))
        await channel.send("" , embed=TimeoutEmbed)
    try:
        Message = await bot.wait_for('message' , check=yesCheck , timeout=120)
        if Message.content == "cancel" or Message.content == "no":
            cancelEmbed = discord.Embed(title="Announcement" , description="Successfully cancelled!" ,
                                            color=discord.Color.from_rgb(0, 0, 255))
            await channel.send("" , embed=cancelEmbed)
            return
        if categoryMsg.content == "placeholder":
            AnnouncementEmbed = discord.Embed(title="KG | Information" , description=msg.content ,

                                              color=discord.Color.from_rgb(0 , 0 , 255))
            AnnouncementEmbed.set_thumbnail(
                url="https://media.discordapp.net/attachments/733628287548653669/754109649074257960/768px-Logo_informations.png?width=468&height=468")

        elif categoryMsg.content == "information":
            AnnouncementEmbed = discord.Embed(title="KG | Information" , description=msg.content ,

                                              color=discord.Color.from_rgb(0 , 0 , 255))
            AnnouncementEmbed.set_thumbnail(
                url="https://media.discordapp.net/attachments/733628287548653669/754109649074257960/768px-Logo_informations.png?width=468&height=468")

        elif categoryMsg.content == "important":
            AnnouncementEmbed = discord.Embed(title=":loudspeaker: Important Announcement" , description=msg.content ,

                                              color=discord.Color.from_rgb(255 , 0 , 0))
            AnnouncementEmbed.set_thumbnail(
                url="https://cdn.discordapp.com/icons/722195079262896239/a_5601885314afd8e105fc079a7df408da.webp?size=128")
        elif categoryMsg.content == "warning":
            AnnouncementEmbed = discord.Embed(title=":warning: Warning Announcement" , description=msg.content ,

                                              color=discord.Color.from_rgb(252, 206, 0))
            AnnouncementEmbed.set_thumbnail(
                url="https://cdn.discordapp.com/emojis/746034342303891585.png?v=1")
            await announcements.send("", embed=AnnouncementEmbed)
            return
        elif categoryMsg.content == "critical":
            if ctx.message.author.id == 635119023918415874:
                AnnouncementEmbed = discord.Embed(title=":no_entry_sign: | Critical Announcement" ,
                                                  description=msg.content ,

                                                  color=discord.Color.from_rgb(255 , 0 , 0))
            else:
                UnauthorisedUseOfCritical = discord.Embed(title=":no_entry_sign: You are unauthorised to use this category.", description="You are not authorised to use this category, please use another category, this category can only be used by the Bot Developer.", color= discord.Color.from_rgb(255, 0, 0))
                await ctx.send("", embed=UnauthorisedUseOfCritical)
                return
        elif categoryMsg.content == "developmentWithPing":
            if ctx.message.author.id == 635119023918415874:
                TestingEmbed = discord.Embed(title=":construction: Development Announcement" ,
                                                  description=msg.content ,

                                                  color=discord.Color.from_rgb(255, 145, 0))
                await announcements.send("@everyone", embed=TestingEmbed)
                return
            else:
                PleaseTryAgain = discord.Embed(title="Error:" ,
                                               description="You did not put the one of the valid categories available for this announcement, please try again." ,
                                               color=discord.Color.from_rgb(255 , 0 , 0))
                await ctx.send("" , embed=PleaseTryAgain)
                return
        elif categoryMsg.content == "development":
            if ctx.message.author.id == 635119023918415874:
                TestingEmbed = discord.Embed(title=":construction: Development Announcement" ,
                                             description=msg.content ,

                                             color=discord.Color.from_rgb(255 , 145 , 0))
                await announcements.send("" , embed=TestingEmbed)
                return
            else:
                PleaseTryAgain = discord.Embed(title="Error:" ,
                                               description="You did not put the one of the valid categories available for this announcement, please try again." ,
                                               color=discord.Color.from_rgb(255 , 0 , 0))
                await ctx.send("" , embed=PleaseTryAgain)
                return


        else:
            PleaseTryAgain = discord.Embed(title="Error:", description="You did not put the one of the valid categories available for this announcement, please try again.", color= discord.Color.from_rgb(255, 0, 0))
            await ctx.send("", embed=PleaseTryAgain)
            return
        SendingAnnouncementEmbed = discord.Embed(title="Announcement" ,
                                                     description="Sending announcement...\n\n" + msg.content ,
                                                     color=discord.Color.dark_grey())
        await channel.send(''.format(msg) , embed=SendingAnnouncementEmbed)
        await announcements.send("@everyone" , embed=AnnouncementEmbed)
    except asyncio.TimeoutError:
        TimeoutEmbed = discord.Embed(title="Timeout!" ,
                                         description="You have reached the 120 second timeout! Please send another command if you want to continue!" ,
                                         color=discord.Color.from_rgb(0, 0, 255))
        await channel.send("" , embed=TimeoutEmbed)

@bot.command()
async def tag(ctx, argument):
    if argument == "mod":
        embed = discord.Embed(title="Moderator Form", url="https://forms.gle/fduX4QMDu29NTkLE9", color=discord.Color.fromrgb(252, 206, 0))
        await ctx.send(embed=embed)
    elif argument == "twitch":
        embed = discord.Embed(title="Kevinator's Twitch", url="https://twitch.tv/keviiinator", color=discord.Color.fromrgb(252, 206, 0))
        await ctx.send(embed=embed)
    elif argument == "discord":
        embed = discord.Embed(title="Discord Invite", url="discord.gg/P24XMKP", color=discord.Color.fromrgb(252, 206, 0))
        await ctx.send(embed=embed)
    return

@tag.error
async def tag_error(ctx, error):
    errorEmbed = discord.Embed(title="Something went wrong.", description="Have you put the correct arguments?\n\nSyntax:\n\n!tag [argument]", color=discord.Color.from_rgb(255, 0, 0))
    await ctx.send(embed=errorEmbed)
@announce.error
async def announce_error(ctx, error):
    if isinstance(error, CheckFailure):
        errorEmbed = discord.Embed(title="Something went wrong.", description="Something went wrong. The permission 'Bot Access' is required to run this command.", color= discord.Color.from_rgb(255, 0, 0))
        await ctx.send("", embed=errorEmbed)
    else:
        raise error

bot.run('NzM0NDk1NDg2NzIzMjI3NzYw.XxSiOg.3B_xKd3mkEOavNHMrXaMX0HN_04')