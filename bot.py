from discord.ext import commands
import discord
bot = commands.Bot(command_prefix='!' , description=None)
import os
bot.remove_command("help")
from random import choice
import asyncio
from random import randint
from discord.ext.commands import CheckFailure
from discord.ext.commands import has_role
from discord.ext.commands import has_permissions
from discord.utils import get
import json

core_color = discord.Color.from_rgb(30, 144, 255)
announcement_channel = "announcements"


@bot.event
async def on_ready():
    print("Bot online!")
    print("Logged into " + bot.user.name + "#" + bot.user.discriminator + "!")
    await bot.change_presence(activity=discord.Game(name="with CORE"))

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'extensions.{extension}')
    embed=discord.Embed(title="Extension loaded!", description=f"{extension}.py was loaded.", color=core_color)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=embed)

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'extensions.{extension}')

@bot.command()
@has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
    embed=discord.Embed(title="User muted!", description="**{0}** was muted by **{1}**!".format(member.display_name, ctx.author.name), color=core_color)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=embed)

@bot.command()
async def maths(ctx):
    num1 = randint(100, 1000)
    num2 = randint(1000, 5000)
    result = num1 + num2
    mathsEmbed = discord.Embed(title="Maths with CORE", description=f"Work out this calculation and say it in chat.\n\n{num1} + {num2}", color=core_color)
    mathsEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=mathsEmbed)
    asyncio.sleep(1)
    msg = await bot.wait_for("message")
    if msg.content == str(result):
        succesfulEmbed = discord.Embed(title="Maths with CORE", description="You successfully guessed the answer.", color=core_color)
        succesfulEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
        await ctx.send(embed=succesfulEmbed)
    else:
        failureEmbed = discord.Embed(title="Maths with CORE", description="Answer was incorrect.", color=core_color)
        failureEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
        await ctx.send(embed=failureEmbed)

@bot.command()
@has_permissions(manage_messages=True) 
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.remove_roles(role)
    embed=discord.Embed(title="User unmuted!", description="**{0}** was unmuted by **{1}**!".format(member.display_name, ctx.author.name), color=core_color)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=embed)

@bot.command()
async def info(ctx, *, member: discord.Member):
    fmt = '{0} joined on {0.joined_at} and has {1} roles.'
    infoEmbed = discord.Embed(title="Information", description=fmt.format(member, len(member.roles)), color=core_color)
    infoEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=infoEmbed)

@bot.command()
async def rps(ctx, arg):
    embed = discord.Embed(title="Rock Paper Scissors!", color=core_color)
    if arg.lower() == "rock":
        embed.description = "Paper!"
    elif arg.lower() == "paper":
        embed.description = "Scissors!"
    elif arg.lower() == "scissors":
        embed.description = "Rock!"
    await ctx.send(embed=embed)

@bot.command()
async def set(ctx,*,channel):
    global announcement_channel
    announcement_channel = channel
    embed = discord.Embed(title="Successfully Changed", description="The announcement channel has been changed.", color=core_color)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=embed)

@bot.command()
@has_permissions(manage_channels=True) 
async def announce(ctx):
    channel = ctx.message.channel
    announcements = discord.utils.get(ctx.message.channel.guild.text_channels , name=announcement_channel)
    areSureEmbed = discord.Embed(title="Announcement" , description="What is the body of the announcement?" ,
                                 color=core_color)
    await ctx.send("" , embed=areSureEmbed)

    def check(m):
        return m.channel == channel and m.author == ctx.message.author

    try:
        msg = await bot.wait_for('message' , check=check , timeout=120)
        if msg.content == "cancel":
            cancelEmbed = discord.Embed(title="Announcement" , description="Successfully cancelled!" ,
                                            color=core_color)
            await channel.send("" , embed=cancelEmbed)
            return
        CategoryEmbed = discord.Embed(title="Announcement" ,
                                                     description="What catgegory is your announcement? Categories: information, warning, important",
                                                     color=core_color)

        await channel.send(''.format(msg) , embed=CategoryEmbed)
    except asyncio.TimeoutError:
        TimeoutEmbed = discord.Embed(title="Timeout!" ,
                                         description="You have reached the 120 second timeout! Please send another command if you want to continue!" ,
                                         color=core_color)
        await channel.send("" , embed=TimeoutEmbed)

    def yesCheck(m):
        return m.channel == channel and m.author == ctx.message.author
    try:
        categoryMsg = await bot.wait_for('message' , check=check , timeout=120)
        if msg.content == "cancel":
            cancelEmbed = discord.Embed(title="Announcement" , description="Successfully cancelled!" ,
                                            color=core_color)
            await channel.send("" , embed=cancelEmbed)
            return
        SendingAnnouncementEmbed = discord.Embed(title="Announcement" ,
                                                     description="Are you sure you want to send this announcement?\n\n" + msg.content ,
                                                     color=core_color)

        await channel.send(''.format(msg) , embed=SendingAnnouncementEmbed)
    except asyncio.TimeoutError:
        TimeoutEmbed = discord.Embed(title="Timeout!" ,
                                         description="You have reached the 120 second timeout! Please send another command if you want to continue!" ,
                                         color=core_color)
        await channel.send("" , embed=TimeoutEmbed)
    try:
        Message = await bot.wait_for('message' , check=yesCheck , timeout=120)
        if Message.content == "cancel" or Message.content == "no":
            cancelEmbed = discord.Embed(title="Announcement" , description="Successfully cancelled!" ,
                                            color=core_color)
            await channel.send("" , embed=cancelEmbed)
            return
        if categoryMsg.content == "placeholder":
            AnnouncementEmbed = discord.Embed(title="CORE | Information" , description=msg.content ,

                                              color=core_color)
            AnnouncementEmbed.set_thumbnail(
                url="https://media.discordapp.net/attachments/733628287548653669/754109649074257960/768px-Logo_informations.png?width=468&height=468")

        elif categoryMsg.content == "information":
            AnnouncementEmbed = discord.Embed(title="CORE | Information" , description=msg.content ,

                                              color=discord.Color.from_rgb(0 , 0 , 255))
            AnnouncementEmbed.set_thumbnail(
                url="https://media.discordapp.net/attachments/733628287548653669/754109649074257960/768px-Logo_informations.png?width=468&height=468")

        elif categoryMsg.content == "important":
            AnnouncementEmbed = discord.Embed(title=":loudspeaker: Important Announcement" , description=msg.content ,

                                              color=discord.Color.from_rgb(255 , 0 , 0))
            AnnouncementEmbed.set_thumbnail(
                url="https://cdn.discordapp.com/emojis/746034342303891585.png?v=1")
        elif categoryMsg.content == "warning":
            AnnouncementEmbed = discord.Embed(title=":warning: Warning Announcement" , description=msg.content ,

                                              color=discord.Color.from_rgb(252, 206, 0))
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
                TestingEmbed = discord.Embed(title=":construction:  Development Announcement" ,
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
                TestingEmbed = discord.Embed(title=":construction:  Development Announcement" ,
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
                                                     color=core_color)
        await channel.send(''.format(msg) , embed=SendingAnnouncementEmbed)
        await announcements.send("@everyone" , embed=AnnouncementEmbed)
    except asyncio.TimeoutError:
        TimeoutEmbed = discord.Embed(title="Timeout!" ,
                                         description="You have reached the 120 second timeout! Please send another command if you want to continue!" ,
                                         color=core_color)
        await channel.send("" , embed=TimeoutEmbed)

@bot.command()
@has_permissions(kick_members=True) 
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    kickEmbed = discord.Embed(title="Successfully Kicked.", description=member.display_name + " was kicked for: " + reason, color=core_color)
    if reason == None:
        kickEmbed.description = member.display_name + "was kicked successfully."
    await ctx.send(embed=kickEmbed)

@bot.command()
@has_permissions(ban_members=True) 
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    banEmbed = discord.Embed(title="Successfully Banned.", description=member.display_name + " was banned for: " + reason, color=core_color)
    if reason == None:
        banEmbed.description = member.display_name + "was banned successfully."
    await ctx.send(embed=banEmbed)


@bot.command()
async def categories(ctx):
    f = discord.Embed(title="Categories", description="These are the categories for the CORE Announce command:\n\ninformation,\nimportant,\nwarning", color=core_color)
    f.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=f)


@bot.command()
async def random(ctx):
    randomMember = choice(ctx.guild.members)
    await ctx.send(f'{randomMember.mention} is the chosen one!')

@bot.command()
async def help(ctx):
    helpEmbed = discord.Embed(color=core_color, title="CORE | Help")
    helpEmbed.set_footer(text="CORE | Help")
    helpEmbed.add_field(name="!help", value="Help Command for CORE", inline=False)
    helpEmbed.add_field(name="!rps", value="Rock Paper Scissors", inline=False)
    helpEmbed.add_field(name="!maths", value="A maths game where you need to work out the answer for a random calculation!", inline=False)
    helpEmbed.add_field(name="!random", value="Chooses a random user and says that they are the chosen one", inline=False)
    helpEmbed.add_field(name="!purge", value="To clear a selected amount of messages in that channel", inline=False)
    helpEmbed.add_field(name="!update", value="Specifies the most recent update for CORE", inline=False)
    helpEmbed.add_field(name="!kick", value="Kicks a user that you specify", inline=False)
    helpEmbed.add_field(name="!ban", value="Bans a user that you specify", inline=False)
    helpEmbed.add_field(name="!announce", value="Announces a message in the announcement channel", inline=False)
    helpEmbed.add_field(name="!load", value="Loads a specific extension", inline=False)
    helpEmbed.add_field(name="!unload", value="Unloads a specific extension", inline=False)
    helpEmbed.add_field(name="!categories", value="Specifies the available announcement categories", inline=False)
    helpEmbed.add_field(name="!info", value="Specifies information about a certain member", inline=False)
    helpEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=helpEmbed)

@bot.command()
async def update(ctx):
    updateEmbed = discord.Embed(title="Most recent update:", description="- Added the !maths command\n- Now able to set your announcement channel\n- !mute and !unmute added", color=core_color)
    updateEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=updateEmbed)

@bot.command()
@has_permissions(manage_channels=True)
async def purge(ctx, amount=15):
    new_amount = amount + 1
    await ctx.channel.purge(limit=new_amount)

@announce.error
async def announce_error(ctx, error):
    if isinstance(error, CheckFailure):
        errorEmbed = discord.Embed(title="Something went wrong.", description="Something went wrong. The permission 'Manage Server' is required to run this command.", color= discord.Color.from_rgb(255, 0, 0))
        await ctx.send("", embed=errorEmbed)
    else:
        raise error


bot.run('NzM0NDk1NDg2NzIzMjI3NzYw.XxSiOg.3B_xKd3mkEOavNHMrXaMX0HN_04')
