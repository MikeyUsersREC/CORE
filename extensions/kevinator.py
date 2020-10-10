from discord.ext import commands
import discord
core_color = discord.Color.from_rgb(30, 144, 255)

@commands.command()
async def tag(self, ctx, argument):
    if argument == "mod":
        embed = discord.Embed(title="Moderator Form", url="https://forms.gle/fduX4QMDu29NTkLE9", description="This is the moderator form.", color=core_color)
        await ctx.send(embed=embed)
    elif argument == "twitch":
        embed = discord.Embed(title="Kevinator's Twitch", url="https://twitch.tv/keviiinator", description="This is the twitch channel.", color=core_color)
        await ctx.send(embed=embed)
    elif argument == "discord":
        embed = discord.Embed(title="Discord Invite", url="https://discord.gg/P24XMKP", description="This is the discord invite.", color=core_color)
        await ctx.send(embed=embed)
    elif argument == "rules":
        embed = discord.Embed(title="Kevinator Gang | Guidelines", description="1. You cannot ping staff members without permission in any situation.\n\n2. Respect people how you would like to be treated.\n\n3. In no circumstances can you disrespect anyone else in our community.\n\n4. Bullying is not tolerated, no matter whether it is a joke or not.\n\n5. Our Moderators know what they are doing and any arguments that arise from a moderator actions will be dealt with professionally. \n\n6. Failure to comply with Moderators can result in a severe punishment.\n\n7. People may not share links or files that may harm other users/yourself.\n\n8. Spamming chat will not be permitted.\n\n9. NSFW Language, Avatars or Nicknames will result in a punishment.\n\n10. Do not ask for any roles or permissions unless absolutely necessary.\n\n11. Terms and Conditions require to be followed by all members in our server.\n\n12. Content must be relevant to the channel you put it in.\n\n13. No Disrupting Stream.\n\n14. Punishments cannot be biased or unlawful, every punishment made by a Moderator must be reasoned.\n\n15. You shall not try to be annoying or hindering to a Moderator.\n\n16. You cannot bypass the rules in any way shape or form.", color=discord.Color.from_rgb(252, 206, 0))
        await ctx.send(embed=embed)
    elif argument == "protocols" or argument == "warnings":
        embed = discord.Embed(title="KDS | Discord Warning System", description="Warning 1: Verbal Warning \nWarning 2: Warning\nWarning 3: Kick\nWarning 4: 12h Mute\nWarning 5: 24h Mute\nWarning 6: Ban", color=core_color)
        await ctx.send(embed=embed)
    return

def setup(bot):
    bot.add_command(tag)