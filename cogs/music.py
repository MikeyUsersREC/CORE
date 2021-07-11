import discord
from discord.ext import commands
import DiscordUtils

music = DiscordUtils.Music()

class MusicCommands(commands.Cog, name = "Music Commands"):
		def __init__(self, bot):
			self.bot = bot

		@commands.command(name = "join", description = "Joins the author's voice channel.")
		async def join(self, ctx):
			await ctx.author.voice.channel.connect()

		@commands.command(name = "leave", description = "Leaves the associated voice channel.")
		async def leave(self, ctx):
			await ctx.voice_client.disconnect()
    
		@commands.command(name = "play", description = "Plays the requested song.")
		async def play(self, ctx, *, url):
			player = music.get_player(guild_id=ctx.guild.id)
			if not player:
				player = music.create_player(ctx, ffmpeg_error_betterfix=True)
			if not ctx.voice_client.is_playing():
				try:
					await player.queue(url)
				except:
					await player.queue(url, search = True)
				song = await player.play()
				await ctx.send(f"Playing {song.name}")
			else:
				song = await player.queue(url, search=True)
				await ctx.send(f"Queued {song.name}")
        
		@commands.command(name = "pause", description = "Pauses the current song.")
		async def pause(self, ctx):
			player = music.get_player(guild_id=ctx.guild.id)
			song = await player.pause()
			await ctx.send(f"Paused {song.name}")
    
		@commands.command(name = "resume", description = "Resumes the current song.")
		async def resume(self, ctx):
    			player = music.get_player(guild_id=ctx.guild.id)
    			song = await player.resume()
    			await ctx.send(f"Resumed {song.name}")
    
		@commands.command(name = "stop", description = "Stops the current song.")
		async def stop(self, ctx):
			player = music.get_player(guild_id=ctx.guild.id)
			await player.stop()
			await ctx.send("Successfully stopped.")
    
		@commands.command(name = "loop", description = "Loops the current song.")
		async def loop(self, ctx):
			player = music.get_player(guild_id=ctx.guild.id)
			song = await player.toggle_song_loop()
			if song.is_looping:
				await ctx.send(f"Enabled loop for {song.name}")
			else:
				await ctx.send(f"Disabled loop for {song.name}")
    
		@commands.command(name = "queue", aliases = ["q"], description = "Displays the current queue.")
		async def queue(self, ctx):
			player = music.get_player(guild_id=ctx.guild.id)
			await ctx.send(f"{', '.join([song.name for song in player.current_queue()])}")
    
		@commands.command(name = "np", aliases = ["now_playing", "nowplaying", "playing"], description = "Sends the song currently playing.")
		async def np(self, ctx):
 		   player = music.get_player(guild_id=ctx.guild.id)
 		   song = player.now_playing()
 		   await ctx.send(song.name)
    
		@commands.command(name = "skip", description = "Skips the current song.")
		async def skip(self, ctx):
		    player = music.get_player(guild_id=ctx.guild.id)
		    data = await player.skip(force=True)
		    if len(data) == 2:
		        await ctx.send(f"Skipped from {data[0].name} to {data[1].name}")
		    else:
		        await ctx.send(f"Skipped {data[0].name}")

		@commands.command(name = "volume", description = "Changes the volume of the current song.")
		async def volume(self, ctx, vol):
    			player = music.get_player(guild_id=ctx.guild.id)
    			song, volume = await player.change_volume(float(vol) / 100) # volume should be a float between 0 to 1
    			await ctx.send(f"Changed volume for {song.name} to {volume*100}%")

		@commands.command(name = "remove", description = "Removes a song from the queue.")
		async def remove(self, ctx, index):
			player = music.get_player(guild_id=ctx.guild.id)
			song = await player.remove_from_queue(int(index))
			await ctx.send(f"Removed {song.name} from queue")

def setup(bot):
	bot.add_cog(MusicCommands(bot))
