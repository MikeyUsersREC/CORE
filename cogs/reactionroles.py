import discord
from discord.ext import commands
import json

class ReactionRoles(commands.Cog, name="Reaction Roles"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="setreactionrole", aliases=["srr"], description="Sets the reaction roles for a message.", usage="setreactionrole <Role> <Message ID> <Emoji>")
	async def setreactionrole(self, ctx, role: discord.Role=None, msg: discord.Message=None, emoji=None):
		if role != None and msg != None and emoji != None:
			await msg.add_reaction(emoji)
			self.bot.reaction_roles[f"{emoji} | {msg.id}"] = [emoji, msg.id, role.id]

			with open(self.bot.reaction_file, "w"):
				self.bot.reaction_roles = json.load(f)


			await ctx.channel.send("Reaction has been set.")				
		else:
		 	await ctx.send("Invalid arguments.")


	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		for key, values in self.bot.reaction_roles.items():
			if key == f"{payload.emoji.name} | {payload.message_id}":
				await payload.member.add_roles(self.bot.get_guild(payload.guild_id).get_role(role_id))
				return

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		for key, values in self.bot.reaction_roles.items():
			if key == f"{payload.emoji.name} | {payload.message_id}":
				await payload.member.add_roles(self.bot.get_guild(payload.guild_id).get_role(role_id))
				return


def setup(bot):
	bot.add_cog(ReactionRoles(bot))