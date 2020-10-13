from discord.ext import commands
import discord
import requests
core_color = discord.Color.from_rgb(30, 144, 255)

@commands.command()
async def myaccount(ctx):
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

	embed = discord.Embed(title=username, description=f"{description}\nAccount ID: {AccountID}", color=core_color)
	await ctx.send(embed=embed)

def setup(bot):
    bot.add_command(myaccount)