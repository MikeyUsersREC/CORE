
from datetime import datetime 
from discord.ext import commands, tasks 
from discord.ext.commands import CheckFailure, has_role, has_permissions 
from discord.utils import get 
from random import randint, choice 
from traceback import format_exception 
from utils.mongo import Document 
from utils.utils import clean_code, Pag 
# Importing Packages

from datetime import datetime
from discord.ext import commands, tasks
from discord.ext.commands import CheckFailure, has_role, has_permissions
from discord.utils import get
from random import randint, choice
from traceback import format_exception
from utils.mongo import Document
from utils.utils import clean_code, Pag
import gpiozero

import asyncio
import contextlib
import discord
import io
import json
import logging
import motor.motor_asyncio
import requests
import random
import string
import traceback
import textwrap
import traceback


# Creation & Configuration


token = None
mongodbtoken = None

with open("secrets.json", "r") as f:
	secret_data = json.load(f)
	token = secret_data["DISCORD_BOT_TOKEN"]
	mongodbtoken = secret_data["MONGODB_TOKEN"]


if token == None or mongodbtoken == None:
	print('The secrets.json file is not supplied.')

async def get_prefix(client, message):
	mongo = motor.motor_asyncio.AsyncIOMotorClient(mongodbtoken)
	db = mongo["core"]
	prefixes = Document(db, "prefixes")
	if await prefixes.find_by_id(message.guild.id) == None:
		return "!"
	else:
		dataset = await prefixes.find_by_id(message.guild.id)
		return dataset["prefix"]


intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, description=None, intents=intents, case_insensitive=True, help_command=None)
bot.launch_time = datetime.utcnow()


def get_launchtime():
	return bot.launch_time


# Variables


bot.core_color = discord.Color.from_rgb(30, 144, 255)

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

	bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(mongodbtoken)
	bot.db = bot.mongo["core"]
	bot.config = Document(bot.db, "info")
	bot.warningData = Document(bot.db, "warnings")
	bot.prefixData = Document(bot.db, "prefixes")
	bot.actionLogs = {}
	bot.enabledPerGuildExtension = Document(bot.db, "enabledExtensions")

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
	warningDataUpdate.start()
	status_change.start()

	bot.load_extension('cogs.dbl')
	bot.load_extension('cogs.help')
	bot.load_extension('cogs.utility')
	bot.load_extension('cogs.fun')
	bot.load_extension('cogs.verify')
	bot.load_extension('cogs.creator')
	bot.load_extension('cogs.info')
	bot.load_extension('cogs.config')
	bot.load_extension('cogs.announce')
	bot.load_extension('cogs.moderation')
	bot.load_extension('cogs.imagemanipulation')
	bot.load_extension('cogs.auditlog')
	bot.load_extension('cogs.python')
	bot.load_extension('cogs.music')
	bot.load_extension('jishaku')
	bot.load_extension('extensions.meaxisnetwork')
	bot.load_extension('extensions.speedrun')
	bot.load_extension('extensions.roblox')
	bot.load_extension('extensions.erlc')
	
	for guild in bot.guilds:

		print(f"{str(guild.id)} | {str(guild.name)}")
	

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
	await bot.enabledPerGuildExtension.insert({"_id": guild.id})
	try:
		await guild.default_channel.send('Hey! I\'m CORE! My prefix is c! and you can see all my commands via the c!help command!\n\nDocumentation: https://mikeycorporation.com/docs\nSource Code: https://github.com/MikeyUsersREC/CORE\nWebsite (Unfinished): https://mikeycorporation.com\nDiscord Bot List: https://discordbotlist.com/bots/core')
	except:
		pass


@bot.event
async def on_message(message):
	mention = f'<@!{bot.user.id}>'
	if mention in message.content:
		dataset = await bot.prefixData.find_by_id(message.guild.id)
		prefix = dataset["prefix"]
		await message.channel.send(f"My prefix is: `{prefix}`")   
	if message.author.bot == False:

		dataset = await bot.config.find_by_id(message.guild.id)
		print(dataset)
		try:
			if dataset["link_automoderation"]:
				if "https://" in message.content or "discord.gg/" in message.content:
					if message.author.guild_permissions.manage_guild:
						await bot.process_commands(message)
					else:
						await message.delete()
				await bot.process_commands(message)
				return
		except:
			pass
		await bot.process_commands(message)


@tasks.loop(seconds=10)
async def status_change():
	statusTable = ["with CORE",  "CORE Games", "over CORE Support", "with MikeyCorporation", "commands"]
	statusChosen = choice(statusTable)
	if statusChosen != "over CORE Support" and statusChosen != "commands":
		await bot.change_presence(activity=discord.Game(name=statusChosen))
	elif statusChosen == "over CORE Support":
		await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=statusChosen))
	else:
		await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=statusChosen))
		await asyncio.sleep(10)



@tasks.loop(minutes=60)
async def warningDataUpdate():
	for guild in bot.guilds:
		if await bot.warningData.find_by_id(guild.id) == None:
			await bot.warningData.insert({"_id": guild.id, "name": guild.name})
			for member in guild.members:
				dataset = await bot.warningData.find_by_id(guild.id)
				memberKey = str(member.id)
				dataset[memberKey] = {"_id": member.id, "warnings": 0, "kicks": 0, "guild_id": guild.id}
				await bot.warningData.update_by_id(dataset)
				print(f"{member.name} in {guild.name} has been updated to warning database.")
		elif await bot.warningData.find_by_id(guild.id) != None:
			for member in guild.members:
				dataset = await bot.warningData.find_by_id(guild.id)
				memberKey = str(member.id)
				if not memberKey in dataset:
					dataset[memberKey] = {"_id": member.id, "warnings": 0, "kicks": 0, "guild_id": guild.id}
					await bot.warningData.update_by_id(dataset)
					print(f"{member.name} in {guild.name} has been updated to warning database.")
		if await bot.enabledPerGuildExtension.find_by_id(guild.id) == None:
			await bot.enabledPerGuildExtension.insert({"_id": guild.id})
@bot.command()
@has_permissions(manage_guild = True)
async def enable(ctx, extension):
	extension = extension.lower()
	listOfExtensions = ["meaxisnetwork", "roblox", "speedrun", "erlc", "0f128am-1823301-191y9-q77r61-09a99qm-oaowiqu7-177a"]
	if extension not in listOfExtensions:
		await ctx.send('This extension does not exist.')
		return
	if await bot.enabledPerGuildExtension.find_by_id(ctx.guild.id) != None:
		dataset = await bot.enabledPerGuildExtension.find_by_id(ctx.guild.id)
		dataset[extension] = True
		await bot.enabledPerGuildExtension.update_by_id(dataset)
		await ctx.send(f"{extension.capitalize()} has been enabled on your server.")
	else:
		await bot.enabledPerGuildExtension.insert({"_id": ctx.guild.id, extension: True})
		await ctx.send(f"{extension.capitalize()} has been enabled.")
	if extension == "0f128am-1823301-191y9-q77r61-09a99qm-oaowiqu7-177a":
		await ctx.send("**PRIVATE DEVELOPMENT BUILD HAS BEEN ENABLED. USE AT YOUR OWN RISK.**")

@bot.command()
@has_permissions(manage_guild = True)
async def disable(ctx, extension):
	if await bot.enabledPerGuildExtension.find_by_id(ctx.guild.id) != None:
		dataset = await bot.enabledPerGuildExtension.find_by_id(ctx.guild.id)
		dataset[extension] = False
		await bot.enabledPerGuildExtension.update_by_id(dataset)
		await ctx.send(f"{extension.capitalize()} has been disabled on your server.")
	else:
		await ctx.send("You cannot disable an extension you have not enabled.")


@bot.command(name="reloadcogs")
@commands.is_owner()
async def reloadcogs(ctx):
	bot.reload_extension('cogs.dbl')
	bot.reload_extension('cogs.help')
	bot.reload_extension('cogs.utility')
	bot.reload_extension('cogs.fun')
	bot.reload_extension('cogs.verify')
	bot.reload_extension('cogs.creator')
	bot.reload_extension('cogs.info')
	bot.reload_extension('cogs.config')
	bot.reload_extension('cogs.announce')
	bot.reload_extension('cogs.moderation')
	bot.reload_extension('cogs.imagemanipulation')
	bot.reload_extension('cogs.auditlog')
	bot.reload_extension('cogs.python')

	bot.reload_extension('extensions.meaxisnetwork')
	bot.reload_extension('extensions.speedrun')
	bot.reload_extension('extensions.roblox')
	bot.reload_extension('extensions.erlc')

try:
	bot.run(token)
except Exception as e:
	print('Failed to start the bot. Stack trace:')
	print(e)
