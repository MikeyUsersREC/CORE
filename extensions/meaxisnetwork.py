from discord.ext import commands
import discord
import requests
core_color = discord.Color.from_rgb(30, 144, 255)

@commands.command()
async def test(ctx):
	payload = {"discordid": ctx.author.id, "secret": "t6ovhm._7-ng9iry-1602428551-gy1pn37w.u06x8_q", "scope": "username"}
	usernameRequest = requests.get("https://api.meaxisnetwork.net/v2/accounts/fromdiscord/", params=payload)
	json = usernameRequest.json()
	username = json["message"]

	payload = {"discordid": ctx.author.id, "secret": "t6ovhm._7-ng9iry-1602428551-gy1pn37w.u06x8_q", "scope": "avatarurl"}
	avatarRequest = requests.get("https://api.meaxisnetwork.net/v2/accounts/fromdiscord/", params=payload)
	print(avatarRequest.json())

def setup(bot):
    bot.add_command(test)