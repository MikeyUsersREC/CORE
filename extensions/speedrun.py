import discord
from discord.ext import commands
import requests
import srcomapi, srcomapi.datatypes as dt

api = srcomapi.SpeedrunCom(); api.debug = 1
core_color = discord.Color.from_rgb(30, 144, 255)
core_image = "https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128"

@commands.command(name="gamesearch", aliases=["searchgame", "search"])
async def gamesearch(ctx, *, game=None):
	if game == None:
		embed = discord.Embed(title="An error has occured.", description="An error has occured that has prevented the command to run properly.", color=core_color)
		await ctx.send(embed=embed)
	else:
		if not game == None:
			search = api.search(srcomapi.datatypes.Game, {"name": game})
			game = search[0]

			GameName = game.names["international"]
			GameAbbreviation = str(game.abbreviation)
			GameIcon = game.assets["cover-large"]["uri"]
			GameID = game.id
			GameCreationDate = game.release_date

			embed = discord.Embed(title=f"{GameName}", color=core_color)
			embed.set_footer(text=f"{GameName} | CORE", icon_url=core_image)

			embed.add_field(name="Name", value=f"{GameName}", inline=False)
			embed.add_field(name="Abbreviation", value=f"{GameAbbreviation.upper()}", inline=False)
			embed.add_field(name="Categories", value=f"{len(game.categories)}", inline=False)
			embed.add_field(name="ID", value=f"{GameID}", inline=False)
			embed.add_field(name="Release Date", value=GameCreationDate, inline=False)

			embed.set_thumbnail(url=GameIcon)

			await ctx.send(embed=embed)


@commands.command(name="usersearch", aliases=["searchuser"])
async def usersearch(ctx, user=None):
	if user == None:
		embed = discord.Embed(title="An error has occured.", description="An error has occured that has prevented the command to run properly.", color=core_color)
		await ctx.send(embed=embed)
	else:
		if not user == None:
			search = api.search(srcomapi.datatypes.User, {"name": user})
			if len(search) != 0:
				UserObject = search[0]
			else:
				UserObject = srcomapi.datatypes.User(api, id=user)
			Country = UserObject.location["country"]["names"]["international"]
			Name = UserObject.name
			Role = UserObject.role.upper()
			UserID = UserObject.id

			RequestObject = requests.get(f"https://speedrun.com/api/v1/users/{UserID}/personal-bests?top=1")
			RequestJSON = RequestObject.json()
			print(RequestJSON)
			RequestList = RequestJSON["data"]

			RunsObject = requests.get(f"https://www.speedrun.com/api/v1/runs?user={UserID}")
			RunsJSON = RunsObject.json()
			print(RunsJSON)
			RunsList = RunsJSON["data"]


			embed = discord.Embed(title=f"{Name}", color=core_color)

			embed.add_field(name="Name", value=f"{Name}", inline=False)
			embed.add_field(name="Country", value=f"{Country}", inline=False)
			embed.add_field(name="Runs (Up to 20)", value=f"{len(RunsList)}", inline=False)
			embed.add_field(name="World Records", value=f"{len(RequestList)}", inline=False)
			embed.add_field(name="Role", value=Role, inline=False)
			embed.add_field(name="ID", value=f"{UserID}", inline=False)
			
			embed.set_thumbnail(url=ctx.author.avatar_url)

			embed.set_footer(text=f"{Name} | CORE", icon_url=core_image)

			await ctx.send(embed=embed)

@commands.command(name="categorysearch")
async def categorysearch(ctx, game, *, category):
	search = api.search(srcomapi.datatypes.Game, {"abbreviation": game})
	if len(search) != 0:
		GameObject = search[0]
	else:
		GameObject = srcomapi.datatypes.Game(api, id=game)

	CategoryList = [item.name for item in GameObject.categories]
	CategoryDescList = [item.rules for item in GameObject.categories]

	GameIcon = GameObject.assets["cover-large"]["uri"]

	CategoryDict = dict()

	for item in CategoryList:
		index = CategoryList.index(item)
		descItem= CategoryDescList[index]
		CategoryDict[item] = descItem

	print(CategoryDict)

	for Category in GameObject.categories:
		print(f" ID of {Category.name} is {Category.id}")


	if category in CategoryDict:
		embed = discord.Embed(title=f"{category} | {GameObject.name}", color=core_color)
		CategorySelected = CategoryDict[category]
		embed.description = f"{category}\n\n{CategorySelected}"
		embed.set_thumbnail(url=GameIcon)
		embed.set_footer(text=f"{GameObject.name} | CORE", icon_url=core_image)
		await ctx.send(embed=embed)
	else:
		raise Exception("This category is not apart of this game.")


@commands.command()
async def leaderboardsearch(ctx, game, *, category):
	GameSearch = api.search(srcomapi.datatypes.Game, {"abbreviation": game})
	if len(GameSearch) != 0:
		Game = GameSearch[0]
	else:
		Game = srcomapi.datatypes.Game(api, id=game)
	
	categoryid = None

	for Category in Game.categories:
		if Category.name == category:
			categoryid = Category.id

	LeaderboardObject = srcomapi.datatypes.Leaderboard(api, data=api.get(f"leaderboards/{Game.id}/category/{categoryid}?top=10"))

	embed = discord.Embed(title=f"Leaderboard for {category}", description="", color=core_color)

	for record in LeaderboardObject.runs:
		
		user = record["run"].players[0]
		CategoryList = [category.name for category in Game.categories]

		if category in CategoryList:
			char_count = 0
			timing = record["run"].times["primary_t"]
			place = record["place"]
			string = f"{place}. {timing} | {category} | {user.name}"
			count = len(string)
			char_count += count

			GameIcon = Game.assets["cover-large"]["uri"]
			
			embed.set_footer(text=f"Showing only 10 results | {Game.name}", icon_url=core_image)

			embed.set_thumbnail(url=GameIcon)

			embed.description = f"{embed.description}{string}\n"

	await ctx.send(embed=embed)

async def runsearch(ctx, *, id):
	Run = api.search(srcomapi.datatypes.Run, {"id": id})

	await ctx.send(f"{dir(Run)}")



def setup(bot):
	bot.add_command(gamesearch)
	bot.add_command(usersearch)
	bot.add_command(categorysearch)
	bot.add_command(leaderboardsearch)