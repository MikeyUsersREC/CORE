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

# Creation & Configuration

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!' , description=None, intents=intents, case_insensitive=True)
bot.remove_command("help")

# Variables

token = "NzM0NDk1NDg2NzIzMjI3NzYw.XxSiOg.m8r2Znmr4sLqf5dr7k9FX4jdgE0"
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

	with open("info.json", "r") as info:
		global data
		data = json.load(info)

	for guild in bot.guilds:
		if str(guild.id) not in data:
			data[str(guild.id)] = {"manualverification": False, "debug_mode": False, "announcement_channel": "announcements", "verification_role": None, "link_automoderation": False}
			print(f"{guild.name} | {guild.id} | Added to JSON.")


	with open("info.json", "w") as info:
		json.dump(data, info, indent=2)

	print(f"{member_count_all} Members")
	bot.loop.create_task(status_change())
	bot.load_extension(f'extensions.dbl')

	for guild in bot.guilds:

		print(f"{str(guild.id)} | {str(guild.name)} | {str(guild.member_count)} Members")

@bot.event
async def on_command_error(ctx, error):
	with open("info.json", "r") as f:
		info_data = json.load(f)

	if info_data[str(ctx.guild.id)]["debug_mode"] == True:
		embed = discord.Embed(title="An error has occured", description=f"You have not put the correct parameters for this command.\n\n\n```{str(error)}```", color=core_color)
		embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
		await ctx.send(embed=embed)
	elif info_data[str(ctx.guild.id)]["debug_mode"] == False:
		embed = discord.Embed(title="An error has occured", description="You have not put the correct parameters for this command.", color=core_color)
		embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
		await ctx.send(embed=embed)


@bot.event
async def on_message(message):
	if message.author.bot == False:
		with open("info.json", "r") as f:
			info_data = json.load(f)

		if info_data[str(message.guild.id)]["link_automoderation"]:
			if "https://" in message.content or "discord.gg/" in message.content:
				if message.author.guild_permissions.manage_guild:
					await bot.process_commands(message)
				else:
					await message.channel.purge(limit=1)
	
	await bot.process_commands(message)

# Status

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


# Commands

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
			with open("info.json", "r") as f:
				data = json.load(f)

			data[str(ctx.guild.id)]["debug_mode"] = True

			with open("info.json", "w") as f:
				json.dump(data, f, indent=2)
			embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
			embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
			await ctx.send(embed=embed)

		elif arg2 == "off":
			with open("info.json", "r") as f:
				data = json.load(f)

			data[str(ctx.guild.id)]["debug_mode"] = False

			with open("info.json", "w") as f:
				json.dump(data, f, indent=2)

			embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
			embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
			await ctx.send(embed=embed)

	if arg1 == "manualverification":
		if arg2 == "on" or arg2 == "true":
			with open("info.json", "r") as f:
				data = json.load(f)

			data[str(ctx.guild.id)]["manualverification"] = True

			with open("info.json", "w") as f:
				json.dump(data, f, indent=2)
			embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
			embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
			await ctx.send(embed=embed)
		else:
			with open("info.json", "r") as f:
				data = json.load(f)

			data[str(ctx.guild.id)]["manualverification"] = False

			with open("info.json", "w") as f:
				json.dump(data, f, indent=2)
			embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
			embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
			await ctx.send(embed=embed)

	if arg1 == "announcement_channel":
		with open("info.json", "r") as f:
			data = json.load(f)

		data[str(ctx.guild.id)]["announcement_channel"] = arg2

		with open("info.json", "w") as f:
			json.dump(data, f, indent=2)
		embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
		embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
		await ctx.send(embed=embed)

	if arg1 == "verification_role":
		with open("info.json", "r") as f:
			data = json.load(f)

		data[str(ctx.guild.id)]["verification_role"] = arg2

		with open("info.json", "w") as f:
			json.dump(data, f, indent=2)

		embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
		embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
		await ctx.send(embed=embed)

	if arg1 == "link_automoderation":
		if arg2 == "on":
			with open("info.json", "r") as f:
				data = json.load(f)

			data[str(ctx.guild.id)]["link_automoderation"] = True

			with open("info.json", "w") as f:
				json.dump(data, f, indent=2)
			embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
			embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
			await ctx.send(embed=embed)

		elif arg2 == "off":
			with open("info.json", "r") as f:
				data = json.load(f)

			data[str(ctx.guild.id)]["link_automoderation"] = False

			with open("info.json", "w") as f:
				json.dump(data, f, indent=2)

			embed = discord.Embed(title="Configuration Changed", description="The configuration has been changed", color=core_color)
			embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
			await ctx.send(embed=embed)

	if arg1 is None and arg2 is None:
		embed = discord.Embed(title="Configuration", description="\n\n**debug** | Debug Mode sends errors in the chat rather than the console.\n\n**manualverification** | Manual Verifications enables code-based chat authenticated verification for servers that support it.\n\n**announcement_channel** | Sets the announcement channel.\n\n**verification_role** | Sets the verification role for servers that support it.\n\n**link_automoderation** | Sets a value so that the bot can check for links.", color=core_color)
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
        try:
            eval(cmd)
            await ctx.send(f'CORE executed your command --> {cmd}')
        except:
            print(f'{cmd} is an invalid command')
            await ctx.send(f'CORE could not execute an invalid command --> {cmd}')



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
    embed = discord.Embed(title="Rock Paper Scissors!", color=core_color)
    if arg.lower() == "rock":
        embed.description = "Paper!"
    elif arg.lower() == "paper":
        embed.description = "Scissors!"
    elif arg.lower() == "scissors":
        embed.description = "Rock!"
    if arg != None:
    	await ctx.send(embed=embed)
    else:
    	raise Exception("No keyword argument specified for the command to run properly. Please put the required arguments and try again.")
# Announcement Commands

@bot.command()
@has_permissions(manage_channels=True) 
async def announce(ctx):
	with open("info.json", "r") as f:
		data = json.load(f)

	announcement_channel = data[str(ctx.guild.id)]["announcement_channel"]
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
	with open("info.json", "r") as f:
		info_data = json.load(f)

	verification_role = info_data[str(ctx.guild.id)]["verification_role"]

	if get(ctx.guild.roles, name=verification_role) == None:
		raise Exception("Configuration contains invalid argument.")
		return

	if info_data[str(ctx.guild.id)]["manualverification"] == False:
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
	elif info_data[str(ctx.guild.id)]["manualverification"] == True:
		member = ctx.message.author
		role = get(member.guild.roles, name="[-] 𝙍𝙊𝘽𝙇𝙊𝙓𝙞𝙖𝙣𝙨")
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
			TimeoutEmbed = discord.Embed(title="Timeout!",	description="You have reached the 300 second timeout! Please send another command if you want to continue!", color=core_color)
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
		helpEmbed = discord.Embed(color=core_color, title="CORE | Help")
		helpEmbed.set_footer(text="CORE | Help")
		helpEmbed.add_field(name="!help", value="Help Command", inline=True)
		helpEmbed.add_field(name="!rps", value="Rock Paper Scissors", inline=True)
		helpEmbed.add_field(name="!maths", value="A maths game", inline=True)
		helpEmbed.add_field(name="!roll", value="Chooses a random user", inline=True)
		helpEmbed.add_field(name="!purge", value="To clear messages", inline=True)
		helpEmbed.add_field(name="!version", value="Recent update for CORE", inline=True)
		helpEmbed.add_field(name="!kick", value="Kicks a user that you specify", inline=True)
		helpEmbed.add_field(name="!mute", value="Mutes a user that you specify", inline=True)
		helpEmbed.add_field(name="!unmute", value="Unmutes a user that you specify", inline=True)
		helpEmbed.add_field(name="!ban", value="Bans a user that you specify", inline=True)
		helpEmbed.add_field(name="!config", value="Changes the server configuration", inline=True)
		helpEmbed.add_field(name="!announce", value="Announces a message", inline=True)
		helpEmbed.add_field(name="!load", value="Loads a specific extension", inline=True)
		helpEmbed.add_field(name="!unload", value="Unloads a specific extension", inline=True)
		helpEmbed.add_field(name="!categories", value="Specifies the announce categories", inline=True)
		helpEmbed.add_field(name="!info", value="Information about a member", inline=True)
		helpEmbed.add_field(name="!support" ,value="Specifies the support server.", inline=True)
		helpEmbed.add_field(name="!invite", value="Invite the bot.", inline=True)
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
    updateEmbed = discord.Embed(title="Most recent version:", description="Version 1.1.2\n\n- New configuration able to be edited with the config command. This configuration is the link_automoderation configuration. This enables automoderation on your server and if it sees a link and the author doesn't have the required Manage Guild previleges, the message will be deleted. The default value for this is off but you can turn it on with the config command.\n\n- New configuration able to be edited with the config command. The verification_role configuration makes it so people can verify in your server with the verify command and they will get the role that you specify here. This works in conjuction with the manualverification configuration which adds an extra layer of authentication when verifying creating a 20 character string needed to be able to gain the role. The verification_role configuration's default value is None.\n\n- The countdown and mute command now has elaborated their time parameter meaning you can set a timer or mute someone for multiple hours or days. The countdown command would be useful for scheduled events such as giveaways and you can now set timers for hours or days so that it would be more useful.\n\n      - The roll command has been modified so that the bot cannot be picked under any circumstances. This is to prevent multiple rerolls because of a bot being chosen.\n\n- Custom errors have been made for convenience whilst troubleshooting why your commands aren't working. Such example would be 'Configuration contains invalid argument'. This error means that a value you put in your configuration does not exist anymore meaning you need to reconfigure your server's settings.\n\n- Critical Maths command bug where the bot would respond to itself causing it to immediately fail has been patched out of the bot with a simple context manager fix.", color=core_color)
    updateEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=updateEmbed)

@bot.command()
@has_permissions(manage_channels=True)
async def purge(ctx, amount=15):
    new_amount = amount + 1
    await ctx.channel.purge(limit=new_amount)

bot.run(token)
