# Importing Packages

from datetime import datetime
from discord.ext import commands, tasks
import discord
import asyncio
import random
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

import textwrap
import io
import contextlib
import traceback
from traceback import format_exception

from utils.utils import clean_code, Pag

# Creation & Configuration


token = None
mongodbtoken = None

with open("secrets.json", "r") as f:
	secret_data = json.load(f)
	token = secret_data["BOT-TOKEN"]
	mongodbtoken = secret_data["MONGODB-TOKEN"]


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
bot = commands.Bot(command_prefix=get_prefix, description=None, intents=intents, case_insensitive=True)
bot.launch_time = datetime.utcnow()
bot.remove_command("help")

def get_launchtime():
	return bot.launch_time




# Variables


core_color = discord.Color.from_rgb(30, 144, 255)

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
	bot.load_extension('cogs.lcrp')
	bot.load_extension('cogs.announce')
	bot.load_extension('cogs.moderation')
	

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



@bot.event
async def on_message(message):
	if message.author.bot == False:

		dataset = await bot.config.find_by_id(message.guild.id)
		if dataset["link_automoderation"]:
			if "https://" in message.content or "discord.gg/" in message.content:
				if message.author.guild_permissions.manage_guild:
					await bot.process_commands(message)
				else:
					await message.delete()
			await bot.process_commands(message)
		await bot.process_commands(message)


@tasks.loop(seconds=10)
async def status_change():
	statusTable = ["with CORE", "CORE Games", "over CORE Support", "with MikeyCorporation", "commands"]
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

@bot.command(name="reloadcogs")
@commands.is_owner()
async def reloadcogs(ctx):
	bot.unload_extension('cogs.dbl')
	bot.unload_extension('cogs.help')
	bot.unload_extension('cogs.utility')
	bot.unload_extension('cogs.fun')
	bot.unload_extension('cogs.verify')
	bot.unload_extension('cogs.creator')
	bot.unload_extension('cogs.info')
	bot.unload_extension('cogs.config')
	bot.unload_extension('cogs.lcrp')
	bot.unload_extension('cogs.announce')
	bot.unload_extension('cogs.moderation')

	bot.load_extension('cogs.dbl')
	bot.load_extension('cogs.help')
	bot.load_extension('cogs.utility')
	bot.load_extension('cogs.fun')
	bot.load_extension('cogs.verify')
	bot.load_extension('cogs.creator')
	bot.load_extension('cogs.info')
	bot.load_extension('cogs.config')
	bot.load_extension('cogs.lcrp')
	bot.load_extension('cogs.announce')
	bot.load_extension('cogs.moderation')



@bot.command(name="eval", aliases=["exec", "run"], description="Evaluates and runs code on behalf of the bot.", usage="eval <Code>")
@commands.is_owner()
async def _eval(ctx, *, code):
	code = clean_code(code)

	local_variables = {
		"discord": discord,
		"commands": commands,
		"bot": bot,
		"ctx": ctx,
		"channel": ctx.channel,
		"author": ctx.author,
		"guild": ctx.guild,
		"message": ctx.message
	    }

	stdout = io.StringIO()

	try:
		with contextlib.redirect_stdout(stdout):
			exec(
				f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
			)

			obj = await local_variables["func"]()
			result = f"{stdout.getvalue()}\n-- {obj}\n"
	except Exception as e:
		result = "".join(format_exception(e, e, e.__traceback__))

	pager = Pag(
		timeout=100,
		entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
		length=1,
		prefix="```py\n",
		suffix="```"
		)

	await pager.start(ctx)

bot.run(token)
