# Importing Packages

from datetime import datetime
from discord.ext import commands, tasks
import discord
import os
import asyncio
from random import randint, choice
from discord.ext.commands import CheckFailure, has_role, has_permissions
from discord.utils import get
import requests
import logging
import json
import string
from utils.mongo import Document
import motor.motor_asyncio
import traceback

# Creation & Configuration

async def get_prefix(client, message):
    mongo = motor.motor_asyncio.AsyncIOMotorClient("MONGO DB TOKEN")
    db = mongo["core"]
    prefixes = Document(db, "prefixes")
    if await prefixes.find_by_id(message.guild.id) == None:
        return "!"
    else:
        dataset = await prefixes.find_by_id(message.guild.id)
        return dataset["prefix"]


intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, description=None, intents=intents, case_insensitive=True)
bot.remove_command("help")


# Variables

token = "TOKEN HERE"
core_color = discord.Color.from_rgb(30, 144, 255)
mn_color = discord.Color.from_rgb(35, 35, 35)
meaxisnetwork_url = "https://meaxisnetwork.net/assets/images/square_logo.png"
# Logging

logging.basicConfig(level=logging.WARNING)

# Events

@bot.event
async def on_ready():
    member_count_all = 0
    print("Bot online!")
    print("Logged into " + bot.user.name + "#" + bot.user.discriminator + "!")
    print("___________\n")
    print("Bot Stats")
    print("\n___________")
    print(f"{str(len(bot.guilds))} Servers")
    for guild in bot.guilds:
        member_count_all += guild.member_count

    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient("MONGO DB TOKEN")
    bot.db = bot.mongo["core"]
    bot.config = Document(bot.db, "info")
    bot.warningData = Document(bot.db, "warnings")
    bot.prefixData = Document(bot.db, "prefixes")
    for document in await bot.config.get_all():
        print(document)

    for guild in bot.guilds:
        if await bot.config.find_by_id(guild.id) == None:
            await bot.config.insert({"_id": guild.id, "debug_mode": False, "announcement_channel": "announcements", "verification_role": "Verified", "manualverification": False, "link_automoderation": False})
    
    for guild in bot.guilds:
        if await bot.prefixData.find_by_id(guild.id) == None:
            await bot.prefixData.insert({"_id": guild.id, "prefix": "!"})

    for document in await bot.prefixData.get_all():
        print(document)

    print(f"{member_count_all} Members")
    bot.loop.create_task(status_change())
    bot.loop.create_task(warningDataUpdate())
    bot.load_extension(f'extensions.dbl')

    for guild in bot.guilds:

        print(f"{str(guild.id)} | {str(guild.name)} | {str(guild.member_count)} Members")

# @bot.event
# async def on_command_error(ctx, error):
#   if not isinstance(error, commands.CommandNotFound):
#       embed = discord.Embed(title="An error has occured.")
#       dataset = await bot.config.find_by_id(ctx.guild.id)
#       if dataset["debug_mode"]:
#           traceback.print_tb(error.__traceback__)
#       else:
#           embed = discord.Embed(title="An error has occured.", description="An error has occured that has prevented the command to run properly.")
#           embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
#           await ctx.send(embed=embed)


@bot.event
async def on_guild_join(guild):
    await bot.config.insert({"_id": guild.id, "debug_mode": False, "announcement_channel": "announcements", "verification_role": "Verified", "manualverification": False, "link_automoderation": False})
    await bot.warningData.insert({"_id": guild.id, "name": guild.name})
    for member in guild.members:
        dataset = await bot.warningData.find_by_id(guild.id)
        dataset[str(member.id)] = {"_id": member.id, "warnings": 0, "kicks": 0, "guild_id": guild.id}
        await bot.warningData.update_by_id(dataset)
        print(f"{member.name} in {guild.name} has been updated to warning database.")
    await bot.prefixData.insert({"_id": guild.id, "prefix": "!"})



@bot.event
async def on_message(message):
    if message.author.bot == False:

        dataset = await bot.config.find_by_id(message.guild.id)

        if dataset["manualverification"]:
            if "https://" in message.content or "discord.gg/" in message.content:
                if message.author.guild_permissions.manage_guild:
                    await bot.process_commands(message)
                else:
                    await message.delete()
            await bot.process_commands(message)
        await bot.process_commands(message)

async def status_change():
    while True:
        statusTable = ["with CORE", "CORE Games", "over CORE Support", "with MikeyCorporation", "commands"]
        statusChosen = choice(statusTable)
        if statusChosen != "over CORE Support" and statusChosen != "commands":
            await bot.change_presence(activity=discord.Game(name=statusChosen))
        elif statusChosen == "over CORE Support":
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=statusChosen))
        else:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=statusChosen))
        await asyncio.sleep(10)


async def warningDataUpdate():
    await asyncio.sleep(3600)
    while True:
        for guild in bot.guilds:
            if await bot.warningData.find_by_id(guild.id) == None:
                await bot.warningData.insert({"_id": guild.id, "name": guild.name})
                for member in guild.members:
                    dataset = await bot.warningData.find_by_id(guild.id)
                    dataset[str(member.id)] = {"_id": member.id, "warnings": 0, "kicks": 0, "guild_id": guild.id}
                    await bot.warningData.update_by_id(dataset)
                    print(f"{member.name} in {guild.name} has been updated to warning database.")
            elif await bot.warningData.find_by_id(guild.id) != None:
                for member in guild.members:
                    dataset = await bot.warningData.find_by_id(guild.id)
                    if dataset[str(member.id)] == None:
                        dataset[str(member.id)] = {"_id": member.id, "warnings": 0, "kicks": 0, "guild_id": guild.id}
                        await bot.warningData.update_by_id(dataset)
                        print(f"{member.name} in {guild.name} has been updated to warning database.")
            

# Commands

@bot.command(aliases=["clearwarns", "clearwarnings"])
@has_permissions(manage_messages=True)
async def clear_warns(ctx, member: discord.Member):
    dataset = await bot.warningData.find_by_id(ctx.guild.id)
    dataset[str(member.id)] = {"_id": member.id, "warnings": 0, "kicks": 0, "guild_id": ctx.guild.id, "warningReasons": None}
    await bot.warningData.update_by_id(dataset)
    print(f"{member.name} in {ctx.guild.name} has been updated to warning database.")


@bot.command()
@has_permissions(manage_guild=True)
async def prefix(ctx, arg=None):
    if arg == None:
        dataset = await bot.prefixData.find_by_id(ctx.guild.id)
        prefix = dataset["prefix"]
        await ctx.send(f"My prefix is `{prefix}`")
    else:
        dataset = await bot.prefixData.find_by_id(ctx.guild.id)
        dataset["prefix"] = arg
        await bot.prefixData.update_by_id(dataset)
        await ctx.send(f"My prefix has been changed to `{arg}`")

@bot.command()
async def load(ctx, extension):
    extensionLowered = extension.lower()
    bot.load_extension(f'extensions.{extensionLowered}')
    embed = discord.Embed(title="Extension loaded!", description=f"{extensionLowered}.py was loaded.", color=core_color)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=embed)

@bot.command()
async def support(ctx):
    embed = discord.Embed(title="Support", description="Support Server: https://discord.gg/YH8WQCT", color=core_color)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=embed)

@bot.command()
async def invite(ctx):
    embed = discord.Embed(title="Bot Invite", description="https://discord.com/api/oauth2/authorize?client_id=734495486723227760&permissions=8&scope=bot", color=core_color)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=embed)

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'extensions.{extension}')

@bot.command()
@has_permissions(manage_guild=True)
async def config(ctx, arg1=None, *, arg2=None):
    if arg1 == "debug":
        if arg2 == "on":

            dataset = await bot.config.find_by_id(ctx.guild.id)

            dataset["debug_mode"] = True

            await bot.config.update_by_id(dataset)

            embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
            await ctx.send(embed=embed)

        elif arg2 == "off":
            dataset = await bot.config.find_by_id(ctx.guild.id)

            dataset["debug_mode"] = False

            await bot.config.update_by_id(dataset)

            embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
            await ctx.send(embed=embed)

    if arg1 == "manualverification":
        if arg2 == "on" or arg2 == "true":
            dataset = await bot.config.find_by_id(ctx.guild.id)

            dataset["manualverification"] = True

            await bot.config.update_by_id(dataset)

            embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
            await ctx.send(embed=embed)
        else:
            dataset = await bot.config.find_by_id(ctx.guild.id)

            dataset["manualverification"] = False

            await bot.config.update_by_id(dataset)
            embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
            await ctx.send(embed=embed)

    if arg1 == "announcement_channel":
        dataset = await bot.config.find_by_id(ctx.guild.id)

        dataset["announcement_channel"] = arg2

        await bot.config.update_by_id(dataset)
        embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
        await ctx.send(embed=embed)

    if arg1 == "verification_role":
        dataset = await bot.config.find_by_id(ctx.guild.id)

        dataset["verification_role"] = arg2

        await bot.config.update_by_id(dataset)

        embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
        await ctx.send(embed=embed)

    if arg1 == "link_automoderation":
        if arg2 == "on":
            dataset = await bot.config.find_by_id(ctx.guild.id)

            dataset["link_automoderation"] = True

            await bot.config.update_by_id(dataset)
            embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
            await ctx.send(embed=embed)

        elif arg2 == "off":
            dataset = await bot.config.find_by_id(ctx.guild.id)

            dataset["link_automoderation"] = False

            await bot.config.update_by_id(dataset)

            embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
            await ctx.send(embed=embed)

    if arg1 is None and arg2 is None:
        embed = discord.Embed(title="Settings and Configurations", description="__**Configurations**__\n\n**debug** | Debug Mode sends errors in the chat rather than the console.\n\n**manualverification** | Manual Verifications enables code-based chat authenticated verification for servers.\n\n**announcement_channel** | Sets the announcement channel.\n\n**verification_role** | Sets the verification role for servers.\n\n**link_automoderation** | The bot can check for links.", color=core_color)
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
        await ctx.send(embed=embed)
# MeaxisNetwork Commands

@bot.command()
async def profile(ctx):
    payload = {"discordid": ctx.author.id, "secret": "t6ovhm._7-ng9iry-1602428551-gy1pn37w.u06x8_q", "scope": "username"}
    usernameRequest = requests.get("https://api.meaxisnetwork.net/v2/accounts/fromdiscord/", params=payload)
    usernameJSON = usernameRequest.json()
    username = usernameJSON["message"]

    payload = {"discordid": ctx.author.id, "secret": "t6ovhm._7-ng9iry-1602428551-gy1pn37w.u06x8_q", "scope": "description"}
    descriptionRequest = requests.get("https://api.meaxisnetwork.net/v2/accounts/fromdiscord/", params=payload)
    descriptionJSON = descriptionRequest.json()
    description = descriptionJSON["message"]
    descriptionFixed = description.replace("\r", "")

    payload = {"discordid": ctx.author.id, "secret": "t6ovhm._7-ng9iry-1602428551-gy1pn37w.u06x8_q", "scope": "profilepicture"}
    avatarRequest = requests.get("https://api.meaxisnetwork.net/v2/accounts/fromdiscord/", params=payload)
    avatarJSON = avatarRequest.json()
    avatarURLSource = descriptionJSON["message"]
    avatarURLString = str(avatarURLSource)
    avatarURLFixed = avatarURLString.replace(r'\/','/')

    payload = {"discordid": ctx.author.id, "secret": "t6ovhm._7-ng9iry-1602428551-gy1pn37w.u06x8_q", "scope": "id"}
    accountIDRequest = requests.get("https://api.meaxisnetwork.net/v2/accounts/fromdiscord/", params=payload)
    accountIDJSON = accountIDRequest.json()
    AccountID = accountIDJSON["message"]

    embed = discord.Embed(title=username, color=mn_color)
    embed.add_field(name = "Description", value = description, inline = False)
    embed.add_field(name = "Account ID", value = AccountID, inline = False)
    embed.set_thumbnail(url=meaxisnetwork_url)
    await ctx.send(embed=embed)

@bot.command()
async def funfact(ctx):
    funfactRequest = requests.get("https://api.meaxisnetwork.net/v2/funfact/")
    funfactJSON = funfactRequest.json()
    funfact = funfactJSON["text"]
    funfactID = funfactJSON["id"]
    funfactAuthor = funfactJSON["author"]
    
    embed = discord.Embed(title=f"Funfact #{funfactID}", color=mn_color)
    embed.add_field(name = "Funfact:", value = funfact, inline = False)
    embed.add_field(name = "Author", value = funfactAuthor, inline = False)
    embed.set_thumbnail(url=meaxisnetwork_url)
    await ctx.send(embed=embed)

@bot.command()
async def leafy(ctx):
    leafyRequest = requests.get("https://api.meaxisnetwork.net/v2/leafy/")
    embed = discord.Embed(title=f"Leafy API Status", color=mn_color)
    if leafyRequest.status_code == 200:
        embed.add_field(name = "Status:", value ="Online", inline = False)
    else:
        embed.add_field(name = "Status:", value ="Offline", inline = False)
    embed.set_thumbnail(url=meaxisnetwork_url)
    await ctx.send(embed=embed)
    return

@bot.command()
async def finduser(ctx, username):
    payload = {"username": username}
    usernameRequest = requests.get("https://api.meaxisnetwork.net/v2/accounts/exists/", params=payload)
    usernameJSON = usernameRequest.json()
    usernameResult = usernameJSON["message"]
    embed = discord.Embed(title="User Result", color=mn_color)
    embed.add_field(name = "Username Entered:", value = username, inline = False)
    embed.add_field(name = "Result:", value = usernameResult, inline = False)
    embed.set_thumbnail(url=meaxisnetwork_url)
    await ctx.send(embed=embed)

@bot.command()
async def run(ctx, *, cmd):
    if ctx.author.id == 635119023918415874:
        if cmd == "ManualWarningDataUpdate":
            for guild in bot.guilds:
                if await bot.warningData.find_by_id(guild.id) == None:
                    await bot.warningData.insert({"_id": guild.id, "name": guild.name})
                    for member in guild.members:
                        dataset = await bot.warningData.find_by_id(guild.id)
                        dataset[str(member.id)] = {"_id": member.id, "warnings": 0, "kicks": 0, "guild_id": guild.id}
                        await bot.warningData.update_by_id(dataset)
                        await ctx.send(f"{member.name} in {guild.name} has been updated to warning database.")
                elif await bot.warningData.find_by_id(guild.id) != None:
                    for member in guild.members:
                        dataset = await bot.warningData.find_by_id(guild.id)
                        if dataset[str(member.id)] == None:
                            dataset[str(member.id)] = {"_id": member.id, "warnings": 0, "kicks": 0, "guild_id": guild.id}
                            await bot.warningData.update_by_id(dataset)
                            await ctx.send(f"{member.name} in {guild.name} has been updated to warning database.")


@bot.command()
@has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *,reason=None):
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
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
        await ctx.send(embed=embed)



@bot.command(name="get_log", aliases=["get_warnings", "warnings"])
@has_permissions(manage_messages=True)
async def get_log(ctx, member: discord.Member):
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


@bot.command()
@has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, time):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
    embed=discord.Embed(title="User muted!", description="**{0}** was muted by **{1}**!".format(member.display_name, ctx.author.name), color=core_color)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
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


@bot.command()
async def maths(ctx, arg="practise", arg2="add", arg3=5, arg4=91):
    if arg == "practise":
        num1 = randint(100, 1000)
        num2 = randint(1000, 5000)
        result = num1 + num2
        mathsEmbed = discord.Embed(title="Maths with CORE", description=f"Work out this calculation and say it in chat.\n\n{num1} + {num2}", color=core_color)
        mathsEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
        await ctx.send(embed=mathsEmbed)
        try:
            msg = await bot.wait_for("message")
            if msg.content == str(result):
                succesfulEmbed = discord.Embed(title="Maths with CORE", description="You successfully guessed the answer.", color=core_color)
                succesfulEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
                await ctx.send(embed=succesfulEmbed)
            else:
                failureEmbed = discord.Embed(title="Maths with CORE", description="Answer was incorrect.", color=core_color)
                failureEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
                await ctx.send(embed=failureEmbed)
        except:
            return
    elif arg == "operation":
        if arg2 == "add":
            number = arg3 + arg4
            addEmbed = discord.Embed(title="Maths with CORE", description=f"Answer is: {number}", color=core_color)
            addEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
            await ctx.send(embed=addEmbed)
        if arg2 == "minus" or arg2 == "subtract":
            number = arg3 - arg4
            subtractEmbed = discord.Embed(title="Maths with CORE", description=f"Answer is: {number}", color=core_color)
            subtractEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
            await ctx.send(embed=subtractEmbed)
        if arg2 == "multiply" or arg2 == "times":
            number = arg3 * arg4
            multiplyEmbed = discord.Embed(title="Maths with CORE", description=f"Answer is: {number}", color=core_color)
            multiplyEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
            await ctx.send(embed=multiplyEmbed)
        if arg2 == "divide" or arg2 == "share":
            number = arg3 / arg4
            divideEmbed = discord.Embed(title="Maths with CORE", description=f"Answer is: {number}", color=core_color)
            divideEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
            await ctx.send(embed=divideEmbed)

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
    randomNumber = randint(1, 3)
    embed = discord.Embed(title="Rock Paper Scissors!", color=core_color)
    if arg.lower() == "rock" or arg.lower() == "paper" or arg.lower() == "scissors":
        if randomNumber == 1:
            embed.description = "Rock!"
        elif randomNumber == 2:
            embed.description = "Paper!"
        elif randomNumber == 3:
            embed.description = "Scissors!"

    if arg.lower() == "rock" or arg.lower() == "paper" or arg.lower() == "scissors":
        await ctx.send(embed=embed)
    else:
        await ctx.send("Please put one of the required arguments. Arguments: 'rock', 'paper' or 'scissors'")
        raise Exception("No keyword argument specified for the command to run properly. Please put the required arguments and try again.")
# Announcement Commands

@bot.command()
@has_permissions(manage_channels=True) 
async def announce(ctx):
    dataset = await bot.config.find_by_id(ctx.guild.id)

    announcement_channel = dataset["announcement_channel"]
    channel = ctx.message.channel
    announcements = discord.utils.get(ctx.message.channel.guild.text_channels , name=announcement_channel)
    areSureEmbed = discord.Embed(title="Announcement" , description="What is the body of the announcement?", color=core_color)
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
        TimeoutEmbed = discord.Embed(title="Timeout!", description="You have reached the 120 second timeout! Please send another command if you want to continue!" , color=core_color)
        await ctx.send(embed=TimeoutEmbed)
        return
    def yesCheck(m):
        return m.channel == channel and m.author == ctx.message.author
    try:
        categoryMsg = await bot.wait_for('message' , check=check , timeout=120)
        if msg.content == "cancel":
            cancelEmbed = discord.Embed(title="Announcement" , description="Successfully cancelled!", color=core_color)
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
        if categoryMsg.content == "important":
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

def is_in_guild(guild_id):
    async def predicate(ctx):
        return ctx.guild and ctx.guild.id == guild_id
    return commands.check(predicate)

@bot.command()
@is_in_guild(722195079262896239)
@has_role("[-] 𝙎𝙩𝙖𝙛𝙛")
async def duty(ctx, arg1="On-Duty"):
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

@bot.command()
async def verify(ctx):

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
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
            await ctx.send(embed=embed)
        else:
            await member.add_roles(role)
            embed = discord.Embed(title="Verification", color=core_color)
            embed.add_field(name="Added Roles", value=verification_role)
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
            await ctx.send(embed=embed)
    elif dataset["manualverification"] == True:
        member = ctx.message.author
        role = get(member.guild.roles, name=verification_role)
        letters = string.ascii_lowercase
        result_str = ''.join(choice(letters) for i in range(20))
        embed = discord.Embed(title="Manual Verification", description=f"Please type this code in chat:\n\n{result_str}", color=core_color)
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
        await ctx.send(embed=embed)
        try:
            Message = await bot.wait_for('message', timeout=300)
            if Message.content.lower() == str(result_str):
                if role in member.roles:
                    embed = discord.Embed(title="Verification", description="You are already verified. No roles have been added.", color=core_color)
                    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
                    await ctx.send(embed=embed)
                else:
                    await member.add_roles(role)
                    embed = discord.Embed(title="Verification", color=core_color)
                    embed.add_field(name="Added Roles", value=verification_role)
                    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
                    await ctx.send(embed=embed) 


        except asyncio.TimeoutError:
            TimeoutEmbed = discord.Embed(title="Timeout!",  description="You have reached the 300 second timeout! Please send another command if you want to continue!", color=core_color)
            await ctx.send(embed=TimeoutEmbed)

@bot.command()
async def countdown(ctx, time):
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
        timeList = time.split("d")
        timeDown = int(timeList[0]) * 60 * 60 * 24
    else:
        return
    await asyncio.sleep(timeDown)
    embed = discord.Embed(title="Timer is up", description=f"The timer you set for {time} has ended.")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(f"{ctx.author.mention}", embed=embed)
    return

@bot.command()
async def roll(ctx):
    randomMember = choice(ctx.author.guild.members)
    if randomMember != bot.user:
        await ctx.send(f'{randomMember.mention} has been chosen.')
    else:
        randomMember = choice(ctx.author.guild.members)

@bot.command()
async def help(ctx, arg=None):
    if arg == None:
        

        dataset = await bot.prefixData.find_by_id(ctx.guild.id)
        prefix = dataset["prefix"]

        helpEmbed = discord.Embed(color=core_color, title="CORE | Help")
        helpEmbed.set_footer(text="CORE | Help")
        helpEmbed.add_field(name=f"{prefix}help", value="Help Command", inline=False)
        helpEmbed.add_field(name=f"{prefix}rps", value="Rock Paper Scissors", inline=False)
        helpEmbed.add_field(name=f"{prefix}maths", value="A maths game", inline=False)
        helpEmbed.add_field(name=f"{prefix}roll", value="Chooses a random user", inline=False)
        helpEmbed.add_field(name=f"{prefix}purge", value="To clear messages", inline=False)
        helpEmbed.add_field(name=f"{prefix}version", value="Recent update for CORE", inline=False)
        helpEmbed.add_field(name=f"{prefix}kick", value="Kicks a user that you specify", inline=False)
        helpEmbed.add_field(name=f"{prefix}mute", value="Mutes a user that you specify", inline=False)
        helpEmbed.add_field(name=f"{prefix}unmute", value="Unmutes a user that you specify", inline=False)
        helpEmbed.add_field(name=f"{prefix}ban", value="Bans a user that you specify", inline=False)
        helpEmbed.add_field(name=f"{prefix}warn", value="Give a warning to a member.", inline=False)
        helpEmbed.add_field(name=f"{prefix}warnings", value=" What warnings someone has.", inline=False)
        helpEmbed.add_field(name=f"{prefix}config", value="Changes the server configuration", inline=False)
        helpEmbed.add_field(name=f"{prefix}announce", value="Announces a message", inline=False)
        helpEmbed.add_field(name=f"{prefix}load", value="Loads a specific extension", inline=False)
        helpEmbed.add_field(name=f"{prefix}unload", value="Unloads a specific extension", inline=False)
        helpEmbed.add_field(name=f"{prefix}categories", value="Specifies the announce categories", inline=False)
        helpEmbed.add_field(name=f"{prefix}info", value="Information about a member", inline=False)
        helpEmbed.add_field(name=f"{prefix}support" ,value="Support Server", inline=False)
        helpEmbed.add_field(name=f"{prefix}prefix" ,value="Modify the prefix.", inline=False)
        helpEmbed.add_field(name=f"{prefix}countdown", value="The bot pings you when the timer finishes.", inline=False)
        helpEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
        await ctx.send(embed=helpEmbed)
    else:
        with open("commands.json", "r") as f:
            command_data = json.load(f)

        if command_data["commands"][arg] != None:
            result_source = command_data["commands"][arg]
            embed = discord.Embed(title=f"Help | {result_source['name']}", description=f"{result_source['description']}\n\nSyntax: {result_source['syntax']}", color=core_color)
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
            await ctx.send(embed=embed)
        else:
            raise Exception("Argument provided did not match any fields.")

@bot.command()
async def version(ctx):
    updateEmbed = discord.Embed(title="Most recent version:", description="Version 1.1.5\n\n- New prefix command which you can change the prefix and view the current prefix for your server. This will also modify the help command to also include the server prefix in the command name rather than the default '!'.\n\n- Verify command fixed and can now function properly.", color=core_color)
    updateEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=updateEmbed)

@bot.command()
@has_permissions(manage_channels=True)
async def purge(ctx, amount=15):
    new_amount = amount + 1
    await ctx.channel.purge(limit=new_amount)

bot.run(token)
