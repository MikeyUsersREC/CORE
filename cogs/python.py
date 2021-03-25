import discord
from discord.ext import commands
from discord.ext.commands import Context
import requests
import random
import re
import typing as t
from discord import Embed

URL = 'https://cheat.sh/python/{search}'
ESCAPE_TT = str.maketrans({"`": "\\`"})
ANSI_RE = re.compile(r"\x1b\[.*?m")
# We need to pass headers as curl otherwise it would default to aiohttp which would return raw html.
HEADERS = {'User-Agent': 'curl/7.68.0'}


class CheatSheet(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def result_fmt(self, url: str, body_text: str) -> t.Tuple[bool, t.Union[str, Embed]]:
        if body_text.startswith("#  404 NOT FOUND"):
            return True

        body_space = min(1986 - len(url), 1000)

        if len(body_text) > body_space:
            description = (f"**Result Of cht.sh**\n"
                           f"```python\n{body_text[:body_space]}\n"
                           f"... (truncated - too many lines)```\n"
                           f"Full results: {url} ")
        else:
            description = (f"**Result Of cht.sh**\n"
                           f"```python\n{body_text}```\n"
                           f"{url}")
        return False, description

    @commands.command(
        name="cheat",
        aliases=("cht.sh", "cheatsheet", "cheat-sheet", "cht"),
        description = "Gets example python for the search query you use."
    )
    async def cheat_sheet(self, ctx: Context, *, search_terms: str) -> None:
        async with ctx.typing():
            search_string = search_terms

            response = requests.get(URL.format(search = search_string), headers = HEADERS)
            result = ANSI_RE.sub("", response.text).translate(ESCAPE_TT)

            is_embed, description = self.result_fmt(
                URL.format(search=search_string),
                result
            )
            if is_embed:
                await ctx.send(embed=description)
            else:
                await ctx.send(content=description)

def setup(bot):
        bot.add_cog(CheatSheet(bot))
